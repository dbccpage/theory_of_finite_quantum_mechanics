"""Exact finite Hubbard fixture, evaluated with SQLite and exact rationals.

Vendored subset of two repository files at commit
fb332922230b8b2d6a25184439b3eca5f3067c32:

- omega_engine_projects/fsp/code/sign_sql/exact_models.py
  (SHA-256 a0b3301af1a38618d59a16a92a462f026a40263f0726d32e3e7ea910588bbaa1)
- omega_engine_projects/fsp/databases/meron_hubbard.sql
  (SHA-256 2e772cb9eccd510aed828b5f71438dddef7ead99a26bd99f3009039888b07c49)

Only the Hubbard functions were copied, from ``rational`` through
``hop_sign``, then from ``occupation_hubbard`` through
``hubbard_transfer_trace`` inclusive. The schema is read from the sibling
file ``hubbard_schema.sql``, which holds the bit table, experiment metadata,
and Hubbard tables and views of the second file. The import block and the
schema path are the only other changes; no arithmetic function and no SQL
statement was edited. The only SQL arithmetic extensions are scalar rational
operations, a stepwise rational sum, and integer popcount.
"""

from __future__ import annotations

import json
import sqlite3
from fractions import Fraction
from pathlib import Path

SCHEMA = Path(__file__).resolve().with_name("hubbard_schema.sql")


def rational(value: object) -> Fraction:
    """Reject approximate numbers, including integral floats and booleans."""
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise TypeError("exact integer, fraction, or rational string required")
    if isinstance(value, str) and any(c in value.lower() for c in ".e"):
        raise ValueError("decimal/exponent syntax is not an exact rational input")
    return Fraction(value)


class RationalSum:
    def __init__(self) -> None:
        self.total = Fraction(0)

    def step(self, value: str) -> None:
        self.total += rational(value)

    def finalize(self) -> str:
        return str(self.total)


def connection() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys=ON")
    con.create_function("qadd", 2, lambda a, b: str(rational(a) + rational(b)))
    con.create_function("qmul", 2, lambda a, b: str(rational(a) * rational(b)))
    con.create_function("qdiv", 2, lambda a, b: str(rational(a) / rational(b)))
    con.create_function("qabs", 1, lambda a: str(abs(rational(a))))
    con.create_function("qsign", 1, lambda a: (rational(a) > 0) - (rational(a) < 0))
    con.create_function("qpow", 2, lambda a, n: str(rational(a) ** n))
    con.create_function("popcount", 1, int.bit_count)
    con.create_aggregate("qsum", 1, RationalSum)
    con.executescript(SCHEMA.read_text(encoding="utf-8"))
    return con


def save_parameters(con: sqlite3.Connection, parameters: dict) -> None:
    con.execute("INSERT INTO experiment_metadata VALUES('parameters',?)",(json.dumps(parameters,sort_keys=True),))


def parameters(con: sqlite3.Connection) -> dict:
    row=con.execute("SELECT value FROM experiment_metadata WHERE key='parameters'").fetchone()
    return json.loads(row[0]) if row else {}


def hop_sign(state: int, source: int, target: int) -> int:
    lo, hi = sorted((source, target))
    occupied_between = (state >> (lo + 1)) & ((1 << (hi - lo - 1)) - 1)
    return -1 if occupied_between.bit_count() % 2 else 1

def occupation_hubbard(sites: int, bonds: list[tuple[int,int]], n_up: int, n_down: int,
                       interaction: object = 4, hopping: object = 1, chemical: object = 0) -> sqlite3.Connection:
    """Construct H in up-orbitals-then-down-orbitals ordering, exactly."""
    if type(sites) is not int or not 1 <= sites <= 6:
        raise ValueError("one to six sites required")
    if any(type(n) is not int or not 0 <= n <= sites for n in (n_up,n_down)):
        raise ValueError("invalid particle sector")
    bonds = validate_bonds(sites,bonds)
    u,t,mu = map(rational,(interaction,hopping,chemical))
    con = connection()
    save_parameters(con,{"model":"occupation-basis ordinary Hubbard","sites":sites,"bonds":bonds,
                         "n_up":n_up,"n_down":n_down,"interaction":str(u),"hopping":str(t),"chemical":str(mu),
                         "orbital_order":"all up orbitals then all down orbitals"})
    states = [up | (down << sites) for up in range(1 << sites) if up.bit_count()==n_up
              for down in range(1 << sites) if down.bit_count()==n_down]
    con.executemany("INSERT INTO hubbard_basis VALUES(?)", ((s,) for s in states))
    entries = []
    for state in states:
        double = sum(((state >> x)&1)*((state >> (sites+x))&1) for x in range(sites))
        entries.append((state,state,str(u*double-mu*(n_up+n_down))))
        for x,y in bonds:
            for spin in range(2):
                a,b = x+spin*sites,y+spin*sites
                if ((state >> a) ^ (state >> b))&1:
                    target = state ^ (1 << a) ^ (1 << b)
                    entries.append((state,target,str(-t*hop_sign(state,a,b))))
    con.executemany("INSERT INTO hubbard_hamiltonian VALUES(?,?,?)", entries)
    return con


def validate_bonds(sites: int, bonds: list[tuple[int,int]]) -> list[tuple[int,int]]:
    normalized = []
    for edge in bonds:
        if len(edge)!=2 or any(type(x) is not int or x<0 or x>=sites for x in edge) or edge[0]==edge[1]:
            raise ValueError("simple finite undirected hopping graph required")
        normalized.append(tuple(sorted(edge)))
    if len(set(normalized)) != len(normalized):
        raise ValueError("duplicate undirected hopping bond")
    return sorted(normalized)


def gauge_obstruction(con: sqlite3.Connection) -> dict:
    """SQL traverses the signed double cover; +/- reachability detects frustration."""
    con.executescript("""
    DROP TABLE IF EXISTS temp.gauge_reach;
    CREATE TEMP TABLE gauge_reach AS
    WITH RECURSIVE reach(root,node,sign) AS (
      SELECT state,state,1 FROM hubbard_basis UNION
      SELECT r.root,h.target,-r.sign*qsign(h.value) FROM reach r
      JOIN hubbard_hamiltonian h ON h.source=r.node
      WHERE h.source<>h.target AND qsign(h.value)<>0
    ) SELECT * FROM reach;
    """)
    bad = con.execute("SELECT root FROM gauge_reach WHERE root=node AND sign=-1 ORDER BY root LIMIT 1").fetchone()
    vertices = con.execute("SELECT COUNT(*) FROM hubbard_basis").fetchone()[0]
    if bad:
        # BFS over a finite signed double cover returns a shortest negative cycle.
        # SQL performs the same reachability independently above; this stores a readable witness.
        from collections import deque
        start = bad[0]
        edges = con.execute("SELECT source,target,-qsign(value) FROM hubbard_hamiltonian WHERE source<>target AND qsign(value)<>0 ORDER BY source,target").fetchall()
        adjacency = {}
        for a,b,s in edges:
            adjacency.setdefault(a,[]).append((b,s))
        queue = deque([(start,1,[start])]); seen={(start,1)}
        while queue:
            node,sign,path=queue.popleft()
            for target,edge_sign in adjacency.get(node,[]):
                item=(target,sign*edge_sign)
                if item==(start,-1):
                    return {"experiment_parameters":parameters(con),"basis_states":vertices,"diagonal_sign_gauge":False,"negative_cycle":path+[target]}
                if item not in seen:
                    seen.add(item);queue.append((*item,path+[target]))
        raise AssertionError("SQL obstruction lacks a reconstruction")
    gauge = con.execute("""SELECT r.node,r.sign FROM gauge_reach r JOIN
      (SELECT node,MIN(root) root FROM gauge_reach GROUP BY node) c ON c.node=r.node AND c.root=r.root ORDER BY r.node""").fetchall()
    return {"experiment_parameters":parameters(con),"basis_states":vertices,"diagonal_sign_gauge":True,"gauge":gauge}


def sql_matrix_product(con: sqlite3.Connection, left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    size=len(left)
    con.execute("DELETE FROM scalar_matrix")
    con.executemany("INSERT INTO scalar_matrix VALUES(?,?,?,?)",
        ((side,i,j,str(mat[i][j])) for side,mat in enumerate((left,right)) for i in range(size) for j in range(size)))
    rows=con.execute("""SELECT a.i,b.j,qsum(qmul(a.value,b.value)) FROM scalar_matrix a
      JOIN scalar_matrix b ON b.side=1 AND b.i=a.j WHERE a.side=0 GROUP BY a.i,b.j ORDER BY a.i,b.j""").fetchall()
    return [[rational(rows[i*size+j][2]) for j in range(size)] for i in range(size)]


def kinetic_matrix(con: sqlite3.Connection, sites: int, bonds: list[tuple[int,int]], r: object) -> list[list[Fraction]]:
    """Palindromic product of exact bond exponentials; r=exp(delta_tau*t/2)."""
    bonds=validate_bonds(sites,bonds);r=rational(r)
    if r<=0:
        raise ValueError("bond exponential parameter must be positive")
    identity=[[Fraction(i==j) for j in range(sites)] for i in range(sites)]
    matrix=identity
    for x,y in bonds+list(reversed(bonds)):
        bond=[row[:] for row in identity]
        bond[x][x]=bond[y][y]=(r+1/r)/2
        bond[x][y]=bond[y][x]=(r-1/r)/2
        matrix=sql_matrix_product(con,bond,matrix)
    return matrix


def auxiliary_hubbard(sites: int, bonds: list[tuple[int,int]], slices: int=2, r: object="3/2",
                      hs: object="2", fugacity: object="1", attractive: bool=False,
                      field_masks: list[int] | None=None) -> sqlite3.Connection:
    """Finite Trotter Hubbard determinant experiment; positive HS scalar omitted.

    SQL enumerates fields, multiplies all spin matrices, and computes determinants
    by recursive signed permutation folding. Bounds are explicit, not asymptotic.
    """
    if type(sites) is not int or not 1<=sites<=6 or type(slices) is not int or slices<1 or sites*slices>16:
        raise ValueError("finite fixture requires 1..6 sites, at most 16 field bits")
    hs,z = rational(hs),rational(fugacity)
    if hs<1 or z<=0:
        raise ValueError("hs>=1 and fugacity>0 required")
    if type(attractive) is not bool:
        raise TypeError("attractive must be boolean")
    con=connection()
    matrix=kinetic_matrix(con,sites,bonds,r)
    save_parameters(con,{"model":"particle-hole-centered Hubbard Suzuki transfer","sites":sites,
                         "bonds":validate_bonds(sites,bonds),"slices":slices,"r":str(rational(r)),"hs":str(hs),
                         "fugacity":str(z),"attractive":attractive,"field_masks":field_masks,
                         "kinetic_schedule":"sorted bonds followed by reverse sorted bonds",
                         "delta_tau_t":"2 log(r)","delta_tau_abs_U":"2 log((hs+1/hs)/2)",
                         "delta_tau_shifted_mu":"log(fugacity)"})
    con.execute("INSERT INTO dq_parameter VALUES(?,?,?,?,?)",(sites,slices,str(hs),str(z),int(attractive)))
    con.executemany("INSERT INTO dq_site VALUES(?)",((i,) for i in range(sites)))
    con.executemany("INSERT INTO dq_kinetic VALUES(?,?,?)",((i,j,str(matrix[i][j])) for i in range(sites) for j in range(sites)))
    if field_masks is None:
        con.execute("""INSERT INTO dq_field WITH RECURSIVE fields(mask) AS
          (SELECT 0 UNION ALL SELECT mask+1 FROM fields,dq_parameter WHERE mask+1<(1 << (sites*slices))) SELECT mask FROM fields""")
    else:
        if len(set(field_masks))!=len(field_masks) or any(type(mask) is not int or not 0<=mask<(1 << (sites*slices)) for mask in field_masks):
            raise ValueError("field masks must be distinct valid integers")
        if not field_masks:
            raise ValueError("at least one field mask required")
        con.executemany("INSERT INTO dq_field VALUES(?)",((mask,) for mask in field_masks))
    con.execute("INSERT INTO dq_product SELECT mask,bit,a.site,b.site,CAST(a.site=b.site AS TEXT) FROM dq_field CROSS JOIN bit CROSS JOIN dq_site a CROSS JOIN dq_site b")
    for time in range(slices):
        con.execute("DELETE FROM dq_next")
        con.execute("""INSERT INTO dq_next
          SELECT p.mask,p.spin,k.i,p.j,
          qsum(qmul(qmul(k.value,qmul(fugacity,qpow(hs,
             (2*((p.mask >> (?*sites+k.j))&1)-1)*CASE WHEN attractive=1 OR p.spin=0 THEN 1 ELSE -1 END))),p.value))
          FROM dq_product p JOIN dq_kinetic k ON k.j=p.i CROSS JOIN dq_parameter
          GROUP BY p.mask,p.spin,k.i,p.j""",(time,))
        con.execute("DELETE FROM dq_product")
        con.execute("INSERT INTO dq_product SELECT * FROM dq_next")
    con.executescript(DQ_DETERMINANTS)
    return con


DQ_DETERMINANTS = """
INSERT INTO dq_determinant
WITH RECURSIVE determinants(mask,spin,row,used,value,derivative) AS (
 SELECT mask,bit,0,0,'1','0' FROM dq_field CROSS JOIN bit UNION ALL
 SELECT d.mask,d.spin,d.row+1,d.used | (1 << m.j),
 qmul(d.value,qmul(CASE WHEN popcount(d.used >> (m.j+1))%2=0 THEN 1 ELSE -1 END,
 qadd(m.value,CAST(m.i=m.j AS TEXT)))),
 qmul(CASE WHEN popcount(d.used >> (m.j+1))%2=0 THEN 1 ELSE -1 END,
 qadd(qmul(d.derivative,qadd(m.value,CAST(m.i=m.j AS TEXT))),qmul(d.value,qmul(CAST(slices AS TEXT),m.value))))
 FROM determinants d JOIN dq_product m ON m.mask=d.mask AND m.spin=d.spin AND m.i=d.row
 CROSS JOIN dq_parameter
 WHERE (d.used & (1 << m.j))=0
)
SELECT mask,spin,qsum(value),qsum(derivative) FROM determinants,dq_parameter WHERE row=sites GROUP BY mask,spin;
"""


def auxiliary_summary(con: sqlite3.Connection) -> dict:
    validate_auxiliary_support(con)
    rows=con.execute("SELECT * FROM dq_weight ORDER BY mask").fetchall()
    total,absolute=con.execute("SELECT qsum(weight),qsum(qabs(weight)) FROM dq_weight").fetchone()
    number=con.execute("SELECT qsum(numerator) FROM dq_number").fetchone()[0]
    negative=[{"mask":row[0],"up":row[1],"down":row[2],"weight":row[3]} for row in rows if rational(row[3])<0]
    # Identity is checked with rational arithmetic, including zero determinants.
    sites,slices,hs,z,attractive=con.execute("SELECT * FROM dq_parameter").fetchone()
    pairing=[]
    for mask,up,down,weight in rows:
        prefactor=rational(hs)**(2*mask.bit_count()-sites*slices)
        pairing.append(rational(down)==rational(up)/prefactor if not attractive and z=="1" else rational(down)==rational(up) if attractive else None)
    exhaustive=len(rows)==(1 << (sites*slices))
    average=str(rational(total)/rational(absolute)) if rational(absolute) else None
    return {"experiment_parameters":parameters(con),"fields":len(rows),"field_coverage":"exhaustive" if exhaustive else "selected fields only",
            "negative_fields":len(negative),"zero_fields":sum(rational(row[3])==0 for row in rows),
            "determinant_sum":total,"absolute_determinant_sum":absolute,
            "particle_number_numerator":number,
            "particle_number_expectation":str(rational(number)/rational(total)) if exhaustive and rational(total) else None,
            "average_sign":average if exhaustive else None,"full_ensemble_average_sign":average if exhaustive else None,
            "selected_subset_average_sign":None if exhaustive else average,
            "pairing_verified":all(pairing) if None not in pairing else None,
            "first_negative":negative[0] if negative else None,
            "normalization":"global positive Hubbard-Stratonovich scalar omitted; attractive field-dependent scalar included"}


def validate_auxiliary_support(con: sqlite3.Connection) -> None:
    """Reject stale or partial relation support before issuing any certificate."""
    key_columns={"dq_field":("mask",),"dq_product":("mask","spin","i","j"),
                 "dq_determinant":("mask","spin"),"dq_parameter":("sites","slices","attractive")}
    for table,columns in key_columns.items():
        invalid=" OR ".join(f"typeof({column}) <> 'integer'" for column in columns)
        if con.execute(f"SELECT COUNT(*) FROM {table} WHERE {invalid}").fetchone()[0]:
            raise ValueError(f"{table} key columns must contain SQLite INTEGER values")
    declared=parameters(con)
    sites,slices=declared["sites"],declared["slices"]
    expected=set(range(1 << (sites*slices))) if declared["field_masks"] is None else set(declared["field_masks"])
    actual={mask for mask, in con.execute("SELECT mask FROM dq_field")}
    if actual!=expected:
        raise ValueError("auxiliary field support differs from declared experiment")
    for table,per_field in (("dq_product",2*sites*sites),("dq_determinant",2)):
        support={mask:count for mask,count in con.execute(f"SELECT mask,COUNT(*) FROM {table} GROUP BY mask")}
        if set(support)!=expected or any(count!=per_field for count in support.values()):
            raise ValueError(f"{table} support differs from admitted fields")
        if con.execute(f"SELECT COUNT(*) FROM {table} WHERE spin NOT IN(0,1)").fetchone()[0]:
            raise ValueError(f"{table} contains an invalid spin key")
    if con.execute("SELECT COUNT(*) FROM dq_product WHERE i<0 OR j<0 OR i>=? OR j>=?",(sites,sites)).fetchone()[0]:
        raise ValueError("dq_product matrix key outside declared domain")
    observed=con.execute("SELECT sites,slices,hs,fugacity,attractive FROM dq_parameter").fetchall()
    expected_parameters=[(sites,slices,declared["hs"],declared["fugacity"],int(declared["attractive"]))]
    if observed!=expected_parameters:
        raise ValueError("auxiliary parameter relation differs from declared experiment")


def hubbard_transfer_trace(sites: int, bonds: list[tuple[int,int]], slices: int=2,
                           r: object="3/2", hs: object="2", fugacity: object="1", attractive: bool=False,
                           number_numerator: bool=False) -> str:
    """Independent full-Fock trace, used to replay the HS reconstruction.

    The global C^(sites*slices) is removed, C=exp(-dt*abs(U)/4)/2.
    This is exponential in sites and intentionally restricted to <=3 sites.
    """
    if type(sites) is not int or not 1<=sites<=3 or type(slices) is not int or slices<1:
        raise ValueError("independent dense replay requires one to three sites")
    bonds=validate_bonds(sites,bonds)
    r,h,z=map(rational,(r,hs,fugacity))
    if r<=0 or h<1 or z<=0 or type(attractive) is not bool:
        raise ValueError("invalid exact Hubbard transfer parameters")
    dim=1 << (2*sites)
    matrix=[[Fraction(i==j) for j in range(dim)] for i in range(dim)]
    c,s=(r+1/r)/2,(r-1/r)/2
    for _ in range(slices):
        # B=T V: onsite factors first, then kinetic factors, in column convention.
        for state in range(dim):
            factor=z**state.bit_count()
            for x in range(sites):
                up,down=(state >> x)&1,(state >> (sites+x))&1
                exponent=up+down-1 if attractive else up-down
                factor *= h**exponent+h**(-exponent)
            matrix[state]=[factor*entry for entry in matrix[state]]
        for x,y in bonds+list(reversed(bonds)):
            for spin in range(2):
                a,b=x+spin*sites,y+spin*sites
                updated=[[Fraction(0) for _ in range(dim)] for _ in range(dim)]
                for state in range(dim):
                    mixed=((state >> a)^(state >> b))&1
                    diagonal=c if mixed else Fraction(1)
                    for origin in range(dim):
                        updated[state][origin]+=diagonal*matrix[state][origin]
                        if mixed:
                            target=state^(1 << a)^(1 << b)
                            updated[target][origin]+=s*hop_sign(state,a,b)*matrix[state][origin]
                matrix=updated
    total=Fraction(0)
    for i in range(dim):
        total+=(i.bit_count() if number_numerator else 1)*matrix[i][i]
    return str(total)


create_hubbard_connection = connection


def run_occupation_analysis(
    sites: int,
    bonds: list[tuple[int, int]],
    n_up: int,
    n_down: int,
    interaction: str = "4",
    hopping: str = "1",
    chemical: str = "0",
) -> dict:
    """Build the occupation Hamiltonian and report the diagonal sign gauge."""
    con = occupation_hubbard(
        sites=sites,
        bonds=bonds,
        n_up=n_up,
        n_down=n_down,
        interaction=interaction,
        hopping=hopping,
        chemical=chemical,
    )
    obstruction = gauge_obstruction(con)
    return {
        "sites": sites,
        "bonds": bonds,
        "n_up": n_up,
        "n_down": n_down,
        "interaction": interaction,
        "basis_states": con.execute("SELECT COUNT(*) FROM hubbard_basis").fetchone()[0],
        "hamiltonian_entries": con.execute("SELECT COUNT(*) FROM hubbard_hamiltonian").fetchone()[0],
        "diagonal_sign_gauge": obstruction["diagonal_sign_gauge"],
        "negative_cycle": obstruction.get("negative_cycle"),
        "gauge": obstruction.get("gauge"),
    }


def run_auxiliary_field_analysis(
    sites: int,
    bonds: list[tuple[int, int]],
    slices: int = 2,
    r: str = "3/2",
    hs: str = "2",
    fugacity: str = "1",
    attractive: bool = False,
    field_masks: list[int] | None = None,
) -> dict:
    """Evaluate auxiliary-field determinants and return the summary record."""
    con = auxiliary_hubbard(
        sites=sites,
        bonds=bonds,
        slices=slices,
        r=r,
        hs=hs,
        fugacity=fugacity,
        attractive=attractive,
        field_masks=field_masks,
    )
    return auxiliary_summary(con)


def verify_direct_fock_trace(
    sites: int,
    bonds: list[tuple[int, int]],
    slices: int = 2,
    r: str = "3/2",
    hs: str = "2",
    fugacity: str = "3/2",
    attractive: bool = False,
) -> dict:
    """Replay the auxiliary-field sum against the dense Fock transfer trace."""
    direct_trace = hubbard_transfer_trace(
        sites=sites,
        bonds=bonds,
        slices=slices,
        r=r,
        hs=hs,
        fugacity=fugacity,
        attractive=attractive,
        number_numerator=False,
    )
    direct_number = hubbard_transfer_trace(
        sites=sites,
        bonds=bonds,
        slices=slices,
        r=r,
        hs=hs,
        fugacity=fugacity,
        attractive=attractive,
        number_numerator=True,
    )
    summary = run_auxiliary_field_analysis(
        sites=sites,
        bonds=bonds,
        slices=slices,
        r=r,
        hs=hs,
        fugacity=fugacity,
        attractive=attractive,
    )
    return {
        "direct_trace": direct_trace,
        "auxiliary_sum": summary["determinant_sum"],
        "trace_matches": direct_trace == summary["determinant_sum"],
        "direct_number_numerator": direct_number,
        "auxiliary_number_numerator": summary["particle_number_numerator"],
        "number_matches": direct_number == summary["particle_number_numerator"],
        "average_sign": summary["average_sign"],
        "particle_number_expectation": summary["particle_number_expectation"],
    }

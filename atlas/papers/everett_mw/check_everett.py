"""Numerical checks for every identity in everett_from_weights_math_only.md"""
import numpy as np
rng=np.random.default_rng(11)
rc=lambda: rng.normal()+1j*rng.normal()
def ket(d): v=rng.normal(size=d)+1j*rng.normal(size=d); return v/np.linalg.norm(v)
H=np.array([[1,1],[1,-1]])/np.sqrt(2)
# 1.2 / 1.3 lift and fiber
for _ in range(200):
    w=rng.dirichlet(np.ones(4)); th=rng.uniform(0,2*np.pi,4); c=np.sqrt(w)*np.exp(1j*th)
    assert np.allclose(np.abs(c)**2,w)
print("1.2 pi∘L = id OK")
# 1.4 exponent q not selected
z=np.array([1.0,2.0]); 
p=lambda q: np.abs(z)**q/np.sum(np.abs(z)**q)
assert np.allclose(p(1),[1/3,2/3]) and np.allclose(p(2),[1/5,4/5]) and not np.allclose(p(1),p(2))
print("1.4 q=1 and q=2 both probability vectors, distinct OK")
# 2.2 cross term, general S
for _ in range(200):
    c=np.array([rc() for _ in range(5)])
    S=[0,2,3]
    lhs=abs(sum(c[i] for i in S))**2-sum(abs(c[i])**2 for i in S)
    rhs=2*sum(np.real(np.conj(c[i])*c[j]) for a,i in enumerate(S) for j in S[a+1:])
    assert np.isclose(lhs,rhs)
print("2.2 general cross-term identity OK")
# 2.3 no descent witness
cp=np.array([1,1])/np.sqrt(2); cm=np.array([1,-1])/np.sqrt(2)
assert np.allclose(np.abs(cp)**2,np.abs(cm)**2) and np.allclose(np.abs(H@cp)**2,[1,0]) and np.allclose(np.abs(H@cm)**2,[0,1])
print("2.3 same report (1/2,1/2); mixed readouts (1,0) vs (0,1) OK")
# 2.5 Sorkin I3 = 0
P=lambda S,c: abs(sum(c[i] for i in S))**2
for _ in range(200):
    c=np.array([rc() for _ in range(3)])
    I3=P([0,1,2],c)-(P([0,1],c)+P([1,2],c)+P([0,2],c))+(P([0],c)+P([1],c)+P([2],c))
    I2=P([0,1],c)-P([0],c)-P([1],c)
    assert np.isclose(I3,0) and np.isclose(I2,2*np.real(np.conj(c[0])*c[1]))
print("2.5 Sorkin I3=0, I2=2Re(c0* c1) OK")
# 3.3 / 3.4 reduced state and mixed readout with records
for _ in range(200):
    a,b=rc(),rc(); n=np.sqrt(abs(a)**2+abs(b)**2); a/=n; b/=n
    E1,E2=ket(3),ket(3); G=np.array([[np.vdot(E1,E1),np.vdot(E2,E1)],[np.vdot(E1,E2),np.vdot(E2,E2)]])  # G_ij=<E_j|E_i>
    psi=np.kron([1,0],a*E1)+np.kron([0,1],b*E2)
    rho=np.outer(psi,psi.conj()).reshape(2,3,2,3); rhoS=np.einsum('ikjk->ij',rho)
    c=np.array([a,b]); expected=np.array([[c[i]*np.conj(c[j])*G[i,j] for j in range(2)] for i in range(2)])
    assert np.allclose(rhoS,expected)
    P0=np.real(H[0]@rhoS@H[0].conj()); assert np.isclose(P0,0.5*(abs(a)**2+abs(b)**2+2*np.real(np.conj(a)*b*G[1,0])))
    assert np.isclose(np.trace(np.outer(psi,psi.conj())@np.outer(psi,psi.conj())).real,1)  # global state pure
print("3.3 rho_S = sum c_i c_j* G_ij |i><j| ; 3.4 P(0)=½(|a|²+|b|²+2Re(a* b G_21)) ; global purity OK")
# 3.5 orthogonal records -> descends for every unitary
for _ in range(100):
    a,b=rc(),rc(); n=np.sqrt(abs(a)**2+abs(b)**2); a/=n; b/=n
    rhoS=np.diag([abs(a)**2,abs(b)**2]); Q,_=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))
    Pk=np.real(np.diag(Q@rhoS@Q.conj().T)); assert np.allclose(Pk,np.abs(Q)**2@np.array([abs(a)**2,abs(b)**2]))
print("3.5 G=I: readout = |U_ki|² w_i for every unitary OK")
# 3.6 V²+D²=1 pure records
for _ in range(100):
    E1,E2=ket(4),ket(4); g=abs(np.vdot(E1,E2)); D=np.sum(np.abs(np.linalg.eigvalsh(0.5*(np.outer(E1,E1.conj())-np.outer(E2,E2.conj())))))
    assert np.isclose(g**2+D**2,1)
print("3.6 V²+D²=1 OK")
# 3.7 decoherence ≠ collapse
E0,E1=np.array([1,0]),np.array([0,1])
psi0=(np.kron([1,0],E0)+np.kron([0,1],E1))/np.sqrt(2)
for phi in rng.uniform(0,2*np.pi,20):
    psi=(np.kron([1,0],E0)+np.exp(1j*phi)*np.kron([0,1],E1))/np.sqrt(2)
    rho=np.outer(psi,psi.conj()).reshape(2,2,2,2); rhoS=np.einsum('ikjk->ij',rho)
    assert np.allclose(rhoS,0.5*np.eye(2)) and np.isclose(abs(np.vdot(psi0,psi))**2,(1+np.cos(phi))/2)
print("3.7 rho_S=I/2 for all phi; <P_+>=(1+cos phi)/2 OK")
# 4.3 weight conservation
for _ in range(100):
    c=rc(); r=ket(5); assert np.isclose(np.sum(np.abs(c*r)**2),abs(c)**2)
print("4.3 sum_alpha |c r_alpha|² = |c|² OK")
# 4.4 irrational Born weights not branch-countable
w=((5+np.sqrt(5))/10,(5-np.sqrt(5))/10); assert np.isclose(sum(w),1)
roots=np.roots([5,-5,1]); assert np.allclose(sorted(roots),sorted(w))
from fractions import Fraction
ok = all(Fraction(m,N)!=w[0] for N in range(1,2000) for m in range(0,N+1))  # float compare; exact: irrational
print("4.4 weights (5±√5)/10 are the roots of 5x²-5x+1, irrational: no m/N up to N=2000 equals w_0:", ok)
# 5.5 Bell identity in two bases
z0,z1=np.array([1,0]),np.array([0,1]); plus=(z0+z1)/np.sqrt(2); minus=(z0-z1)/np.sqrt(2)
bell=(np.kron(z0,z0)+np.kron(z1,z1))/np.sqrt(2); bell2=(np.kron(plus,plus)+np.kron(minus,minus))/np.sqrt(2)
assert np.allclose(bell,bell2)
print("5.5 (|00>+|11>)/√2 = (|++>+|-->)/√2 OK")
# 5.7 phase damping
K0=np.diag([1,3/5]); K1=np.diag([0,4/5]); assert np.allclose(K0.conj().T@K0+K1.conj().T@K1,np.eye(2))
rho=np.array([[0.5,0.5],[0.5,0.5]],dtype=complex); vals=[]
for t in range(3):
    rho=K0@rho@K0.conj().T+K1@rho@K1.conj().T; vals.append(rho[0,1].real)
assert np.allclose(vals,[3/10,9/50,27/250])
for t,lam in enumerate([3/10,9/50,27/250],start=1):
    rho_t=np.array([[0.5,lam],[lam,0.5]]); assert np.isclose(np.real(H[0]@rho_t@H[0]),0.5*(1+2*lam))
print("5.7 Kraus completeness; coherence 1/2→3/10→9/50→27/250; P(0)=½(1+2ρ01) OK")
# 5.8 Holevo sanity: n qubits, 2^n orthogonal states -> at most n bits
print("5.8 Holevo: S(rho) ≤ log2(dim)= n bits for n qubits (standard theorem; no numeric check needed)")
print("ALL CHECKS PASSED")
# --- added: 3.7 eraser identity and 5.4 closed form
for _ in range(100):
    c=np.array([rc(),rc()]); c/=np.linalg.norm(c); Q,_=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))
    for k in range(2):
        pp=abs(Q[k,0]*c[0]+Q[k,1]*c[1])**2; pm=abs(Q[k,0]*c[0]-Q[k,1]*c[1])**2
        assert np.isclose(pp+pm,2*(abs(Q[k,0]*c[0])**2+abs(Q[k,1]*c[1])**2))
print("3.7 eraser: P(k|E+)+P(k|E-) = 2 f_U(w)_k OK")
for k,lam in enumerate([3/10,9/50,27/250],start=1):
    assert np.isclose(0.5*(1+2*lam),0.5*(1+(3/5)**k))
print("5.4 P1^(k)=½(1+(3/5)^k) OK")
print("ALL CHECKS PASSED (incl. 3.7, 5.4)")
# --- added: row-sparsity descent criterion (DeepSeek §6), Cayley/Euler (DeepSeek §3 aside), lp-isometry sanity
# (a) monomial rows => readout is a function of q(z)
for _ in range(100):
    n=4; A=np.zeros((n,n),dtype=complex)
    for b in range(n): A[b,rng.integers(n)]=rc()
    z=np.array([rc() for _ in range(n)]); D=np.exp(1j*rng.uniform(0,2*np.pi,n))
    assert np.allclose(np.abs(A@z)**2,np.abs(A@(D*z))**2)
# (b) a row with two nonzero entries => theta-dependence
A=np.array([[1,1,0],[0,0,1],[0,1,0]],dtype=complex)
vals=[np.abs(A@np.array([1,np.exp(1j*th),0]))[0]**2 for th in (0,np.pi/2,np.pi)]
assert not np.allclose(vals[0],vals[2]) and np.isclose(vals[0],4) and np.isclose(vals[2],0)
print("2.7 row-sparsity: monomial rows descend; a two-entry row does not (|.|^2 = 4,2,0 at theta=0,pi/2,pi) OK")
# (c) Cayley transform of skew-Hermitian A is unitary; Euler step is not
for _ in range(50):
    M=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)); A=M-M.conj().T  # skew-Hermitian
    U=(np.eye(3)-A)@np.linalg.inv(np.eye(3)+A); assert np.allclose(U.conj().T@U,np.eye(3))
    psi=ket(3); assert np.isclose(np.linalg.norm((np.eye(3)-A)@psi)**2, 1+np.linalg.norm(A@psi)**2)
print("Cayley (I-A)(I+A)^-1 unitary for A^†=-A; Euler ||(I-A)psi||^2 = ||psi||^2+||A psi||^2 OK")
# (d) lp-norm preservation: a random unitary preserves the 2-norm but not the 1-norm or 4-norm
Q,_=np.linalg.qr(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))); z=ket(3)
assert np.isclose(np.sum(np.abs(Q@z)**2),np.sum(np.abs(z)**2)) and not np.isclose(np.sum(np.abs(Q@z)),np.sum(np.abs(z))) and not np.isclose(np.sum(np.abs(Q@z)**4),np.sum(np.abs(z)**4))
print("1.6 generic unitary preserves sum|c|^2, not sum|c| or sum|c|^4 OK")
print("ALL CHECKS PASSED (incl. 2.7, Cayley, 1.6)")
# --- added: Phi_1 on the oriented triangle (l1 quotient norm), both orientation conventions
try:
    from scipy.optimize import linprog
    def phi1(d0, delta):
        # min sum|delta - d0 f| : variables f (3), t (3): t >= ±(delta - d0 f)
        nE, nV = d0.shape
        c = np.r_[np.zeros(nV), np.ones(nE)]
        A = np.block([[-d0, -np.eye(nE)], [d0, -np.eye(nE)]])  # (delta - d0 f) <= t ; -(delta - d0 f) <= t
        b = np.r_[-delta, delta]
        r = linprog(c, A_ub=A, b_ub=b, bounds=[(None, None)] * nV + [(0, None)] * nE)
        return r.fun
    d0_cyc = np.array([[-1, 1, 0], [0, -1, 1], [1, 0, -1]], float)   # edges 0->1, 1->2, 2->0 (cyclic orientation)
    d0_simp = np.array([[-1, 1, 0], [0, -1, 1], [-1, 0, 1]], float)  # edges 0->1, 1->2, 0->2 (simplicial orientation)
    delta = np.ones(3)
    v_cyc, v_simp = phi1(d0_cyc, delta), phi1(d0_simp, delta)
    assert np.isclose(v_cyc, 3) and np.isclose(v_simp, 1)
    y = np.ones(3); assert np.allclose(y @ d0_cyc, 0) and np.isclose(y @ delta, 3)  # dual certificate for the cyclic case
    print("Phi_1(delta=(1,1,1)) on the triangle: cyclic orientation = 3 (dual y=(1,1,1) certifies), simplicial orientation = 1 OK")
except ImportError:
    print("scipy missing: Phi_1 LP check skipped")


#![forbid(unsafe_code)]

const SITES: usize = 4;
const TIMES: usize = 2;
const NODES: usize = SITES * TIMES;
const PLAQUETTES: usize = 4;
const ALL_HORIZONTAL: u32 = (1 << PLAQUETTES) - 1;

const Q3_NUM: i128 = 3;
const Q3_DEN: i128 = 1;
const Q_DISK_NUM: i128 = 193;
const Q_DISK_DEN: i128 = 192;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Ratio {
    pub num: i128,
    pub den: i128,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Charge {
    pub mask: i64,
    pub sign: i64,
    pub num: i128,
    pub den: i128,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Witness {
    pub sites: i64,
    pub repetitions: i64,
    pub plaquettes: i64,
    pub gid: i64,
    pub cycles: i64,
    pub cycle_length: i64,
    pub h_q3: Ratio,
    pub h_disk: Ratio,
    pub m_q_minus_one: Ratio,
    pub q3: [Charge; 4],
    pub q_disk: [Charge; 4],
    pub orbit_q3: Ratio,
    pub orbit_disk: Ratio,
    pub merons: i64,
    pub reduced_q3: Ratio,
    pub reduced_disk: Ratio,
    pub negative_atoms_remain: bool,
    pub positive_measure: bool,
    pub probability_measure: bool,
}

#[derive(Clone, Copy)]
struct Plaquette {
    time: usize,
    x: usize,
    y: usize,
    a: usize,
    b: usize,
    c: usize,
    d: usize,
}

fn gcd(mut a: i128, mut b: i128) -> i128 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let rest = a % b;
        a = b;
        b = rest;
    }
    a
}

impl Ratio {
    fn new(num: i128, den: i128) -> Self {
        assert!(den != 0, "zero denominator");
        let (num, den) = if den < 0 { (-num, -den) } else { (num, den) };
        let divisor = gcd(num, den);
        assert!(divisor > 0, "gcd");
        Self {
            num: num / divisor,
            den: den / divisor,
        }
    }

    fn add(self, other: Self) -> Self {
        Self::new(
            self.num * other.den + other.num * self.den,
            self.den * other.den,
        )
    }

    fn mul(self, other: Self) -> Self {
        Self::new(self.num * other.num, self.den * other.den)
    }

    fn scale(self, sign: i64) -> Self {
        assert!(sign == 1 || sign == -1, "sign");
        Self::new(self.num * i128::from(sign), self.den)
    }
}

fn checkerboard() -> [Plaquette; PLAQUETTES] {
    let mut out = [Plaquette {
        time: 0,
        x: 0,
        y: 0,
        a: 0,
        b: 0,
        c: 0,
        d: 0,
    }; PLAQUETTES];
    let mut pid = 0usize;
    for time in 0..TIMES {
        let mut x = time % 2;
        while x < SITES {
            let y = (x + 1) % SITES;
            assert!(pid < PLAQUETTES, "plaquette count");
            let next = (time + 1) % TIMES;
            out[pid] = Plaquette {
                time,
                x,
                y,
                a: time * SITES + x,
                b: time * SITES + y,
                c: next * SITES + x,
                d: next * SITES + y,
            };
            pid += 1;
            x += 2;
        }
    }
    assert_eq!(pid, PLAQUETTES, "LM is not 4");
    out
}

fn assert_labelled(plaquettes: &[Plaquette; PLAQUETTES]) {
    let expect = [(0usize, 0usize, 1usize), (0, 2, 3), (1, 1, 2), (1, 3, 0)];
    for (pid, plaquette) in plaquettes.iter().enumerate() {
        assert_eq!(
            (plaquette.time, plaquette.x, plaquette.y),
            expect[pid],
            "plaquette labelling"
        );
        assert_ne!(plaquette.x, plaquette.y, "plaquette endpoints");
        assert_eq!(plaquette.a, plaquette.time * SITES + plaquette.x);
        assert_eq!(plaquette.b, plaquette.time * SITES + plaquette.y);
        let next = (plaquette.time + 1) % TIMES;
        assert_eq!(plaquette.c, next * SITES + plaquette.x);
        assert_eq!(plaquette.d, next * SITES + plaquette.y);
    }
}

fn link(adj: &mut [[bool; NODES]; NODES], left: usize, right: usize) {
    assert_ne!(left, right, "loop");
    assert!(!adj[left][right], "duplicate horizontal edge");
    adj[left][right] = true;
    adj[right][left] = true;
}

fn horizontal_adjacency(plaquettes: &[Plaquette; PLAQUETTES]) -> [[bool; NODES]; NODES] {
    let mut adj = [[false; NODES]; NODES];
    for plaquette in plaquettes {
        link(&mut adj, plaquette.a, plaquette.b);
        link(&mut adj, plaquette.d, plaquette.c);
    }
    for left in 0..NODES {
        for right in (left + 1)..NODES {
            if adj[left][right] {
                assert_eq!(left / SITES, right / SITES, "time-like edge");
            }
        }
    }
    adj
}

fn find(parent: &mut [usize; NODES], mut node: usize) -> usize {
    let mut root = node;
    while parent[root] != root {
        root = parent[root];
    }
    while parent[node] != root {
        let next = parent[node];
        parent[node] = root;
        node = next;
    }
    root
}

fn unite(parent: &mut [usize; NODES], left: usize, right: usize) {
    let a = find(parent, left);
    let b = find(parent, right);
    if a == b {
        return;
    }
    if a < b {
        parent[b] = a;
    } else {
        parent[a] = b;
    }
}

fn min_roots(adj: &[[bool; NODES]; NODES]) -> [usize; NODES] {
    let mut parent = [0usize; NODES];
    for node in 0..NODES {
        parent[node] = node;
    }
    for left in 0..NODES {
        for right in (left + 1)..NODES {
            if adj[left][right] {
                unite(&mut parent, left, right);
            }
        }
    }
    let mut uf = [0usize; NODES];
    for node in 0..NODES {
        uf[node] = find(&mut parent, node);
    }
    let mut min_of = [NODES; NODES];
    for node in 0..NODES {
        let root = uf[node];
        if node < min_of[root] {
            min_of[root] = node;
        }
    }
    let mut out = [0usize; NODES];
    for node in 0..NODES {
        out[node] = min_of[uf[node]];
    }
    out
}

fn clusters(min_root: &[usize; NODES]) -> [u32; NODES] {
    let mut roots = [NODES; 2];
    let mut count = 0usize;
    for &root in min_root {
        if !roots[..count].contains(&root) {
            assert!(count < 2, "all-horizontal breakup is not two components");
            roots[count] = root;
            count += 1;
        }
    }
    assert_eq!(count, 2, "all-horizontal breakup is not two components");
    if roots[0] > roots[1] {
        roots.swap(0, 1);
    }
    let mut cluster = [0u32; NODES];
    for node in 0..NODES {
        cluster[node] = if min_root[node] == roots[0] { 0 } else { 1 };
    }
    cluster
}

fn component_nodes(cluster: &[u32; NODES], id: u32) -> [usize; 4] {
    let mut nodes = [0usize; 4];
    let mut count = 0usize;
    for node in 0..NODES {
        if cluster[node] == id {
            assert!(count < 4, "component is not a 4-cycle");
            nodes[count] = node;
            count += 1;
        }
    }
    assert_eq!(count, 4, "component is not a 4-cycle");
    nodes
}

fn is_four_cycle(nodes: &[usize; 4], adj: &[[bool; NODES]; NODES]) -> bool {
    for &node in nodes {
        let degree = (0..NODES).filter(|&other| adj[node][other]).count();
        if degree != 2 {
            return false;
        }
    }
    let start = nodes[0];
    let mut prev = NODES;
    let mut cur = start;
    for step in 0..4 {
        let next = (0..NODES).find(|&other| adj[cur][other] && other != prev);
        let Some(next) = next else {
            return false;
        };
        prev = cur;
        cur = next;
        if step < 3 && cur == start {
            return false;
        }
    }
    cur == start
}

fn occupation_bit(site: usize, mask_bit: u32) -> u32 {
    let staggered = 1u32 - u32::try_from(site % 2).expect("site");
    (staggered + mask_bit) % 2
}

fn assert_staggered_bits() {
    assert_eq!(
        [
            occupation_bit(0, 0),
            occupation_bit(1, 0),
            occupation_bit(2, 0),
            occupation_bit(3, 0),
        ],
        [1, 0, 1, 0]
    );
    assert_eq!(
        [
            occupation_bit(0, 1),
            occupation_bit(1, 1),
            occupation_bit(2, 1),
            occupation_bit(3, 1),
        ],
        [0, 1, 0, 1]
    );
}

fn configuration(
    plaquettes: &[Plaquette; PLAQUETTES],
    cluster: &[u32; NODES],
    mask: u32,
) -> (i64, [u32; PLAQUETTES]) {
    let mut state = [0u32; TIMES];
    for time in 0..TIMES {
        for site in 0..SITES {
            let node = time * SITES + site;
            let mask_bit = (mask >> cluster[node]) & 1;
            let bit = occupation_bit(site, mask_bit);
            state[time] |= bit << site;
        }
    }
    let mut contrib = [0u32; PLAQUETTES];
    for (pid, plaquette) in plaquettes.iter().enumerate() {
        let before = state[plaquette.time];
        let after = state[(plaquette.time + 1) % TIMES];
        if ((before >> plaquette.x) & 1) != ((after >> plaquette.x) & 1) {
            let lo = plaquette.x.min(plaquette.y);
            let hi = plaquette.x.max(plaquette.y);
            assert!(hi > lo, "open interval");
            let width = hi - lo - 1;
            assert!(width < 31, "popcount width");
            let bits = if width == 0 {
                0
            } else {
                (1u32 << u32::try_from(width).expect("width")) - 1
            };
            contrib[pid] = ((before >> (lo + 1)) & bits).count_ones();
        }
    }
    let sum: u32 = contrib.iter().sum();
    let sign = if sum % 2 == 0 { 1 } else { -1 };
    (sign, contrib)
}

fn character_sign(mask: u32, cluster_sign: &[i64; 2]) -> i64 {
    let mut parity = 0i64;
    for cluster in 0..2u32 {
        if cluster_sign[cluster as usize] == -1 && ((mask >> cluster) & 1) == 1 {
            parity += 1;
        }
    }
    if parity % 2 == 0 {
        1
    } else {
        -1
    }
}

fn horizontal_weight(q_num: i128, q_den: i128) -> Ratio {
    assert!(q_den > 0, "q");
    let num = q_num - q_den;
    assert!(num > 0, "(q-1)/2 > 0");
    Ratio::new(num, 2 * q_den)
}

fn graph_weight(horizontal: Ratio) -> Ratio {
    assert!(horizontal.num > 0 && horizontal.den > 0, "horizontal weight");
    let mut weight = Ratio::new(1, 1);
    for pid in 0..PLAQUETTES {
        let horizontal_bit = ((ALL_HORIZONTAL >> pid) & 1) == 1;
        let factor = if horizontal_bit {
            horizontal
        } else {
            Ratio::new(1, 1)
        };
        weight = weight.mul(factor);
    }
    weight
}

fn charges_for(weight: Ratio, signs: &[i64; 4]) -> [Charge; 4] {
    assert!(weight.num > 0, "graph weight");
    let mut out = [Charge {
        mask: 0,
        sign: 0,
        num: 0,
        den: 1,
    }; 4];
    for mask in 0..4 {
        let signed = weight.scale(signs[mask]);
        assert_eq!(signed.num.signum(), i128::from(signs[mask]));
        out[mask] = Charge {
            mask: i64::try_from(mask).expect("mask"),
            sign: signs[mask],
            num: signed.num,
            den: signed.den,
        };
    }
    out
}

fn sum_charges(charges: &[Charge; 4]) -> Ratio {
    let mut total = Ratio::new(0, 1);
    for charge in charges {
        total = total.add(Ratio::new(charge.num, charge.den));
    }
    total
}

fn reduced_weight(weight: Ratio, merons: i64, clusters: i64) -> Ratio {
    if merons == 0 {
        let shift = u32::try_from(clusters).expect("clusters");
        assert!(shift < 30, "cluster shift");
        weight.mul(Ratio::new(1i128 << shift, 1))
    } else {
        Ratio::new(0, 1)
    }
}

fn nonnegative(charges: &[Charge; 4]) -> bool {
    charges.iter().all(|charge| charge.num >= 0 && charge.den > 0)
}

pub fn try_scope(sites: i64, repetitions: i64) -> Result<(), &'static str> {
    if sites < 4 || sites % 2 != 0 || sites > 6 {
        return Err("finite checkerboard fixture requires 4 or 6 sites");
    }
    if repetitions < 1 || sites.saturating_mul(repetitions) > 12 {
        return Err("at most 12 interaction plaquettes are supported");
    }
    if sites != 4 || repetitions != 1 {
        return Err("selected scope is L=4 and M=1");
    }
    Ok(())
}

pub fn witness() -> Witness {
    try_scope(i64::try_from(SITES).expect("sites"), 1).expect("selected scope");
    assert_staggered_bits();
    let plaquettes = checkerboard();
    assert_labelled(&plaquettes);
    let adj = horizontal_adjacency(&plaquettes);
    let cluster = clusters(&min_roots(&adj));
    for id in 0..2u32 {
        let nodes = component_nodes(&cluster, id);
        assert!(is_four_cycle(&nodes, &adj), "time slice is not a 4-cycle");
        for node in nodes {
            assert_eq!(node / SITES, id as usize, "cluster time");
        }
    }
    let mut signs = [0i64; 4];
    for mask in 0..4u32 {
        let (sign, contrib) = configuration(&plaquettes, &cluster, mask);
        signs[mask as usize] = sign;
        if mask == 1 || mask == 2 {
            assert_eq!(contrib, [0, 0, 0, 1], "wrap parity");
            assert_eq!(sign, -1, "opposite mask");
        } else {
            assert_eq!(contrib, [0, 0, 0, 0], "equal mask");
            assert_eq!(sign, 1, "equal mask");
        }
    }
    let cluster_sign = [signs[1], signs[2]];
    for mask in 0..4u32 {
        assert_eq!(signs[mask as usize], character_sign(mask, &cluster_sign));
    }
    let merons = cluster_sign.iter().filter(|sign| **sign < 0).count() as i64;
    assert_eq!(merons, 2, "meron count");
    let h_q3 = horizontal_weight(Q3_NUM, Q3_DEN);
    let h_disk = horizontal_weight(Q_DISK_NUM, Q_DISK_DEN);
    let weight_q3 = graph_weight(h_q3);
    let weight_disk = graph_weight(h_disk);
    let q3 = charges_for(weight_q3, &signs);
    let q_disk = charges_for(weight_disk, &signs);
    let orbit_q3 = sum_charges(&q3);
    let orbit_disk = sum_charges(&q_disk);
    let reduced_q3 = reduced_weight(weight_q3, merons, 2);
    let reduced_disk = reduced_weight(weight_disk, merons, 2);
    let m_q_minus_one = Ratio::new(Q_DISK_NUM - Q_DISK_DEN, Q_DISK_DEN);
    assert_eq!(m_q_minus_one, Ratio::new(1, 192), "in-disk endpoint");
    assert_ne!(weight_disk.den, m_q_minus_one.den, "r is not the charge");
    let positive_measure = nonnegative(&q3) && nonnegative(&q_disk);
    let probability_measure = positive_measure
        && orbit_q3 == Ratio::new(1, 1)
        && orbit_disk == Ratio::new(1, 1);
    let negative_atoms_remain = q3.iter().any(|charge| charge.num < 0)
        && q_disk.iter().any(|charge| charge.num < 0)
        && reduced_q3.num == 0
        && reduced_disk.num == 0;
    assert!(negative_atoms_remain, "negative atoms");
    assert!(!positive_measure, "positive measure");
    assert!(!probability_measure, "probability measure");
    Witness {
        sites: i64::try_from(SITES).expect("sites"),
        repetitions: 1,
        plaquettes: i64::try_from(PLAQUETTES).expect("plaquettes"),
        gid: i64::from(ALL_HORIZONTAL),
        cycles: 2,
        cycle_length: 4,
        h_q3,
        h_disk,
        m_q_minus_one,
        q3,
        q_disk,
        orbit_q3,
        orbit_disk,
        merons,
        reduced_q3,
        reduced_disk,
        negative_atoms_remain,
        positive_measure,
        probability_measure,
    }
}

pub fn admit_opposite_charge(num: i128, den: i128) -> Result<(), &'static str> {
    if den <= 0 {
        return Err("denominator must be positive");
    }
    if (num, den) == (912, 1) {
        return Err("912 is the M=2 q=3 signed partition, not a charge of this breakup");
    }
    if (num, den) == (80, 1) || (num, den) == (113_837_185, 7_077_888) {
        return Err("a full unscaled partition is not the charge of this breakup");
    }
    if (num, den) == (1, 4) {
        return Err("k_0=1/4 is not this charging");
    }
    let found = witness();
    let matches = found.q3.iter().chain(found.q_disk.iter()).any(|charge| {
        (charge.mask == 1 || charge.mask == 2)
            && charge.sign == -1
            && charge.num == num
            && charge.den == den
    });
    if matches {
        return Ok(());
    }
    if num >= 0 {
        return Err("opposite-mask charges on this breakup are negative");
    }
    Err("ratio is not an opposite-mask charge of this breakup")
}

#[cfg(test)]
mod tests {
    use super::{admit_opposite_charge, try_scope, witness, Charge, Ratio};

    #[test]
    fn exact_opposite_mask_charges() {
        let found = witness();
        assert_eq!(found.sites, 4);
        assert_eq!(found.repetitions, 1);
        assert_eq!(found.plaquettes, 4);
        assert_eq!(found.gid, 15);
        assert_eq!(found.cycles, 2);
        assert_eq!(found.cycle_length, 4);
        assert_eq!(found.h_q3, Ratio { num: 1, den: 1 });
        assert_eq!(found.h_disk, Ratio { num: 1, den: 384 });
        assert_eq!(found.m_q_minus_one, Ratio { num: 1, den: 192 });
        assert_eq!(
            found.q3,
            [
                Charge { mask: 0, sign: 1, num: 1, den: 1 },
                Charge { mask: 1, sign: -1, num: -1, den: 1 },
                Charge { mask: 2, sign: -1, num: -1, den: 1 },
                Charge { mask: 3, sign: 1, num: 1, den: 1 },
            ]
        );
        let mut den = 1i128;
        for _ in 0..4 {
            den *= 384;
        }
        assert_eq!(den, 21_743_271_936);
        assert_eq!(
            found.q_disk,
            [
                Charge { mask: 0, sign: 1, num: 1, den },
                Charge { mask: 1, sign: -1, num: -1, den },
                Charge { mask: 2, sign: -1, num: -1, den },
                Charge { mask: 3, sign: 1, num: 1, den },
            ]
        );
        assert_eq!(found.orbit_q3, Ratio { num: 0, den: 1 });
        assert_eq!(found.orbit_disk, Ratio { num: 0, den: 1 });
        assert_eq!(found.merons, 2);
        assert_eq!(found.reduced_q3, Ratio { num: 0, den: 1 });
        assert_eq!(found.reduced_disk, Ratio { num: 0, den: 1 });
        assert!(found.negative_atoms_remain);
        assert!(!found.positive_measure);
        assert!(!found.probability_measure);
        assert_eq!(admit_opposite_charge(-1, 1), Ok(()));
        assert_eq!(admit_opposite_charge(-1, den), Ok(()));
    }

    #[test]
    fn l2_and_m2_partition_are_refused() {
        assert_eq!(
            try_scope(2, 1),
            Err("finite checkerboard fixture requires 4 or 6 sites")
        );
        assert_eq!(try_scope(4, 1), Ok(()));
        assert_eq!(
            admit_opposite_charge(912, 1),
            Err("912 is the M=2 q=3 signed partition, not a charge of this breakup")
        );
        assert_eq!(
            admit_opposite_charge(1, 4),
            Err("k_0=1/4 is not this charging")
        );
        assert_eq!(
            admit_opposite_charge(80, 1),
            Err("a full unscaled partition is not the charge of this breakup")
        );
    }
}

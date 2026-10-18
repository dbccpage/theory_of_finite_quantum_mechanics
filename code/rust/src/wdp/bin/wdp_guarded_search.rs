use omega_wdp::genesis_guarded_history::{
    admit_problem, guarded_certificate, kind_compatible, kind_sorted_order, legal_extensions,
    respects, CausalProblem, GuardedHistoryError, Json, StarCoherence, SwapComplex,
    MAX_H1_COMPONENT,
};
use std::collections::{BTreeMap, BTreeSet};
use std::process::ExitCode;
use std::time::Instant;

#[derive(Clone, Copy)]
struct Letter {
    tag: &'static str,
    kind: &'static str,
    relation: Option<&'static str>,
    tokens: &'static [&'static str],
    birth: bool,
    cap: usize,
    key: Option<(usize, usize)>,
}

struct Tier {
    name: &'static str,
    tokens: &'static [&'static str],
    keys: &'static [(usize, usize)],
    letters: Vec<Letter>,
    min_events: usize,
    max_events: usize,
    births: bool,
    merges: bool,
    edges: (usize, usize),
}

const fn letter(
    tag: &'static str,
    kind: &'static str,
    relation: Option<&'static str>,
    tokens: &'static [&'static str],
    cap: usize,
    key: Option<(usize, usize)>,
) -> Letter {
    Letter {
        tag,
        kind,
        relation,
        tokens,
        birth: false,
        cap,
        key,
    }
}

fn tiers(max_events: usize, selected: &str) -> Vec<Tier> {
    const U0: &[&str] = &["u0"];
    const U01: &[&str] = &["u0", "u1"];
    const U012: &[&str] = &["u0", "u1", "u2"];
    const R00: &[&str] = &["u0", "u0"];
    const R01: &[&str] = &["u0", "u1"];
    const R12: &[&str] = &["u1", "u2"];
    const R02: &[&str] = &["u0", "u2"];
    const F012: &[&str] = &["u0", "u1", "u2"];
    const F021: &[&str] = &["u0", "u2", "u1"];
    const BB: &[&str] = &["b", "b"];
    const U0B: &[&str] = &["u0", "b"];
    let many = usize::MAX;
    let all = vec![
        Tier {
            name: "A",
            tokens: U0,
            keys: &[(0, 0), (1, 0)],
            letters: vec![
                letter("ar", "add_assertion", Some("r"), R00, many, None),
                letter("xr", "remove", Some("r"), R00, many, Some((0, 0))),
                letter("as", "add_assertion", Some("s"), R00, many, None),
                letter("xs", "remove", Some("s"), R00, many, Some((1, 0))),
            ],
            min_events: 3,
            max_events: 6,
            births: false,
            merges: false,
            edges: (0, 2),
        },
        Tier {
            name: "B",
            tokens: U01,
            keys: &[(0, 1), (0, 0)],
            letters: vec![
                letter("a01", "add_assertion", Some("r"), R01, many, None),
                letter("x01", "remove", Some("r"), R01, many, Some((0, 1))),
                letter("a00", "add_assertion", Some("r"), R00, many, None),
                letter("x00", "remove", Some("r"), R00, many, Some((0, 0))),
                letter("i01", "identify", None, R01, 1, None),
            ],
            min_events: 3,
            max_events,
            births: false,
            merges: true,
            edges: (0, 2),
        },
        Tier {
            name: "C",
            tokens: U012,
            keys: &[(0, 1)],
            letters: vec![
                letter("a01", "add_assertion", Some("r"), R01, many, None),
                letter("x01", "remove", Some("r"), R01, many, Some((0, 1))),
                letter("i01", "identify", None, R01, 1, None),
                letter("i12", "identify", None, R12, 1, None),
                letter("i02", "identify", None, R02, 1, None),
                letter("f012", "fill", None, F012, 1, None),
                letter("f021", "fill", None, F021, 1, None),
            ],
            min_events: 3,
            max_events,
            births: false,
            merges: true,
            edges: (0, 2),
        },
        Tier {
            name: "D",
            tokens: U0,
            keys: &[(0, 0)],
            letters: vec![
                Letter {
                    tag: "tb",
                    kind: "add_term",
                    relation: None,
                    tokens: &[],
                    birth: true,
                    cap: 1,
                    key: None,
                },
                letter("ib", "identify", None, U0B, 1, None),
                letter("abb", "add_assertion", Some("r"), BB, many, None),
                letter("xbb", "remove", Some("r"), BB, many, None),
                letter("ar", "add_assertion", Some("r"), R00, many, None),
                letter("xr", "remove", Some("r"), R00, many, Some((0, 0))),
            ],
            min_events: 3,
            max_events: 6,
            births: true,
            merges: true,
            edges: (0, 2),
        },
        Tier {
            name: "E",
            tokens: U0,
            keys: &[(0, 0)],
            letters: vec![
                letter("ar", "add_assertion", Some("r"), R00, many, None),
                letter("xr", "remove", Some("r"), R00, many, Some((0, 0))),
            ],
            min_events: 4,
            max_events: 6,
            births: false,
            merges: false,
            edges: (3, 3),
        },
    ];
    all.into_iter()
        .filter(|t| selected.contains(t.name))
        .collect()
}

fn multisets(letters: &[Letter], size: usize) -> Vec<Vec<usize>> {
    fn go(
        letters: &[Letter],
        from: usize,
        left: usize,
        cur: &mut Vec<usize>,
        out: &mut Vec<Vec<usize>>,
    ) {
        if left == 0 {
            out.push(cur.clone());
            return;
        }
        for l in from..letters.len() {
            let used = cur.iter().filter(|&&x| x == l).count();
            if used < letters[l].cap {
                cur.push(l);
                go(letters, l, left - 1, cur, out);
                cur.pop();
            }
        }
    }
    let mut out = Vec::new();
    go(letters, 0, size, &mut Vec::new(), &mut out);
    out
}

fn uses_birth(l: &Letter) -> bool {
    l.tokens.contains(&"b")
}

fn count_tables(tier: &Tier, multiset: &[usize]) -> Vec<Vec<usize>> {
    let removals: Vec<&Letter> = multiset
        .iter()
        .map(|&l| &tier.letters[l])
        .filter(|l| l.kind == "remove")
        .collect();
    let identifies = multiset.iter().any(|&l| tier.letters[l].kind == "identify");
    let caps: Vec<usize> = tier
        .keys
        .iter()
        .map(|&key| {
            let readers = if tier.merges && identifies {
                removals.len()
            } else {
                removals.iter().filter(|l| l.key == Some(key)).count()
            };
            readers.min(2)
        })
        .collect();
    let mut out = vec![vec![]];
    for cap in caps {
        out = out
            .into_iter()
            .flat_map(|prefix: Vec<usize>| {
                (0..=cap).map(move |c| {
                    let mut next = prefix.clone();
                    next.push(c);
                    next
                })
            })
            .collect();
    }
    out
}

fn problem_json(
    tier: &Tier,
    multiset: &[usize],
    counts: &[usize],
    extra: &[(usize, usize)],
) -> Json {
    let n = tier.tokens.len();
    let mut tables = vec![vec!["0".to_string(); n * n]; 2];
    for (&(table, entry), &c) in tier.keys.iter().zip(counts) {
        tables[table][entry] = c.to_string();
    }
    let tags: Vec<String> = multiset
        .iter()
        .enumerate()
        .map(|(e, &l)| format!("{}{}", tier.letters[l].tag, e))
        .collect();
    let birth_event = multiset.iter().position(|&l| tier.letters[l].birth);
    let events = multiset
        .iter()
        .enumerate()
        .map(|(e, &l)| {
            let spec = &tier.letters[l];
            let mut preds: BTreeSet<String> = extra
                .iter()
                .filter(|&&(_, b)| b == e)
                .map(|&(a, _)| tags[a].clone())
                .collect();
            if uses_birth(spec) {
                if let Some(b) = birth_event {
                    preds.insert(tags[b].clone());
                }
            }
            let mut fields = vec![
                ("tag", Json::text(tags[e].clone())),
                ("kind", Json::text(spec.kind)),
                (
                    "predecessors",
                    Json::Arr(preds.into_iter().map(Json::Str).collect()),
                ),
            ];
            if spec.birth {
                fields.push(("birth", Json::text("b")));
            } else {
                fields.push((
                    "tokens",
                    Json::Arr(spec.tokens.iter().map(|t| Json::text(*t)).collect()),
                ));
            }
            if let Some(r) = spec.relation {
                fields.push(("relation", Json::text(r)));
            }
            Json::object(fields)
        })
        .collect();
    Json::object([
        ("schema", Json::text("wdp-causal-problem-v1")),
        (
            "initial",
            Json::object([
                (
                    "terms",
                    Json::Arr((0..n).map(|i| Json::Str(format!("t{i}"))).collect()),
                ),
                (
                    "r",
                    Json::Arr(tables[0].iter().map(|c| Json::text(c.clone())).collect()),
                ),
                (
                    "s",
                    Json::Arr(tables[1].iter().map(|c| Json::text(c.clone())).collect()),
                ),
                ("filled", Json::Arr(vec![])),
            ]),
        ),
        (
            "initial_tokens",
            Json::Arr(tier.tokens.iter().map(|t| Json::text(*t)).collect()),
        ),
        ("events", Json::Arr(events)),
        (
            "protected_prices",
            Json::Arr(vec![
                Json::text("term_additions"),
                Json::text("assertion_additions"),
            ]),
        ),
    ])
}

fn combinations(
    pairs: &[(usize, usize)],
    size: usize,
    from: usize,
    current: &mut Vec<(usize, usize)>,
    out: &mut Vec<Vec<(usize, usize)>>,
) {
    if current.len() == size {
        out.push(current.clone());
        return;
    }
    for i in from..pairs.len() {
        current.push(pairs[i]);
        combinations(pairs, size, i + 1, current, out);
        current.pop();
    }
}

fn closure(masks: &mut [u32]) -> bool {
    let k = masks.len();
    for _ in 0..k {
        for e in 0..k {
            for p in 0..k {
                if masks[e] & (1 << p) != 0 {
                    masks[e] |= masks[p];
                }
            }
        }
    }
    masks.iter().enumerate().all(|(e, m)| m & (1 << e) == 0)
}

fn canonical_key(multiset: &[usize], masks: &[u32]) -> Vec<(u8, u8)> {
    let k = multiset.len();
    let pairs: Vec<(usize, usize)> = (0..k)
        .flat_map(|b| {
            (0..k)
                .filter(move |&a| masks[b] & (1 << a) != 0)
                .map(move |a| (a, b))
        })
        .collect();
    let mut groups: BTreeMap<usize, Vec<usize>> = BTreeMap::new();
    for (e, &l) in multiset.iter().enumerate() {
        groups.entry(l).or_default().push(e);
    }
    let groups: Vec<Vec<usize>> = groups.into_values().collect();
    let mut best: Option<Vec<(u8, u8)>> = None;
    let mut sigma: Vec<usize> = (0..k).collect();
    fn permute(
        groups: &[Vec<usize>],
        g: usize,
        sigma: &mut Vec<usize>,
        pairs: &[(usize, usize)],
        best: &mut Option<Vec<(u8, u8)>>,
    ) {
        if g == groups.len() {
            let mut mapped: Vec<(u8, u8)> = pairs
                .iter()
                .map(|&(a, b)| (sigma[a] as u8, sigma[b] as u8))
                .collect();
            mapped.sort_unstable();
            if best.as_ref().is_none_or(|b| mapped < *b) {
                *best = Some(mapped);
            }
            return;
        }
        let members = &groups[g];
        let mut images = members.clone();
        heap_permutations(&mut images, members.len(), &mut |perm| {
            for (src, dst) in members.iter().zip(perm) {
                sigma[*src] = *dst;
            }
            permute(groups, g + 1, sigma, pairs, best);
        });
    }
    permute(&groups, 0, &mut sigma, &pairs, &mut best);
    best.unwrap_or_default()
}

fn heap_permutations(items: &mut Vec<usize>, k: usize, visit: &mut dyn FnMut(&[usize])) {
    if k <= 1 {
        visit(items);
        return;
    }
    for i in 0..k {
        heap_permutations(items, k - 1, visit);
        if k.is_multiple_of(2) {
            items.swap(i, k - 1);
        } else {
            items.swap(0, k - 1);
        }
    }
}

#[derive(Default)]
struct Totals {
    families: usize,
    with_legal: usize,
    compatible: usize,
    compatible_with_legal: usize,
    corollary_failures: usize,
    theorem_failures: usize,
    noncompatible_two_legal: usize,
    noncompatible_star: usize,
    disconnected: usize,
    h1_positive: usize,
    witnesses_replayed: usize,
    witness_failures: usize,
}

impl Totals {
    fn add(&mut self, o: &Totals) {
        self.families += o.families;
        self.with_legal += o.with_legal;
        self.compatible += o.compatible;
        self.compatible_with_legal += o.compatible_with_legal;
        self.corollary_failures += o.corollary_failures;
        self.theorem_failures += o.theorem_failures;
        self.noncompatible_two_legal += o.noncompatible_two_legal;
        self.noncompatible_star += o.noncompatible_star;
        self.disconnected += o.disconnected;
        self.h1_positive += o.h1_positive;
        self.witnesses_replayed += o.witnesses_replayed;
        self.witness_failures += o.witness_failures;
    }

    fn line(&self, label: &str) -> String {
        format!(
            "{label}: families={} with_legal={} kind_compatible={} (with_legal={}) corollary_failures={} \
             theorem_failures={} noncompatible_ge2_legal={} noncompatible_with_star_base={} \
             disconnected={} h1_positive={} witnesses_replayed={} witness_failures={}",
            self.families,
            self.with_legal,
            self.compatible,
            self.compatible_with_legal,
            self.corollary_failures,
            self.theorem_failures,
            self.noncompatible_two_legal,
            self.noncompatible_star,
            self.disconnected,
            self.h1_positive,
            self.witnesses_replayed,
            self.witness_failures
        )
    }
}

struct Case {
    events: usize,
    legal: usize,
    text: String,
    note: String,
}

fn keep(cases: &mut Vec<Case>, case: Case, limit: usize) {
    cases.push(case);
    cases.sort_by(|a, b| (a.events, a.legal, &a.text).cmp(&(b.events, b.legal, &b.text)));
    cases.truncate(limit);
}

struct Findings {
    h1: Vec<Case>,
    disconnected: Vec<Case>,
    failures: Vec<Case>,
}

fn analyze(
    problem: &CausalProblem,
    legal: &BTreeSet<Vec<usize>>,
    text: &str,
    totals: &mut Totals,
    findings: &mut Findings,
) -> Result<(), GuardedHistoryError> {
    let k = problem.event_count();
    totals.families += 1;
    let compatible = kind_compatible(problem);
    totals.compatible += usize::from(compatible);
    if legal.is_empty() {
        return Ok(());
    }
    totals.with_legal += 1;
    totals.compatible_with_legal += usize::from(compatible);
    let sorted = kind_sorted_order(problem);
    let complex = SwapComplex::new(k, legal)?;
    let mut h1 = Vec::new();
    for c in 0..complex.components().len() {
        if complex.components()[c].len() > MAX_H1_COMPONENT {
            return Err(GuardedHistoryError::ComponentTooLarge {
                component: c,
                vertices: complex.components()[c].len(),
            });
        }
        h1.push(complex.reduce_component(c)?.h1_rank);
    }
    let star = complex.star_base(sorted.as_deref());
    let components = complex.components().len();
    let note = format!(
        "legal={} components={} h1={:?} edges={} squares={} hexagons={} kind_compatible={} star_base={:?}",
        legal.len(),
        components,
        h1,
        complex.edges().len(),
        complex.squares(),
        complex.hexagons(),
        compatible,
        star
    );
    let fail = |findings: &mut Findings, why: &str| {
        eprintln!("CROSS-CHECK FAILURE ({why}): {note}\nPROBLEM {text}");
        keep(
            &mut findings.failures,
            Case {
                events: k,
                legal: legal.len(),
                text: text.to_owned(),
                note: format!("{why}: {note}"),
            },
            20,
        );
    };
    if star.is_some() && (components != 1 || h1.iter().any(|&r| r > 0)) {
        totals.theorem_failures += 1;
        fail(findings, "star base but not connected and simply connected");
    }
    if compatible {
        let ok = sorted
            .as_deref()
            .is_some_and(|s| complex.lower_covers_closed(s));
        if !ok {
            totals.corollary_failures += 1;
            fail(
                findings,
                "kind compatible but kind-sorted order is not a star base",
            );
        }
    } else {
        totals.noncompatible_two_legal += usize::from(legal.len() >= 2);
        totals.noncompatible_star += usize::from(star.is_some());
    }
    if components >= 2 {
        totals.disconnected += 1;
        keep(
            &mut findings.disconnected,
            Case {
                events: k,
                legal: legal.len(),
                text: text.to_owned(),
                note: note.clone(),
            },
            3,
        );
    }
    if h1.iter().any(|&r| r > 0) {
        totals.h1_positive += 1;
        keep(
            &mut findings.h1,
            Case {
                events: k,
                legal: legal.len(),
                text: text.to_owned(),
                note: note.clone(),
            },
            5,
        );
    }
    if let Some(base) = &star {
        if legal.len() <= 120 && !complex.edges().is_empty() {
            let mut coherence = StarCoherence::new(&complex, base)?;
            let component = complex.component_of(coherence.base()).unwrap_or_default();
            for pair in complex.witness_pairs(component, 1)? {
                totals.witnesses_replayed += 1;
                if let Err(e) = coherence.witness(pair.source, &pair.first, &pair.second) {
                    totals.witness_failures += 1;
                    fail(findings, &format!("coherence witness refused: {e}"));
                }
            }
        }
    }
    Ok(())
}

fn run_tier(
    tier: &Tier,
    totals: &mut Totals,
    findings: &mut Findings,
) -> Result<(), GuardedHistoryError> {
    for size in tier.min_events..=tier.max_events {
        for multiset in multisets(&tier.letters, size) {
            let letters: Vec<&Letter> = multiset.iter().map(|&l| &tier.letters[l]).collect();
            let births = letters.iter().filter(|l| l.birth).count();
            let users = letters.iter().filter(|l| uses_birth(l)).count();
            if tier.births && (births != 1 || users == 0) {
                continue;
            }
            for counts in count_tables(tier, &multiset) {
                let base_json = problem_json(tier, &multiset, &counts, &[]);
                let base = admit_problem(&base_json)?;
                let base_legal = legal_extensions(&base)?;
                let k = multiset.len();
                let pairs: Vec<(usize, usize)> = (0..k)
                    .flat_map(|a| (0..k).filter(move |&b| b != a).map(move |b| (a, b)))
                    .collect();
                let mut edge_sets: Vec<Vec<(usize, usize)>> = Vec::new();
                for size in tier.edges.0..=tier.edges.1 {
                    combinations(&pairs, size, 0, &mut Vec::new(), &mut edge_sets);
                }
                let mut seen = BTreeSet::new();
                for extra in edge_sets {
                    let mut masks = base.before().to_vec();
                    for &(a, b) in &extra {
                        masks[b] |= 1 << a;
                    }
                    if !closure(&mut masks) || !seen.insert(canonical_key(&multiset, &masks)) {
                        continue;
                    }
                    let json = problem_json(tier, &multiset, &counts, &extra);
                    let problem = admit_problem(&json)?;
                    if problem.before() != masks.as_slice() {
                        return Err(GuardedHistoryError::Inconsistent(
                            "search closure differs from admission closure",
                        ));
                    }
                    let legal: BTreeSet<Vec<usize>> = base_legal
                        .iter()
                        .filter(|o| respects(problem.before(), o))
                        .cloned()
                        .collect();
                    analyze(&problem, &legal, &json.to_canonical(), totals, findings)?;
                }
            }
        }
    }
    Ok(())
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let mut max_events = 5usize;
    let mut selected = "ABCDE".to_string();
    let mut k = 0;
    while k < args.len() {
        match (args[k].as_str(), args.get(k + 1)) {
            ("--max-events", Some(v)) => match v.parse::<usize>() {
                Ok(n) if (3..=6).contains(&n) => max_events = n,
                _ => {
                    eprintln!("--max-events must be 3..=6");
                    return ExitCode::from(2);
                }
            },
            ("--tiers", Some(v)) => selected = v.clone(),
            _ => {
                eprintln!("usage: wdp_guarded_search [--max-events N] [--tiers ABCDE]");
                return ExitCode::from(2);
            }
        }
        k += 2;
    }
    let start = Instant::now();
    println!("wdp_guarded_search: AuthorityEffect None; bounded finite menu, not a proof");
    println!(
        "menu: tiers {selected}; tiers B,C at most {max_events} events; tiers A,D,E at most 6 \
         events; tiers A-D 0-2 extra edges, tier E exactly 3"
    );
    let mut grand = Totals::default();
    let mut findings = Findings {
        h1: vec![],
        disconnected: vec![],
        failures: vec![],
    };
    for tier in tiers(max_events, &selected) {
        let mut totals = Totals::default();
        let letters: Vec<String> = tier
            .letters
            .iter()
            .map(|l| format!("{}:{}{:?}", l.tag, l.kind, l.tokens))
            .collect();
        println!(
            "tier {} tokens={:?} count_keys={:?} letters={} events={}..={} extra_edges={}..={}",
            tier.name,
            tier.tokens,
            tier.keys,
            letters.join(","),
            tier.min_events,
            tier.max_events,
            tier.edges.0,
            tier.edges.1
        );
        if let Err(e) = run_tier(&tier, &mut totals, &mut findings) {
            eprintln!("search refused in tier {}: {e}", tier.name);
            return ExitCode::from(2);
        }
        println!("{}", totals.line(&format!("tier {}", tier.name)));
        grand.add(&totals);
    }
    println!("{}", grand.line("TOTAL"));
    println!("elapsed_seconds={}", start.elapsed().as_secs());
    for case in &findings.failures {
        println!("FAILURE {} | {}", case.note, case.text);
    }
    for (label, cases) in [
        ("H1>0", &findings.h1),
        ("DISCONNECTED", &findings.disconnected),
    ] {
        for case in cases {
            println!("{label} events={} {}", case.events, case.note);
            println!("PROBLEM {}", case.text);
            if label == "H1>0" {
                match guarded_certificate(case.text.as_bytes(), 1) {
                    Ok(cert) => {
                        let summary = Json::object([
                            (
                                "components",
                                cert.get("components").cloned().unwrap_or(Json::Null),
                            ),
                            (
                                "star_base",
                                cert.get("star_base").cloned().unwrap_or(Json::Null),
                            ),
                            (
                                "separating_cocycle",
                                cert.get("separating_cocycle")
                                    .cloned()
                                    .unwrap_or(Json::Null),
                            ),
                        ]);
                        println!("CERTIFICATE-SUMMARY {}", summary.to_canonical());
                    }
                    Err(e) => println!("CERTIFICATE-REFUSED {e}"),
                }
            }
        }
    }
    if grand.corollary_failures + grand.theorem_failures + grand.witness_failures > 0 {
        println!("RESULT: CROSS-CHECK FAILURES PRESENT");
        return ExitCode::from(1);
    }
    println!("RESULT: no cross-check failure in the declared menu");
    ExitCode::SUCCESS
}

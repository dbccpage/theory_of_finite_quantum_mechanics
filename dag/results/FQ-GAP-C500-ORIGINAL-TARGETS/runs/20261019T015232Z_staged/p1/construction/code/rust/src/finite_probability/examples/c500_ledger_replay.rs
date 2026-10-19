use std::io::{self, BufRead};
use tfqm_finite_probability::c500_ledger::summarize;
fn main() {
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        let f: Vec<_> = line.split('\t').collect();
        let n: usize = f[1].parse().unwrap();
        let mut targets = vec![];
        for k in 0..n {
            targets.push((
                f[2 + 2 * k].parse::<usize>().unwrap(),
                match f[3 + 2 * k] {
                    "false" => false,
                    "true" => true,
                    _ => panic!("bool required"),
                },
            ));
        }
        let at = 2 + 2 * n;
        let count: usize = f[at].parse().unwrap();
        assert_eq!(f.len(), at + 1 + 2 * count);
        let clauses: Vec<_> = (0..count)
            .map(|k| {
                (
                    f[at + 1 + 2 * k].to_string(),
                    f[at + 2 + 2 * k].parse::<u8>().unwrap(),
                )
            })
            .collect();
        let s = summarize(&targets, &clauses).unwrap();
        let mut out = vec![
            f[0].to_string(),
            s.targets.to_string(),
            s.source_satisfied.to_string(),
            s.scoped_clauses.to_string(),
            s.open_clauses.to_string(),
            s.invalid_clauses.to_string(),
        ];
        for (t, _) in targets {
            out.push(t.to_string());
        }
        out.extend(s.open_ids);
        println!("{}", out.join("\t"));
    }
    println!("ledger_status\tSOURCE_BOUND_SCOPE_MAP_NOT_ORIGINAL_TARGET_DISCHARGE");
}

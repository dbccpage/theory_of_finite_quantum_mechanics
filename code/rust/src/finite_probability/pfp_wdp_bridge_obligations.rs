//! Status ledger of the five open Genesis-to-WDP bridge obligations O01..O05, one status vector per line.
//!
//! Exact replay of `code/python/src/qm/pfp_wdp_bridge_obligations.py` for PFP batch 01, node
//! PG-WDP-GENESIS-BRIDGE-OBLIGATIONS. Statuses: 0 open, 1 control-only, 2 discharged. End-to-end is DEFINED as
//! all five discharged (a modelling choice). The programme order O01<..<O05 is our mapping of the derivation order
//! in the programme document, not a stated prerequisite relation. Rust derives the upgrade counts by simulating
//! every strict single-position update (the Python producer uses a closed form). Nothing here discharges any
//! obligation. AuthorityEffect: None.

pub const N: usize = 5;
const SOURCE_REPORTED: [u8; N] = [1, 1, 1, 1, 1];

fn all_discharged(v: &[u8; N]) -> bool {
    v.iter().all(|&s| s == 2)
}

/// Wire line for one status vector.
pub fn line(v: &[u8; N]) -> String {
    let count = |t: u8| v.iter().filter(|&&s| s == t).count();
    let (n_open, n_control, n_disch) = (count(0), count(1), count(2));
    let mut prefix = true;
    for j in 0..N {
        for k in j..N {
            if v[k] == 2 && v[j] != 2 {
                prefix = false;
            }
        }
    }
    let mut upgrades = 0usize;
    let mut completing = 0usize;
    for k in 0..N {
        for s in (v[k] + 1)..3 {
            let mut w = *v;
            w[k] = s;
            upgrades += 1;
            if all_discharged(&w) {
                completing += 1;
            }
        }
    }
    let digits: String = v.iter().map(|s| s.to_string()).collect();
    format!(
        "led\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        digits,
        n_open,
        n_control,
        n_disch,
        all_discharged(v) as i32,
        (v.iter().all(|&s| s >= 1)) as i32,
        prefix as i32,
        upgrades,
        completing,
        (*v == SOURCE_REPORTED) as i32
    )
}

/// Replay one tab-separated public-input line `led\t<five digits in 0..=2>`.
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "led" {
        return None;
    }
    let code = parts.next()?;
    if parts.next().is_some() || code.len() != N {
        return None;
    }
    let mut v = [0u8; N];
    for (i, c) in code.chars().enumerate() {
        let d = c.to_digit(10)? as u8;
        if d > 2 {
            return None;
        }
        v[i] = d;
    }
    Some(line(&v))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn all_vectors() -> Vec<[u8; N]> {
        let mut out = Vec::new();
        for x in 0..243u32 {
            let mut v = [0u8; N];
            let mut y = x;
            for i in (0..N).rev() {
                v[i] = (y % 3) as u8;
                y /= 3;
            }
            out.push(v);
        }
        out
    }

    #[test]
    fn pfp_wdp_bridge_obligations_exactly_one_vector_is_end_to_end() {
        let done: Vec<[u8; N]> = all_vectors().into_iter().filter(all_discharged).collect();
        assert_eq!(done, vec![[2, 2, 2, 2, 2]]);
    }

    #[test]
    fn pfp_wdp_bridge_obligations_controls_passing_is_not_discharge() {
        let controls = all_vectors().into_iter().filter(|v| v.iter().all(|&s| s >= 1)).count();
        assert_eq!(controls, 32);
        let l = line(&[1, 1, 1, 1, 1]);
        let cols: Vec<&str> = l.split('\t').collect();
        assert_eq!((cols[5], cols[6], cols[10]), ("0", "1", "1"));
    }

    #[test]
    fn pfp_wdp_bridge_obligations_programme_order_counts_63_prefixes() {
        let n = all_vectors().iter().filter(|v| line(v).split('\t').nth(7) == Some("1")).count();
        assert_eq!(n, 63);
        assert_eq!(line(&[0, 0, 0, 0, 2]).split('\t').nth(7), Some("0"));
    }

    #[test]
    fn pfp_wdp_bridge_obligations_single_update_completes_only_from_four_discharged() {
        for v in all_vectors() {
            let cols: Vec<String> = line(&v).split('\t').map(|s| s.to_string()).collect();
            let disch: usize = cols[4].parse().unwrap();
            assert_eq!(cols[9], if disch == 4 { "1" } else { "0" }, "{:?}", v);
        }
    }

    #[test]
    fn pfp_wdp_bridge_obligations_wire_endpoints_and_malformed_lines() {
        assert_eq!(replay("led\t00000").unwrap(), "led\t00000\t5\t0\t0\t0\t0\t1\t10\t0\t0");
        assert_eq!(replay("led\t22222").unwrap(), "led\t22222\t0\t0\t5\t1\t1\t1\t0\t0\t0");
        assert!(replay("led\t0000").is_none());
        assert!(replay("led\t00003").is_none());
        assert!(replay("led\t0000x").is_none());
        assert!(replay("sel\t00000").is_none());
        assert!(replay("led\t00000\t1").is_none());
    }
}

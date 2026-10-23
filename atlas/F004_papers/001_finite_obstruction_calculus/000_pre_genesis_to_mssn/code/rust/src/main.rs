//! Exact bounded replay of the manuscript's finite examples; no dependencies.
use std::collections::BTreeMap;
use std::io::{self, BufRead};

fn numbers(text: &str) -> Option<Vec<i64>> {
    if text.is_empty() { return Some(vec![]); }
    text.split(',').map(|s| {
        let n: i64 = s.parse().ok()?;
        if n.unsigned_abs() <= 1_000_000 && n.to_string() == s { Some(n) } else { None }
    }).collect()
}

fn natural(text: &str) -> Option<u32> {
    let value: u32 = text.parse().ok()?;
    if value.to_string() == text { Some(value) } else { None }
}

fn factor(reports: &[i64], answers: &[i64]) -> Option<BTreeMap<i64, i64>> {
    if reports.len() != answers.len() { return None; }
    let mut image = BTreeMap::new();
    for (&r, &s) in reports.iter().zip(answers) {
        if image.get(&r).is_some_and(|&old| old != s) { return None; }
        image.insert(r, s);
    }
    Some(image)
}

fn fraction(numerator: i64, denominator: i64) -> String {
    let (mut a, mut b) = (numerator.abs(), denominator);
    while b != 0 { (a,b) = (b,a % b); }
    let (n,d) = (numerator/a, denominator/a);
    if d == 1 { n.to_string() } else { format!("{n}/{d}") }
}

fn replay(line: &str) -> Option<String> {
    let fields: Vec<_> = line.split('\t').collect();
    match fields.as_slice() {
        ["v1", "factor", r, s] => {
            let (r, s) = (numbers(r)?, numbers(s)?);
            if r.len() > 8 || r.len() != s.len() { return None; }
            Some(if factor(&r, &s).is_some() { "1" } else { "0" }.to_string())
        }
        ["v1", "demand", n, w, d, b] => {
            let (n, w, d, b): (u32, u32, u32, u32) =
                (natural(n)?, natural(w)?, natural(d)?, natural(b)?);
            if n > 8 || [w, d, b].iter().any(|&x| x >= (1 << n)) { return None; }
            let residual = w & !d;
            if d & !w != 0 || b & residual != 0 { return None; }
            Some((residual | b).count_ones().to_string())
        }
        ["v1", "boundary", n, es, cs] => {
            let n: usize = natural(n)? as usize;
            let (ends, coefficients) = (numbers(es)?, numbers(cs)?);
            if n > 8 || ends.len() != 2*coefficients.len() || coefficients.len() > 16 { return None; }
            let mut result = vec![0_i64; n];
            for (pair, c) in ends.chunks_exact(2).zip(coefficients) {
                let (a, b) = (usize::try_from(pair[0]).ok()?, usize::try_from(pair[1]).ok()?);
                if a >= n || b >= n { return None; }
                result[a] -= c;
                result[b] += c;
            }
            Some(result.iter().map(i64::to_string).collect::<Vec<_>>().join(","))
        }
        ["v1", "components", n, es, cs] => {
            let n = natural(n)? as usize;
            let (ends, coefficients) = (numbers(es)?, numbers(cs)?);
            if n > 8 || ends.len() % 2 != 0 || ends.len() > 32 || coefficients.len() != n { return None; }
            let mut labels: Vec<_> = (0..n).collect();
            for pair in ends.chunks_exact(2) {
                let (a,b) = (usize::try_from(pair[0]).ok()?, usize::try_from(pair[1]).ok()?);
                if a >= n || b >= n { return None; }
                let (ra, rb) = (labels[a], labels[b]);
                for label in &mut labels {
                    if *label == ra || *label == rb { *label = ra.min(rb); }
                }
            }
            let mut totals = BTreeMap::<usize, i64>::new();
            for (&label, &weight) in labels.iter().zip(&coefficients) {
                *totals.entry(label).or_default() += weight;
            }
            Some(totals.iter().flat_map(|(label,total)| [label.to_string(),total.to_string()])
                .collect::<Vec<_>>().join(","))
        }
        ["v1", "cyclic", values] => {
            let v = numbers(values)?;
            let [modulus, value] = v.as_slice() else { return None; };
            Some(if *modulus == 0 { *value } else { value.rem_euclid(modulus.abs()) }.to_string())
        }
        ["v1", "triangle", filled, values] => {
            let filled = natural(filled)?;
            let v = numbers(values)?;
            let [x,y,z] = v.as_slice() else { return None; };
            if filled > 1 || x != y || y != z { return None; }
            Some(if filled == 1 { 0 } else { *x }.to_string())
        }
        ["v1", "cochain", values] => {
            let v = numbers(values)?;
            if v.len() != 3 { return None; }
            Some(v.iter().sum::<i64>().to_string())
        }
        ["v1", "bellpair", flag] => {
            match natural(flag)? {
                0 => Some("1,0,0,1".into()),
                1 => Some("0,1,1,0".into()),
                _ => None,
            }
        }
        ["v1", "decimal", word] => {
            if word.len() > 16 || !word.bytes().all(|c| c.is_ascii_digit()) { return None; }
            Some(word.bytes().map(|c| format!("{:04b}", c-b'0')).collect())
        }
        ["v1", "decimal_decode", bits] => {
            if bits.len() > 64 || bits.len() % 4 != 0 || !bits.bytes().all(|c| c == b'0' || c == b'1') {
                return None;
            }
            let mut result = String::new();
            for block in bits.as_bytes().chunks_exact(4) {
                let n = block.iter().fold(0, |old, c| 2*old+(c-b'0'));
                if n >= 10 { return None; }
                result.push((b'0'+n) as char);
            }
            Some(result)
        }
        ["v1", operation, word] if *operation == "recover" || *operation == "erase" => {
            if word.len() > 64 || !word.chars().all(|c| ['a','b','c'].contains(&c)) { return None; }
            if *operation == "erase" { Some(word.chars().filter(|&c| c != 'c').collect()) }
            else { Some(if word.contains('c') { "NON_DESCENT" } else { word }.to_string()) }
        }
        ["v1", "rename", ms, ws] => {
            let (mapping, word) = (numbers(ms)?, numbers(ws)?);
            if mapping.len() > 8 || word.len() > 64 { return None; }
            let mapped: Option<Vec<_>> = word.iter().map(|&i| {
                mapping.get(usize::try_from(i).ok()?).map(i64::to_string)
            }).collect();
            Some(mapped?.join(","))
        }
        ["v1", "trace", values] => {
            let values = numbers(values)?;
            if values.len() % 3 != 0 || values.len() > 48 { return None; }
            let mut reversed = Vec::new();
            for edge in values.chunks_exact(3).rev() {
                if edge[1] != 0 && edge[1] != 1 { return None; }
                reversed.extend([edge[2].to_string(), (1-edge[1]).to_string(), edge[0].to_string()]);
            }
            Some(reversed.join(","))
        }
        ["v1", "code", word] => {
            if word.len() > 64 { return None; }
            let mut result = String::new();
            for c in word.chars() {
                match c { 'a' => result.push('0'), 'b' => result.push_str("00"), _ => return None }
            }
            Some(result)
        }
        ["v1", "chsh", values] => {
            let v = numbers(values)?;
            let [a, b, c, d] = v.as_slice() else { return None; };
            Some(format!("{},{}", a+b+c-d, a+b-c+d))
        }
        ["v1", "freeword", word] => {
            if word.len() > 64 { return None; }
            let mut stack = Vec::<u8>::new();
            for c in word.bytes() {
                if !b"abAB".contains(&c) { return None; }
                if stack.last().is_some_and(|&last| last == (c ^ 32)) { stack.pop(); }
                else { stack.push(c); }
            }
            String::from_utf8(stack).ok()
        }
        ["v1", "bellmix", values] => {
            let weights = numbers(values)?;
            let total: i64 = weights.iter().sum();
            if weights.len() != 16 || weights.iter().any(|&w| w < 0) || total == 0 { return None; }
            let mut corr = [0_i64; 5];
            for (state, weight) in weights.iter().enumerate() {
                let sign = |bit: u32| -> i64 { if state & (1_usize << bit) == 0 { 1 } else { -1 } };
                let (a0,a1,b0,b1) = (sign(3),sign(2),sign(1),sign(0));
                for (i,c) in [a0*b0,a0*b1,a1*b0,a1*b1].iter().enumerate() {
                    corr[i] += weight*c;
                }
            }
            corr[4] = corr[0]+corr[1]-corr[2]+corr[3];
            Some(corr.iter().map(|&n| fraction(n,total)).collect::<Vec<_>>().join(","))
        }
        ["v1", "triangle_degree", values] => {
            let v = numbers(values)?;
            let [m,x,y,z] = v.as_slice() else { return None; };
            if x != y || y != z { return None; }
            Some(if *m == 0 { *x } else { x.rem_euclid(m.abs()) }.to_string())
        }
        _ => None,
    }
}

fn main() -> io::Result<()> {
    for line in io::stdin().lock().lines() {
        println!("{}", replay(&line?).unwrap_or_else(|| "REFUSE".to_string()));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn triangle_degree_attachment_retains_integral_torsion() {
        assert_eq!(replay("v1\ttriangle_degree\t2,1,1,1"), Some("1".into()));
        assert_eq!(replay("v1\ttriangle_degree\t2,2,2,2"), Some("0".into()));
        assert_eq!(replay("v1\ttriangle_degree\t0,-3,-3,-3"), Some("-3".into()));
        assert_eq!(replay("v1\ttriangle_degree\t-2,-3,-3,-3"), Some("1".into()));
        assert!(replay("v1\ttriangle_degree\t2,1,1,0").is_none());
    }
    #[test] fn joint_mixtures_obey_oriented_bell_bound() {
        for first in 0..16 { for second in 0..16 {
            let mut weights = [0_i64; 16];
            weights[first] += 1;
            weights[second] += 2;
            let csv = weights.iter().map(i64::to_string).collect::<Vec<_>>().join(",");
            let result = replay(&format!("v1\tbellmix\t{csv}")).unwrap();
            assert_eq!(result.split(',').count(), 5);
            let score = result.split(',').last().unwrap();
            let mut parts = score.split('/');
            let numerator: i64 = parts.next().unwrap().parse().unwrap();
            let denominator: i64 = parts.next().unwrap_or("1").parse().unwrap();
            assert!(numerator.abs() <= 2*denominator);
        } }
        assert_eq!(replay("v1\tbellmix\t1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"),
            Some("0,0,0,0,0".into()));
        assert!(replay("v1\tbellmix\t0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0").is_none());
    }
    #[test] fn free_group_reduction_and_nonabelian_commutator() {
        assert_eq!(replay("v1\tfreeword\tabBA"), Some("".into()));
        assert_eq!(replay("v1\tfreeword\tabAB"), Some("abAB".into()));
        assert_eq!(replay("v1\tfreeword\taaABbA"), Some("".into()));
        for bad in ["c".to_string(), "a".repeat(65), "á".to_string()] {
            assert!(replay(&format!("v1\tfreeword\t{bad}")).is_none());
        }
    }
    #[test] fn factors_reconstruct_image() {
        let image = factor(&[0, 1, 0], &[2, 3, 2]).unwrap();
        assert_eq!(image[&0], 2);
        assert!(factor(&[0, 0], &[1, 2]).is_none());
        assert!(factor(&[], &[]).unwrap().is_empty());
    }
    #[test] fn finite_counterexamples() {
        assert_eq!(replay("v1\tcode\taa"), replay("v1\tcode\tb"));
        assert_eq!(replay("v1\tboundary\t3\t0,1,1,2,2,0\t1,1,1"), Some("0,0,0".into()));
        assert_eq!(replay("v1\tchsh\t1,1,-1,1"), Some("0,4".into()));
        assert!(replay("v1\tdemand\t2\t1\t0\t1").is_none());
    }
    #[test] fn malformed_and_bounded_inputs() {
        for record in ["v2\tcode\ta", "v1\tcode\tc", "v1\tfactor\t0\t",
            "v1\tboundary\t1\t0,1\t1", "v1\tdemand\t9\t0\t0\t0",
            "v1\tchsh\t1000001,0,0,0"] { assert!(replay(record).is_none(), "{record}"); }
    }
    #[test] fn integral_classes_preserve_torsion_and_zero_modulus() {
        assert_eq!(replay("v1\tcyclic\t2,1"), Some("1".into()));
        assert_eq!(replay("v1\tcyclic\t2,2"), Some("0".into()));
        assert_eq!(replay("v1\tcyclic\t-2,-3"), Some("1".into()));
        assert_eq!(replay("v1\tcyclic\t0,-3"), Some("-3".into()));
        for record in ["v1\tcyclic\t2", "v1\tcyclic\t2,1,0", "v1\tcyclic\t02,1",
            "v1\tcyclic\t2,1000001"] { assert!(replay(record).is_none()); }
    }
    #[test] fn integral_component_coordinates_and_refusals() {
        assert_eq!(replay("v1\tcomponents\t0\t\t"), Some("".into()));
        assert_eq!(replay("v1\tcomponents\t3\t2,0,1,1\t2,-1,3"), Some("0,5,1,-1".into()));
        assert_eq!(replay("v1\tcomponents\t3\t0,1,1,2,2,0\t-2,1,1"), Some("0,0".into()));
        for record in ["v1\tcomponents\t2\t0,2\t1,1", "v1\tcomponents\t2\t0\t1,1",
            "v1\tcomponents\t2\t\t1", "v1\tcomponents\t9\t\t",
            "v1\tcomponents\t02\t\t1,1"] { assert!(replay(record).is_none()); }
    }
    #[test] fn triangle_kernel_and_attachment() {
        for k in [-1_000_000, -11, -1, 0, 1, 17, 1_000_000] {
            assert_eq!(replay(&format!("v1\ttriangle\t0\t{k},{k},{k}")), Some(k.to_string()));
            assert_eq!(replay(&format!("v1\ttriangle\t1\t{k},{k},{k}")), Some("0".into()));
        }
        for record in ["v1\ttriangle\t0\t1,1,0", "v1\ttriangle\t1\t1,0,1",
            "v1\ttriangle\t2\t1,1,1", "v1\ttriangle\t01\t1,1,1",
            "v1\ttriangle\t0\t1,1", "v1\ttriangle\t0\t1,1,1,1",
            "v1\ttriangle\t0\t1000001,1000001,1000001"] {
            assert!(replay(record).is_none(), "{record}");
        }
    }
    #[test] fn dual_triangle_square_zero() {
        for p in -4..=4 { for q in -4..=4 { for r in -4..=4 {
            let record = format!("v1\tcochain\t{},{},{}", q-p, r-q, p-r);
            assert_eq!(replay(&record), Some("0".into()));
        } } }
        assert_eq!(replay("v1\tcochain\t1000000,1000000,1000000"), Some("3000000".into()));
        assert!(replay("v1\tcochain\t1,2").is_none());
        assert!(replay("v1\tcochain\t1,2,1000001").is_none());
    }
    #[test] fn exact_pair_distributions() {
        for flag in 0..=1 {
            let output = replay(&format!("v1\tbellpair\t{flag}")).unwrap();
            let p = numbers(&output).unwrap();
            assert!(p.iter().all(|&x| x >= 0));
            assert_eq!(p.iter().sum::<i64>(), 2);
            assert_eq!((p[0]+p[1], p[2]+p[3], p[0]+p[2], p[1]+p[3]), (1,1,1,1));
            assert_eq!(p[0]-p[1]-p[2]+p[3], if flag == 0 { 2 } else { -2 });
        }
        for flag in ["2", "01", "-1", "+1", "١", ""] {
            assert!(replay(&format!("v1\tbellpair\t{flag}")).is_none());
        }
    }
    #[test] fn decimal_code_and_exact_decoder_domain() {
        for n in 0..=9999 {
            let digits = n.to_string();
            let bits = replay(&format!("v1\tdecimal\t{digits}")).unwrap();
            assert_eq!(bits.len(), 4*digits.len());
            assert_eq!(replay(&format!("v1\tdecimal_decode\t{bits}")), Some(digits));
        }
        for record in ["v1\tdecimal\t١", "v1\tdecimal_decode\t0", "v1\tdecimal_decode\t1010"] {
            assert!(replay(record).is_none());
        }
    }
    #[test] fn typed_recovery_and_erasure() {
        assert_eq!(replay("v1\trecover\tabba"), Some("abba".into()));
        assert_eq!(replay("v1\trecover\tacb"), Some("NON_DESCENT".into()));
        assert_eq!(replay("v1\terase\tacb"), Some("ab".into()));
        assert_eq!(replay("v1\trename\t2,0,1\t0,1,2,0"), Some("2,0,1,2".into()));
        assert!(replay("v1\trename\t2,0,1\t3").is_none());
        assert!(replay("v1\trecover\td").is_none());
    }
    #[test] fn trace_reversal_preserves_arrows_and_multiplicity() {
        let trace = "0,1,1,1,1,2,0,1,1";
        let reversed = replay(&format!("v1\ttrace\t{trace}")).unwrap();
        assert_eq!(reversed, "1,0,0,2,0,1,1,0,0");
        assert_eq!(replay(&format!("v1\ttrace\t{reversed}")), Some(trace.into()));
        assert!(replay("v1\ttrace\t0,2,1").is_none());
    }
}

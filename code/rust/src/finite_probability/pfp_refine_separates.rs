//! Supplied-tag refinement and many conflicts: exact finite tables.
//!
//! Exact integer replay of `code/python/src/qm/pfp_refine_separates.py` for PFP batch 01, node
//! PG-REFINE-SEPARATES. Conflict graphs on small vertex sets, proper one-bit tags, minimal bit counts,
//! all labelled graphs on up to 5 vertices, fibre tag counts and refinement counts. Existence tables
//! only: no claim about the cost of finding a tag. AuthorityEffect: None.

fn parse_edges(text: &str) -> Option<Vec<(usize, usize)>> {
    if text == "-" {
        return Some(Vec::new());
    }
    let mut out: Vec<(usize, usize)> = Vec::new();
    for part in text.split(',') {
        let mut it = part.split('-');
        let u: usize = it.next()?.parse().ok()?;
        let v: usize = it.next()?.parse().ok()?;
        if it.next().is_some() {
            return None;
        }
        let e = (u.min(v), u.max(v));
        if !out.contains(&e) {
            out.push(e);
        }
    }
    out.sort();
    Some(out)
}

fn edges_text(edges: &[(usize, usize)]) -> String {
    if edges.is_empty() {
        return "-".to_string();
    }
    edges.iter().map(|(u, v)| format!("{}-{}", u, v)).collect::<Vec<_>>().join(",")
}

fn adjacency(n: usize, edges: &[(usize, usize)]) -> Vec<Vec<usize>> {
    let mut adj = vec![Vec::new(); n];
    for &(u, v) in edges {
        adj[u].push(v);
        adj[v].push(u);
    }
    adj
}

fn components(n: usize, edges: &[(usize, usize)]) -> u64 {
    let adj = adjacency(n, edges);
    let mut seen = vec![false; n];
    let mut count = 0;
    for s in 0..n {
        if seen[s] {
            continue;
        }
        count += 1;
        let mut stack = vec![s];
        seen[s] = true;
        while let Some(x) = stack.pop() {
            for &y in &adj[x] {
                if !seen[y] {
                    seen[y] = true;
                    stack.push(y);
                }
            }
        }
    }
    count
}

fn one_bit_tags(n: usize, edges: &[(usize, usize)]) -> u64 {
    let mut count = 0;
    for mask in 0u64..(1u64 << n) {
        if edges.iter().all(|&(u, v)| (mask >> u & 1) != (mask >> v & 1)) {
            count += 1;
        }
    }
    count
}

fn colour_from(v: usize, n: usize, adj: &[Vec<usize>], k: usize, colour: &mut Vec<usize>) -> bool {
    if v == n {
        return true;
    }
    for c in 0..k {
        if adj[v].iter().all(|&w| w >= v || colour[w] != c) {
            colour[v] = c;
            if colour_from(v + 1, n, adj, k, colour) {
                return true;
            }
        }
    }
    false
}

fn colourable(n: usize, edges: &[(usize, usize)], k: usize) -> bool {
    let adj = adjacency(n, edges);
    let mut colour = vec![usize::MAX; n];
    colour_from(0, n, &adj, k, &mut colour)
}

fn chromatic_number(n: usize, edges: &[(usize, usize)]) -> usize {
    let mut k = 1;
    while !colourable(n, edges, k) {
        k += 1;
    }
    k
}

fn min_bits(n: usize, edges: &[(usize, usize)]) -> usize {
    let mut b = 0;
    while !colourable(n, edges, 1usize << b) {
        b += 1;
    }
    b
}

fn odd_girth(n: usize, edges: &[(usize, usize)]) -> usize {
    let adj = adjacency(n, edges);
    let mut best = 0usize;
    for s in 0..n {
        let mut dist = vec![-1i64; n];
        dist[s] = 0;
        let mut queue = vec![s];
        let mut head = 0;
        while head < queue.len() {
            let x = queue[head];
            head += 1;
            for &y in &adj[x] {
                if dist[y] < 0 {
                    dist[y] = dist[x] + 1;
                    queue.push(y);
                }
            }
        }
        for &(u, v) in edges {
            if dist[u] >= 0 && dist[u] == dist[v] {
                let length = (2 * dist[u] + 1) as usize;
                if best == 0 || length < best {
                    best = length;
                }
            }
        }
    }
    best
}

fn graph_line(name: &str, n: usize, text: &str) -> Option<String> {
    let edges = parse_edges(text)?;
    if edges.iter().any(|&(u, v)| v >= n || u >= n) || n > 20 {
        return None;
    }
    let tags = one_bit_tags(n, &edges);
    Some(format!(
        "graph\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        name,
        n,
        edges.len(),
        components(n, &edges),
        (tags > 0) as i32,
        tags,
        chromatic_number(n, &edges),
        min_bits(n, &edges),
        odd_girth(n, &edges),
        edges_text(&edges)
    ))
}

fn enum_line(n: usize) -> Option<String> {
    if n == 0 || n > 6 {
        return None;
    }
    let mut pairs = Vec::new();
    for u in 0..n {
        for v in (u + 1)..n {
            pairs.push((u, v));
        }
    }
    let (mut total, mut bipartite, mut colouring_pairs) = (0u64, 0u64, 0u64);
    let mut by_bits = [0u64; 4];
    for mask in 0u64..(1u64 << pairs.len()) {
        let edges: Vec<(usize, usize)> = (0..pairs.len()).filter(|&i| mask >> i & 1 == 1).map(|i| pairs[i]).collect();
        total += 1;
        let tags = one_bit_tags(n, &edges);
        if tags > 0 {
            bipartite += 1;
            colouring_pairs += tags;
        }
        by_bits[min_bits(n, &edges).min(3)] += 1;
    }
    Some(format!(
        "enum\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        n, total, bipartite, colouring_pairs, by_bits[0], by_bits[1], by_bits[2], by_bits[3]
    ))
}

fn fiber_bits(m: u64) -> u32 {
    let mut b = 0;
    while (1u64 << b) < m {
        b += 1;
    }
    b
}

fn injective_sequences(depth: usize, m: usize, k: usize, used: &mut Vec<bool>) -> u64 {
    if depth == m {
        return 1;
    }
    let mut total = 0;
    for c in 0..k {
        if !used[c] {
            used[c] = true;
            total += injective_sequences(depth + 1, m, k, used);
            used[c] = false;
        }
    }
    total
}

fn fiber_line(m: usize) -> Option<String> {
    if m == 0 || m > 6 {
        return None;
    }
    let mut counts = Vec::new();
    for b in 0..4 {
        let k = 1usize << b;
        let mut used = vec![false; k];
        counts.push(injective_sequences(0, m, k, &mut used));
    }
    Some(format!(
        "fiber\t{}\t{}\t{}\t{}\t{}\t{}",
        m,
        fiber_bits(m as u64),
        counts[0],
        counts[1],
        counts[2],
        counts[3]
    ))
}

fn refine_line(n: usize, o: usize, t: usize) -> Option<String> {
    if n == 0 || o == 0 || t == 0 || (o.pow(n as u32)).checked_mul(t.pow(n as u32))? > 100_000 {
        return None;
    }
    let (mut total, mut failures, mut sep, mut equal_count, mut old_kept) = (0u64, 0u64, 0u64, 0u64, 0u64);
    for qi in 0..o.pow(n as u32) {
        let q: Vec<usize> = (0..n).map(|a| qi / o.pow(a as u32) % o).collect();
        for gi in 0..t.pow(n as u32) {
            let g: Vec<usize> = (0..n).map(|a| gi / t.pow(a as u32) % t).collect();
            for a in 0..n {
                for b in 0..n {
                    total += 1;
                    let equal = q[a] == q[b] && g[a] == g[b];
                    // The refined pair is (q, g): it is equal exactly when both components agree.
                    let refined_a = (q[a], g[a]);
                    let refined_b = (q[b], g[b]);
                    if (refined_a == refined_b) != equal {
                        failures += 1;
                    }
                    if q[a] == q[b] && g[a] != g[b] {
                        sep += 1;
                        if refined_a == refined_b {
                            failures += 1;
                        }
                    }
                    if q[a] != q[b] {
                        old_kept += 1;
                        if refined_a == refined_b {
                            failures += 1;
                        }
                    }
                    if refined_a == refined_b {
                        equal_count += 1;
                    }
                }
            }
        }
    }
    Some(format!("refine\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}", n, o, t, total, failures, sep, equal_count, old_kept))
}

/// Replay one tab-separated public-input line (graph / enum / fiber / fiberbits / refine).
pub fn replay(input: &str) -> Option<String> {
    let parts: Vec<&str> = input.split('\t').collect();
    match *parts.first()? {
        "graph" if parts.len() == 4 => graph_line(parts[1], parts[2].parse().ok()?, parts[3]),
        "enum" if parts.len() == 2 => enum_line(parts[1].parse().ok()?),
        "fiber" if parts.len() == 2 => fiber_line(parts[1].parse().ok()?),
        "fiberbits" if parts.len() == 2 => {
            let m: u64 = parts[1].parse().ok()?;
            if m == 0 {
                return None;
            }
            Some(format!("fiberbits\t{}\t{}", m, fiber_bits(m)))
        }
        "refine" if parts.len() == 4 => refine_line(parts[1].parse().ok()?, parts[2].parse().ok()?, parts[3].parse().ok()?),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn cols(line: &str) -> Vec<String> {
        line.split('\t').map(|s| s.to_string()).collect()
    }

    #[test]
    fn pfp_refine_separates_triangle_and_odd_cycles_need_two_bits() {
        let t = cols(&replay("graph\ttriangle\t3\t0-1,1-2,0-2").unwrap());
        assert_eq!(t[5..10], ["0", "0", "3", "2", "3"]);
        let c5 = cols(&replay("graph\tcycle5\t5\t0-1,1-2,2-3,3-4,0-4").unwrap());
        assert_eq!(c5[5..10], ["0", "0", "3", "2", "5"]);
        let k33 = cols(&replay("graph\tk33\t6\t0-3,0-4,0-5,1-3,1-4,1-5,2-3,2-4,2-5").unwrap());
        assert_eq!(k33[5..10], ["1", "2", "2", "1", "0"]);
    }

    #[test]
    fn pfp_refine_separates_labelled_bipartite_counts() {
        let counts: Vec<String> = (1..=5).map(|n| cols(&replay(&format!("enum\t{}", n)).unwrap())[3].clone()).collect();
        assert_eq!(counts, ["1", "2", "7", "41", "376"]);
        let five = cols(&replay("enum\t5").unwrap());
        assert_eq!(&five[5..9], ["1", "375", "647", "1"]);
    }

    #[test]
    fn pfp_refine_separates_fibre_bit_counts() {
        assert_eq!(replay("fiber\t3").unwrap(), "fiber\t3\t2\t0\t0\t24\t336");
        assert_eq!(replay("fiber\t1").unwrap(), "fiber\t1\t0\t1\t2\t4\t8");
        assert_eq!(replay("fiberbits\t17").unwrap(), "fiberbits\t17\t5");
    }

    #[test]
    fn pfp_refine_separates_refinement_counts_and_iff() {
        assert_eq!(replay("refine\t3\t2\t2").unwrap(), "refine\t3\t2\t2\t576\t0\t96\t288\t192");
        let l = cols(&replay("refine\t4\t2\t2").unwrap());
        assert_eq!(l[5], "0");
        assert_eq!(l[6], "768");
    }

    #[test]
    fn pfp_refine_separates_rejects_malformed_lines() {
        assert!(replay("graph\tbad\t2\t0-5").is_none());
        assert!(replay("fiber\t0").is_none());
        assert!(replay("unknown\t1").is_none());
    }
}

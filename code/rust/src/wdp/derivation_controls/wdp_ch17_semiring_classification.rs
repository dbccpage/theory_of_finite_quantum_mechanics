
const ALPHABET: [i64; 3] = [-1, 0, 1];

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Witness {
    pub matrices: i64,
    pub partitions: i64,
    pub pairs: i64,
    pub discrete_p1: i64,
    pub one_block_p0: i64,
    pub one_block_p1: i64,
    pub p1_pairs: i64,
    pub refusals: i64,
    pub multiplicity_squares: i64,
    pub example1_b: [i64; 4],
    pub example1_row_sums: [i64; 3],
    pub example1_pm: [i64; 6],
    pub example1_lengths: i64,
    pub example2_source_6: i64,
    pub example2_total_6: i64,
    pub example3_summands: [i64; 2],
    pub example3_block_sum: i64,
    pub example4_length0_source: i64,
    pub example4_length0_total: i64,
    pub example4_length8_source: i64,
    pub example4_edges: [i64; 2],
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct Mat {
    rows: usize,
    cols: usize,
    entries: Vec<i64>,
}

impl Mat {
    fn get(&self, row: usize, col: usize) -> i64 {
        self.entries[row * self.cols + col]
    }

    fn eye(n: usize) -> Mat {
        let mut entries = vec![0_i64; n * n];
        for index in 0..n {
            entries[index * n + index] = 1;
        }
        Mat {
            rows: n,
            cols: n,
            entries,
        }
    }
}

fn add(left: i64, right: i64) -> i64 {
    left.checked_add(right).expect("i64 addition overflowed")
}

fn mul_i(left: i64, right: i64) -> i64 {
    left.checked_mul(right).expect("i64 multiplication overflowed")
}

fn sub(left: i64, right: i64) -> i64 {
    left.checked_sub(right).expect("i64 subtraction overflowed")
}

fn mat_from(rows: &[&[i64]]) -> Mat {
    assert!(!rows.is_empty(), "matrix needs a row");
    let cols = rows[0].len();
    assert!(rows.iter().all(|row| row.len() == cols), "ragged matrix");
    let mut entries = Vec::with_capacity(rows.len() * cols);
    for row in rows {
        entries.extend_from_slice(row);
    }
    Mat {
        rows: rows.len(),
        cols,
        entries,
    }
}

fn mul(left: &Mat, right: &Mat) -> Mat {
    assert_eq!(left.cols, right.rows, "matrix product shape");
    let mut entries = vec![0_i64; left.rows * right.cols];
    for i in 0..left.rows {
        for k in 0..left.cols {
            let lik = left.get(i, k);
            for j in 0..right.cols {
                let index = i * right.cols + j;
                entries[index] = add(entries[index], mul_i(lik, right.get(k, j)));
            }
        }
    }
    Mat {
        rows: left.rows,
        cols: right.cols,
        entries,
    }
}

fn transpose(matrix: &Mat) -> Mat {
    let mut entries = vec![0_i64; matrix.rows * matrix.cols];
    for i in 0..matrix.rows {
        for j in 0..matrix.cols {
            entries[j * matrix.rows + i] = matrix.get(i, j);
        }
    }
    Mat {
        rows: matrix.cols,
        cols: matrix.rows,
        entries,
    }
}

fn sum_entries(matrix: &Mat) -> i64 {
    matrix.entries.iter().copied().fold(0_i64, add)
}

fn matrix_power(matrix: &Mat, length: usize) -> Mat {
    let mut power = Mat::eye(matrix.rows);
    for _ in 0..length {
        power = mul(&power, matrix);
    }
    power
}

fn source_column(matrix: &Mat, length: usize) -> Vec<i64> {
    let ones = Mat {
        rows: matrix.rows,
        cols: 1,
        entries: vec![1_i64; matrix.rows],
    };
    mul(&matrix_power(matrix, length), &ones).entries
}

fn set_partitions(n: usize) -> Vec<Vec<Vec<usize>>> {
    if n == 0 {
        return vec![Vec::new()];
    }
    let mut out = Vec::new();
    for part in set_partitions(n - 1) {
        let mut singleton = part.clone();
        singleton.push(vec![n - 1]);
        out.push(singleton);
        for index in 0..part.len() {
            let mut inserted = part.clone();
            inserted[index].push(n - 1);
            out.push(inserted);
        }
    }
    out
}

fn canonicalize(mut blocks: Vec<Vec<usize>>) -> Vec<Vec<usize>> {
    for block in &mut blocks {
        block.sort_unstable();
    }
    blocks.sort();
    blocks
}

fn partitions_of(n: usize) -> Vec<Vec<Vec<usize>>> {
    let mut parts: Vec<_> = set_partitions(n).into_iter().map(canonicalize).collect();
    parts.sort();
    parts
}

fn validate_partition(n: usize, blocks: &[Vec<usize>]) -> Result<(), &'static str> {
    if n == 0 || blocks.is_empty() {
        return Err("refused: empty carrier or empty partition");
    }
    let mut seen = vec![false; n];
    for block in blocks {
        if block.is_empty() {
            return Err("refused: empty block");
        }
        for &vertex in block {
            if vertex >= n || seen[vertex] {
                return Err("refused: blocks are not a partition");
            }
            seen[vertex] = true;
        }
    }
    if seen.iter().any(|flag| !flag) {
        Err("refused: blocks are not a partition")
    } else {
        Ok(())
    }
}

fn membership(n: usize, blocks: &[Vec<usize>]) -> Mat {
    let width = blocks.len();
    let mut entries = vec![0_i64; n * width];
    for (column, block) in blocks.iter().enumerate() {
        for &vertex in block {
            entries[vertex * width + column] = 1;
        }
    }
    Mat {
        rows: n,
        cols: width,
        entries,
    }
}

fn block_sum(matrix: &Mat, source: usize, target: &[usize]) -> i64 {
    target.iter().fold(0_i64, |acc, &vertex| add(acc, matrix.get(source, vertex)))
}

fn rows_agree(matrix: &Mat, blocks: &[Vec<usize>]) -> bool {
    blocks.iter().all(|block| {
        let Some(&first) = block.first() else {
            return false;
        };
        block.iter().skip(1).all(|&vertex| {
            (0..matrix.cols).all(|column| matrix.get(vertex, column) == matrix.get(first, column))
        })
    })
}

fn quotient(matrix: &Mat, blocks: &[Vec<usize>]) -> Result<Mat, &'static str> {
    if matrix.rows != matrix.cols {
        return Err("refused: matrix is not square");
    }
    validate_partition(matrix.rows, blocks)?;
    let width = blocks.len();
    let mut entries = vec![0_i64; width * width];
    for (i, source) in blocks.iter().enumerate() {
        for (j, target) in blocks.iter().enumerate() {
            let first = block_sum(matrix, source[0], target);
            for &vertex in source.iter().skip(1) {
                if block_sum(matrix, vertex, target) != first {
                    return Err("refused: outgoing block sums depend on the representative");
                }
            }
            entries[i * width + j] = first;
        }
    }
    let quotient_matrix = Mat {
        rows: width,
        cols: width,
        entries,
    };
    let h = membership(matrix.rows, blocks);
    if mul(matrix, &h) != mul(&h, &quotient_matrix) {
        return Err("internal: constant block sums did not give MH=HB");
    }
    Ok(quotient_matrix)
}

fn agreeing_lengths(matrix: &Mat, blocks: &[Vec<usize>], quotient_matrix: &Mat, max_n: usize) -> usize {
    let h = membership(matrix.rows, blocks);
    let mut power_m = Mat::eye(matrix.rows);
    let mut power_b = Mat::eye(quotient_matrix.rows);
    let mut agreed = 0_usize;
    for _length in 0..=max_n {
        if mul(&power_m, &h) != mul(&h, &power_b) {
            return agreed;
        }
        agreed += 1;
        power_m = mul(&power_m, matrix);
        power_b = mul(&power_b, quotient_matrix);
    }
    agreed
}

fn row_sum_multiplicity() -> [i64; 5] {
    let mut counts = [0_i64; 5];
    for &left in &ALPHABET {
        for &right in &ALPHABET {
            let index = usize::try_from(add(left, right) + 2).expect("row-sum index");
            counts[index] += 1;
        }
    }
    counts
}

fn array_from<const N: usize>(entries: &[i64]) -> [i64; N] {
    let mut out = [0_i64; N];
    out.copy_from_slice(entries);
    out
}

struct Counts {
    matrices: i64,
    partitions: i64,
    pairs: i64,
    discrete_p1: i64,
    one_block_p0: i64,
    one_block_p1: i64,
    p1_pairs: i64,
    refusals: i64,
    multiplicity_squares: i64,
}

fn census() -> Counts {
    let parts = partitions_of(2);
    assert_eq!(parts.len(), 2, "a 2-set has two nonempty partitions");
    assert_eq!(parts, vec![vec![vec![0], vec![1]], vec![vec![0, 1]]]);
    let mut matrices = 0_i64;
    let mut discrete_p1 = 0_i64;
    let mut one_block_p0 = 0_i64;
    let mut one_block_p1 = 0_i64;
    let mut admitted = 0_i64;
    let mut refused = 0_i64;
    let mut identical_rows = 0_i64;
    for &a in &ALPHABET {
        for &b in &ALPHABET {
            for &c in &ALPHABET {
                for &d in &ALPHABET {
                    matrices = add(matrices, 1);
                    let matrix = mat_from(&[&[a, b], &[c, d]]);
                    let same_rows = a == c && b == d;
                    if same_rows {
                        identical_rows = add(identical_rows, 1);
                    }
                    for blocks in &parts {
                        let p0 = rows_agree(&matrix, blocks);
                        if blocks.len() == 1 && same_rows {
                            assert!(p0, "identical rows are P0 on the one-block partition");
                        }
                        match quotient(&matrix, blocks) {
                            Ok(quotient_matrix) => {
                                admitted = add(admitted, 1);
                                assert_eq!(agreeing_lengths(&matrix, blocks, &quotient_matrix, 8), 9);
                                if blocks.len() == 1 {
                                    one_block_p1 = add(one_block_p1, 1);
                                    if p0 {
                                        one_block_p0 = add(one_block_p0, 1);
                                    }
                                    let row_sum = add(a, b);
                                    assert_eq!(row_sum, add(c, d));
                                    assert_eq!(quotient_matrix.get(0, 0), row_sum);
                                } else if blocks.len() == 2 {
                                    discrete_p1 = add(discrete_p1, 1);
                                    assert_eq!(quotient_matrix, matrix);
                                    assert!(p0, "singleton blocks agree row-wise");
                                } else {
                                    panic!("two vertices have no other nonempty partition");
                                }
                            }
                            Err(message) => {
                                assert!(message.starts_with("refused:"), "{message}");
                                refused = add(refused, 1);
                                assert!(!p0, "P0 produced a refusal");
                                assert_eq!(blocks.len(), 1);
                                assert_ne!(add(a, b), add(c, d));
                                let h = membership(2, blocks);
                                let mh = mul(&matrix, &h);
                                assert_ne!(mh.get(0, 0), mh.get(1, 0));
                            }
                        }
                    }
                }
            }
        }
    }
    assert_eq!(matrices, i64::from(3_u32.pow(4)));
    assert_eq!(identical_rows, one_block_p0);
    assert!(one_block_p0 < one_block_p1, "P1 does not imply P0 on this box");
    let counts = row_sum_multiplicity();
    assert_eq!(counts, [1, 2, 3, 2, 1]);
    let squares = counts.iter().copied().map(|count| mul_i(count, count)).fold(0_i64, add);
    assert_eq!(squares, one_block_p1);
    let partitions = i64::try_from(parts.len()).expect("partition count");
    let pairs = mul_i(matrices, partitions);
    assert_eq!(add(admitted, refused), pairs);
    let p1_pairs = add(discrete_p1, one_block_p1);
    assert_eq!(p1_pairs, admitted);
    assert_eq!(discrete_p1, matrices);
    assert_eq!(refused, sub(pairs, p1_pairs));
    assert_eq!(refused, sub(matrices, one_block_p1));
    Counts {
        matrices,
        partitions,
        pairs,
        discrete_p1,
        one_block_p0,
        one_block_p1,
        p1_pairs,
        refusals: refused,
        multiplicity_squares: squares,
    }
}

fn example1_matrix() -> Mat {
    mat_from(&[&[2, -1, 3], &[0, 1, 3], &[4, -2, 1]])
}

fn example1_blocks() -> Vec<Vec<usize>> {
    vec![vec![0, 1], vec![2]]
}

fn example_one() -> ([i64; 4], [i64; 3], [i64; 6], i64) {
    let matrix = example1_matrix();
    let blocks = example1_blocks();
    assert!(!rows_agree(&matrix, &blocks), "example 1 rows differ inside the block");
    let quotient_matrix = quotient(&matrix, &blocks).expect("example 1 admits MH=HB");
    let b_entries = array_from::<4>(&quotient_matrix.entries);
    assert_eq!(b_entries, [1, 3, 2, 1]);
    let one_block = vec![vec![0_usize, 1, 2]];
    assert!(quotient(&matrix, &one_block).is_err(), "example 1 fails P2");
    let mut row_sums = [0_i64; 3];
    for source in 0..3 {
        row_sums[source] = (0..3).fold(0_i64, |acc, column| add(acc, matrix.get(source, column)));
    }
    assert_eq!(row_sums, [4, 4, 3]);
    let lengths = agreeing_lengths(&matrix, &blocks, &quotient_matrix, 12);
    assert_eq!(lengths, 13);
    let h = membership(3, &blocks);
    let p = transpose(&h);
    assert_eq!(array_from::<6>(&p.entries), [1, 1, 0, 0, 0, 1]);
    assert_eq!(p.get(0, 0), p.get(0, 1));
    assert_eq!(p.get(1, 0), p.get(1, 1));
    let pm = mul(&p, &matrix);
    let pm_entries = array_from::<6>(&pm.entries);
    assert_eq!(pm_entries, [2, 0, 6, 4, -2, 1]);
    assert_ne!(pm.get(0, 0), pm.get(0, 1));
    assert_ne!(pm.get(1, 0), pm.get(1, 1));
    (b_entries, row_sums, pm_entries, i64::try_from(lengths).expect("length count"))
}

fn example_two() -> (i64, i64) {
    let matrix = mat_from(&[&[2, 0, 0], &[0, 0, 2], &[0, 0, 2]]);
    let split = vec![vec![0_usize, 1], vec![2]];
    assert!(quotient(&matrix, &split).is_err(), "example 2 split is not P1");
    let one_block = vec![vec![0_usize, 1, 2]];
    let quotient_matrix = quotient(&matrix, &one_block).expect("example 2 is P2");
    assert_eq!(quotient_matrix.get(0, 0), 2);
    assert_eq!(agreeing_lengths(&matrix, &one_block, &quotient_matrix, 6), 7);
    let mut power_of_two = 1_i64;
    let mut source_6 = 0_i64;
    let mut total_6 = 0_i64;
    for length in 0..=6 {
        let total = sum_entries(&matrix_power(&matrix, length));
        let column = source_column(&matrix, length);
        assert_eq!(column, vec![power_of_two, power_of_two, power_of_two]);
        assert_eq!(total, mul_i(3, power_of_two));
        assert_eq!(total, column.iter().copied().fold(0_i64, add));
        assert_ne!(column[0], total, "per-source aggregate is not the sum of all entries");
        if length == 6 {
            source_6 = column[0];
            total_6 = total;
        }
        if length < 6 {
            power_of_two = mul_i(power_of_two, 2);
        }
    }
    (source_6, total_6)
}

fn example_three() -> ([i64; 2], i64) {
    let matrix = mat_from(&[&[1, -1], &[0, 0]]);
    let one_block = vec![vec![0_usize, 1]];
    assert!(!rows_agree(&matrix, &one_block));
    let left = matrix.get(0, 0);
    let right = matrix.get(0, 1);
    assert_ne!(left, 0);
    assert_ne!(right, 0);
    let block_sum = add(left, right);
    assert_eq!(block_sum, 0);
    assert_eq!(add(matrix.get(1, 0), matrix.get(1, 1)), 0);
    let quotient_matrix = quotient(&matrix, &one_block).expect("example 3 one-block");
    assert_eq!(quotient_matrix.get(0, 0), block_sum);
    assert_ne!(matrix.get(0, 0), matrix.get(1, 0));
    ([left, right], block_sum)
}

fn example_four() -> (i64, i64, i64, [i64; 2]) {
    let matrix = mat_from(&[&[1, -1, 0], &[0, 1, -1], &[0, 0, 0]]);
    let split = vec![vec![0_usize, 1], vec![2]];
    assert!(quotient(&matrix, &split).is_err(), "example 4 split is not P1");
    let one_block = vec![vec![0_usize, 1, 2]];
    let quotient_matrix = quotient(&matrix, &one_block).expect("example 4 one-block");
    assert_eq!(quotient_matrix.get(0, 0), 0);
    assert_eq!(agreeing_lengths(&matrix, &one_block, &quotient_matrix, 8), 9);
    let edges = [matrix.get(0, 0), matrix.get(1, 0)];
    assert_eq!(edges, [1, 0]);
    let column0 = source_column(&matrix, 0);
    assert_eq!(column0, vec![1, 1, 1]);
    let total0 = sum_entries(&matrix_power(&matrix, 0));
    assert_eq!(total0, 3);
    assert_ne!(column0[0], total0, "empty-path weight is not the sum of all entries of I");
    let mut length8 = 0_i64;
    for length in 1..=8 {
        let column = source_column(&matrix, length);
        assert_eq!(column, vec![0, 0, 0]);
        if length == 8 {
            length8 = column[0];
        }
    }
    (column0[0], total0, length8, edges)
}

pub fn witness() -> Witness {
    let counts = census();
    let (example1_b, example1_row_sums, example1_pm, example1_lengths) = example_one();
    let (example2_source_6, example2_total_6) = example_two();
    let (example3_summands, example3_block_sum) = example_three();
    let (example4_length0_source, example4_length0_total, example4_length8_source, example4_edges) =
        example_four();
    let zero = mat_from(&[&[0, 0], &[0, 0]]);
    assert!(quotient(&zero, &[]).is_err(), "the empty partition is outside the scope");
    Witness {
        matrices: counts.matrices,
        partitions: counts.partitions,
        pairs: counts.pairs,
        discrete_p1: counts.discrete_p1,
        one_block_p0: counts.one_block_p0,
        one_block_p1: counts.one_block_p1,
        p1_pairs: counts.p1_pairs,
        refusals: counts.refusals,
        multiplicity_squares: counts.multiplicity_squares,
        example1_b,
        example1_row_sums,
        example1_pm,
        example1_lengths,
        example2_source_6,
        example2_total_6,
        example3_summands,
        example3_block_sum,
        example4_length0_source,
        example4_length0_total,
        example4_length8_source,
        example4_edges,
    }
}

pub fn refuse_example_two_split() -> Result<(), &'static str> {
    let matrix = mat_from(&[&[2, 0, 0], &[0, 0, 2], &[0, 0, 2]]);
    let one_block = vec![vec![0_usize, 1, 2]];
    let quotient_matrix = quotient(&matrix, &one_block).expect("example 2 one-block quotient");
    assert_eq!(quotient_matrix.get(0, 0), 2);
    let split = vec![vec![0_usize, 1], vec![2]];
    assert_eq!(block_sum(&matrix, 0, &split[0]), 2);
    assert_eq!(block_sum(&matrix, 0, &split[1]), 0);
    assert_eq!(block_sum(&matrix, 1, &split[0]), 0);
    assert_eq!(block_sum(&matrix, 1, &split[1]), 2);
    match quotient(&matrix, &split) {
        Ok(_) => panic!("unequal source-block sums were accepted"),
        Err(message) => Err(message),
    }
}

#[cfg(test)]
mod tests {
    use super::{
        add, agreeing_lengths, example1_blocks, example1_matrix, mat_from, membership, mul,
        quotient, refuse_example_two_split, source_column, sum_entries, witness, Mat,
    };

    #[test]
    fn two_vertex_box_and_opened_lengths() {
        let found = witness();
        assert_eq!(found.matrices, 81);
        assert_eq!(found.partitions, 2);
        assert_eq!(found.pairs, 162);
        assert_eq!(found.discrete_p1, 81);
        assert_eq!(found.one_block_p0, 9);
        assert_eq!(found.one_block_p1, 19);
        assert!(found.one_block_p0 < found.one_block_p1);
        assert_eq!(found.multiplicity_squares, 19);
        assert_eq!(found.p1_pairs, 100);
        assert_eq!(found.refusals, 62);
        assert_eq!(add(found.discrete_p1, found.one_block_p1), found.p1_pairs);
        assert_eq!(add(found.p1_pairs, found.refusals), found.pairs);
        assert_eq!(found.example1_b, [1, 3, 2, 1]);
        assert_eq!(found.example1_row_sums, [4, 4, 3]);
        assert_ne!(found.example1_row_sums[0], found.example1_row_sums[2]);
        assert_eq!(found.example1_pm, [2, 0, 6, 4, -2, 1]);
        assert_eq!((found.example1_pm[0], found.example1_pm[3]), (2, 4));
        assert_eq!((found.example1_pm[1], found.example1_pm[4]), (0, -2));
        assert_ne!(found.example1_pm[0], found.example1_pm[1]);
        assert_eq!(found.example1_lengths, 13);
        assert_eq!(found.example2_source_6, 64);
        assert_eq!(found.example2_total_6, 192);
        assert_ne!(found.example2_source_6, found.example2_total_6);
        assert_eq!(found.example3_summands, [1, -1]);
        assert_eq!(found.example3_block_sum, 0);
        assert_eq!(add(found.example3_summands[0], found.example3_summands[1]), 0);
        assert_eq!(found.example4_length0_source, 1);
        assert_eq!(found.example4_length0_total, 3);
        assert_ne!(found.example4_length0_source, found.example4_length0_total);
        assert_eq!(found.example4_length8_source, 0);
        assert_eq!(found.example4_edges, [1, 0]);
        assert_ne!(found.example4_edges[0], found.example4_edges[1]);

        let matrix = example1_matrix();
        let blocks = example1_blocks();
        let quotient_matrix = quotient(&matrix, &blocks).expect("example 1");
        let h = membership(matrix.rows, &blocks);
        let mut power_m = Mat::eye(matrix.rows);
        let mut power_b = Mat::eye(quotient_matrix.rows);
        for _length in 0..=12 {
            assert_eq!(mul(&power_m, &h), mul(&h, &power_b));
            power_m = mul(&power_m, &matrix);
            power_b = mul(&power_b, &quotient_matrix);
        }

        let fourth = mat_from(&[&[1, -1, 0], &[0, 1, -1], &[0, 0, 0]]);
        let split = vec![vec![0_usize, 1], vec![2]];
        assert!(quotient(&fourth, &split).is_err());
        let one_block = vec![vec![0_usize, 1, 2]];
        let fourth_quotient = quotient(&fourth, &one_block).expect("example 4");
        assert_eq!(fourth_quotient.get(0, 0), 0);
        assert_eq!(agreeing_lengths(&fourth, &one_block, &fourth_quotient, 8), 9);
        assert_eq!(source_column(&fourth, 0), vec![1, 1, 1]);
        assert_eq!(sum_entries(&Mat::eye(3)), 3);
        for length in 1..=8 {
            assert_eq!(source_column(&fourth, length), vec![0, 0, 0]);
        }
    }

    #[test]
    fn refuses_equal_totals_with_unequal_blocks() {
        assert_eq!(
            refuse_example_two_split(),
            Err("refused: outgoing block sums depend on the representative")
        );
    }
}

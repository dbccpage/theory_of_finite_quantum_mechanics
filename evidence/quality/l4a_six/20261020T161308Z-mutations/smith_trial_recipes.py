"""Literal staged Smith faults; no current-source grade is inferred."""
def recipes():
    from mutations import candidates
    legacy={'SM'+str(i).zfill(2) for i in range(1,7)}|{'SP'+str(i).zfill(2) for i in range(1,9)}
    entries=[dict(e) for e in candidates() if e['source']=='code/rust/src/linear_algebra/smith_form.rs' and e['id'].split('-',1)[0] in legacy]
    for e in entries:
        if e['id']=='SP05-storage-budget':
            e['before']='        admit_sparse_elements(storage, limit)?;\n        let counts = sparse_column_counts(matrix)?;'
            e['after']='        let counts = sparse_column_counts(matrix)?;'
    entries.extend(dict(id=i,before=b,after=a,outcome='unrun',source='code/rust/src/linear_algebra/smith_form.rs')for i,b,a in extra_recipes())
    return entries

def extra_recipes():
    return [
        ('CV01-native-zero-denominator','if d == 0 {','if false {'),
        ('CV02-native-before-widening','let n_big = BigInt::from(*val.numer());\n    let d_big = BigInt::from(d);','let n_big = BigInt::from(*val.numer() / d);\n    let d_big = BigInt::from(1);'),
        ('CV03-native-fraction','if (&n_big % &d_big).is_zero() {','if true {'),
        ('CV04-big-zero-denominator','if val.denom().is_zero() {','if false {'),
        ('CV05-big-fraction','if (n % d).is_zero() {','if true {'),
        ('SM07-diagonal-admission','        self.check_diagonal(rank)?;',''),
        ('SM08-column-orientation','        transpose_integer_rows(&mut self.v);',''),
        ('SM09-diagonal-privacy','    invariants: Vec<BigInt>,\n}','    pub invariants: Vec<BigInt>,\n}'),
        ('SM10-result-privacy','    diagonal: SmithDiagonal,\n    diagonal_matrix: BasicMatrix<BigInt>,\n    u: BasicMatrix<BigInt>,\n    v: BasicMatrix<BigInt>,','    pub diagonal: SmithDiagonal,\n    pub diagonal_matrix: BasicMatrix<BigInt>,\n    pub u: BasicMatrix<BigInt>,\n    pub v: BasicMatrix<BigInt>,'),
        ('HG01-output-metadata','.and_then(|n| n.checked_add(matrix.cols.min(nonzero)))','.and_then(|n| n.checked_add(0))'),
        ('HG02-row-mask','column.retain(|(row, _)| !pivot.iter().any(|(pivot_row, _)| pivot_row == row));','column.clear();'),
        ('HG03-gcd-value','g.gcd(value)','g + *value'),
        ('HG04-swap-order','columns.swap_remove(index)','columns.remove(index)'),
        ('HG05-row-removal','            remove_sparse_pivot_rows(&mut columns, &pivot);',''),
        ('HG06-zero-workspace','if nonzero == 0 {','if false {'),
    ]

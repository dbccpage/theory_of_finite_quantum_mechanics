
pub fn verify() -> Result<i8, &'static str> {
    let rows = [
        [xi(), ix(), xx()],
        [iy(), yi(), yy()],
        [xy(), yx(), zz()],
    ];
    let mut row_phase = 0i8;
    for row in &rows {
        let product = mul(&mul(&row[0], &row[1])?, &row[2])?;
        if !is_signed_identity(&product) {
            return Err("row product is not ±I");
        }
        row_phase = (row_phase + product.phase) % 4;
    }
    let mut col_phase = 0i8;
    for col in 0..3 {
        let product = mul(&mul(&rows[0][col], &rows[1][col])?, &rows[2][col])?;
        if !is_signed_identity(&product) {
            return Err("column product is not ±I");
        }
        col_phase = (col_phase + product.phase) % 4;
    }
    if row_phase == col_phase {
        return Err("row and column phases agree");
    }
    if assignments() != 0 {
        return Err("noncontextual assignment exists");
    }
    Ok(col_phase - row_phase)
}

#[derive(Clone, Copy)]
struct Op {
    x: [u8; 2],
    z: [u8; 2],
    phase: i8,
}

fn mul(left: &Op, right: &Op) -> Result<Op, &'static str> {
    let mut extra = 0i8;
    let mut x = [0u8; 2];
    let mut z = [0u8; 2];
    for q in 0..2 {
        let overlap = i8::try_from(left.z[q] & right.x[q]).map_err(|_| "phase")?;
        extra = extra.checked_add(2i8.checked_mul(overlap).ok_or("phase")?).ok_or("phase")?;
        x[q] = left.x[q] ^ right.x[q];
        z[q] = left.z[q] ^ right.z[q];
    }
    let phase = left
        .phase
        .checked_add(right.phase)
        .and_then(|sum| sum.checked_add(extra))
        .ok_or("phase")?
        .rem_euclid(4);
    Ok(Op { x, z, phase })
}

fn is_signed_identity(op: &Op) -> bool {
    op.x == [0, 0] && op.z == [0, 0]
}

fn pauli(x0: u8, z0: u8, x1: u8, z1: u8, phase: i8) -> Op {
    Op {
        x: [x0, x1],
        z: [z0, z1],
        phase,
    }
}

fn xi() -> Op { pauli(1, 0, 0, 0, 0) }
fn ix() -> Op { pauli(0, 0, 1, 0, 0) }
fn xx() -> Op { pauli(1, 0, 1, 0, 0) }
fn iy() -> Op { pauli(0, 0, 1, 1, 1) }
fn yi() -> Op { pauli(1, 1, 0, 0, 1) }
fn yy() -> Op { pauli(1, 1, 1, 1, 2) }
fn xy() -> Op { pauli(1, 0, 1, 1, 1) }
fn yx() -> Op { pauli(1, 1, 1, 0, 1) }
fn zz() -> Op { pauli(0, 1, 0, 1, 0) }

fn assignments() -> u32 {
    let mut found = 0u32;
    for mask in 0..512u32 {
        let bit = |index: u32| ((mask >> index) & 1) as u8;
        let rows = bit(0) ^ bit(1) ^ bit(2) == 0
            && bit(3) ^ bit(4) ^ bit(5) == 0
            && bit(6) ^ bit(7) ^ bit(8) == 0;
        let cols = bit(0) ^ bit(3) ^ bit(6) == 0
            && bit(1) ^ bit(4) ^ bit(7) == 0
            && bit(2) ^ bit(5) ^ bit(8) == 1;
        if rows && cols {
            found += 1;
        }
    }
    found
}

//! Campaign module four_wall_operad.
//!
//! Four wall transports read from a vertex potential telescope to zero, and
//! the same signed sum counts each corner once with each sign. Interval
//! composition in the operad is associative on lengths.

pub fn verify() -> Result<i64, &'static str> {
    let corners = [2i64, 5, -1, 4];
    let walls = [
        corners[1] - corners[0],
        corners[2] - corners[1],
        corners[3] - corners[2],
        corners[0] - corners[3],
    ];
    let mut telescoping = 0i64;
    for wall in walls {
        telescoping = telescoping.checked_add(wall).ok_or("wall")?;
    }
    let mut signed = 0i64;
    for corner in corners {
        signed = signed
            .checked_add(corner)
            .and_then(|v| v.checked_sub(corner))
            .ok_or("corner")?;
    }
    if telescoping != 0 || signed != 0 {
        return Err("four-wall holonomy is not flat");
    }
    let (a, b, c) = (3i64, 5, 8);
    let left = (a + b) + c;
    let right = a + (b + c);
    if left != right {
        return Err("operad composition is not associative");
    }
    Ok(left)
}

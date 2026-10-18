
pub fn separates_future_divergent_pairs(
    futures: &[u8],
    sensor_outputs: &[Vec<u8>],
    selected_sensors: &[usize],
) -> bool {
    let n = futures.len();
    for i in 0..n {
        for j in (i + 1)..n {
            if futures[i] != futures[j] {
                let separated = selected_sensors
                    .iter()
                    .any(|&s| sensor_outputs[s][i] != sensor_outputs[s][j]);
                if !separated {
                    return false;
                }
            }
        }
    }
    true
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_future_distinction_coverage_and_savings() {
        let futures = [0u8, 1, 2];
        let sensors = vec![
            vec![0u8, 0, 1],
            vec![0u8, 1, 1],
            vec![0u8, 1, 2],
        ];
        assert!(separates_future_divergent_pairs(&futures, &sensors, &[2]));
        assert!(!separates_future_divergent_pairs(&futures, &sensors, &[0]));
    }
}

pub fn verify_day_5_campaign(
    fuel_cap: u32,
    reset_fuel_between_episodes: bool,
    retain_raw_proposals: bool,
    corrupt_crt_residue: bool,
) -> Result<(u32, u32, [u32; 4]), &'static str> {
    if reset_fuel_between_episodes {
        return Err("fuel ledger reset between episodes refused");
    }
    if !retain_raw_proposals {
        return Err("omitting raw proposal retention refused");
    }
    let spent = 6_u32 + 5 + 3;
    if spent > fuel_cap {
        return Err("campaign fuel spend exceeded cap");
    }

    let mut residues = [0_u32; 4];
    for idx in 0..4 {
        let n = (idx + 1) as u32;
        let mod_2n = 2_u32.pow(n);
        let mod_3n = 3_u32.pow(n);
        let mod_6n = 6_u32.pow(n);
        let mut found = 0_u32;
        for a in 0..mod_6n {
            if a % mod_2n == 0 && a % mod_3n == 1 {
                found = a;
                break;
            }
        }
        if corrupt_crt_residue {
            found += 1;
        }
        if found % mod_2n != 0 || found % mod_3n != 1 {
            return Err("CRT residue failed mod 2^n / 3^n congruences");
        }
        residues[idx] = found;
    }

    Ok((spent, fuel_cap - spent, residues))
}

#[test]
fn plan_7d_day_5_witness_and_controls() {
    let (spent, rem, residues) =
        verify_day_5_campaign(20, false, true, false).expect("valid Day 5 campaign passes");
    assert_eq!(spent, 14);
    assert_eq!(rem, 6);
    assert_eq!(residues, [4, 28, 136, 1216]);

    assert!(verify_day_5_campaign(20, true, true, false).is_err());
    assert!(verify_day_5_campaign(20, false, false, false).is_err());
    assert!(verify_day_5_campaign(20, false, true, true).is_err());
    assert!(verify_day_5_campaign(10, false, true, false).is_err());
}

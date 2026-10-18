//! The MUB(6) claim firewall shared by every omega_native report.
//!
//! Each report carries this line and declares no authority effect, so the
//! text lives here once instead of in every module.

pub const FIREWALL: &str = "stated region only; mints no authority";
pub const AUTHORITY_EFFECT: &str = "None";

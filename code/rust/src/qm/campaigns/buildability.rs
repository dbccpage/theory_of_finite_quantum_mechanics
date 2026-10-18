// AuthorityEffect: None.

//! The buildability set `S` of a declared finite architecture.
//!
//! An architecture declares exact rates `lambda_gen`, `mu_rep`, `eps_mix`, a
//! logical floor `p_floor`, whether its correctable syndrome lies in the
//! reachability cone, and a U(1) connection on a finite carrier. The residual
//! after `n` repair cycles is `rho(n) = rho0 + n * step` with
//! `step = lambda_gen - mu_rep - eps_mix`.
//!
//! - `S1` (race): `step <= 0`. This is exactly the condition that
//!   `rho(n) <= rho0` for every `n`; when `step > 0` the first cycle exceeds `rho0`.
//! - `S2` (floor): `p_floor > 0`.
//! - `S3` (reachability): declared. Nothing here computes a Lieb–Robinson cone.
//! - `S4` (advantage): the declared connection is not gauge trivial, so some
//!   cycle carries holonomy that no vertex gauge removes.
//!
//! `S` is the conjunction. Apart from the race, the equivalence of a declared
//! "useful" predicate with `S` is a definition. A connection that does not fit
//! the declared carrier is refused. Nothing here says whether any device
//! satisfies `S`, and nothing links `S4` to classical simulability.

use num_traits::Signed;

use omega_number_theory::rational::Rational;
use omega_quantum_physics::u1_graph_connection::U1Connection;
use omega_solvers::data_cochain_packet::FiniteCochainPacket;

use omega_quantum_physics::holonomy_interference::{HolonomyInterferenceError, TreeGaugeFixing};

/// Declared generation, repair and mixing rates.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ResidualRace {
    lambda_gen: Rational,
    mu_rep: Rational,
    eps_mix: Rational,
}

impl ResidualRace {
    pub fn new(lambda_gen: Rational, mu_rep: Rational, eps_mix: Rational) -> Self {
        Self {
            lambda_gen,
            mu_rep,
            eps_mix,
        }
    }

    /// `lambda_gen - mu_rep - eps_mix`.
    pub fn step(&self) -> Rational {
        &self.lambda_gen - &self.mu_rep - &self.eps_mix
    }

    /// `rho(n) = rho0 + n * step`.
    pub fn residual_after(&self, rho0: &Rational, cycles: u64) -> Rational {
        rho0 + Rational::from_integer(cycles.into()) * self.step()
    }

    /// The first cycle whose residual exceeds `rho0`: cycle `1` when
    /// `step > 0`, and none otherwise.
    pub fn first_excess_cycle(&self) -> Option<u64> {
        self.step().is_positive().then_some(1)
    }
}

/// A declared architecture and its four conditions.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ArchitectureDeclaration {
    race: ResidualRace,
    p_floor: Rational,
    in_cone: bool,
    holonomy_resource: bool,
}

impl ArchitectureDeclaration {
    /// `S4` is computed from `connection` on `packet`; the rest is declared.
    pub fn new(
        race: ResidualRace,
        p_floor: Rational,
        in_cone: bool,
        packet: &FiniteCochainPacket,
        connection: &U1Connection,
    ) -> Result<Self, HolonomyInterferenceError> {
        let holonomy_resource = !TreeGaugeFixing::new(packet, connection)?.is_gauge_trivial();
        Ok(Self {
            race,
            p_floor,
            in_cone,
            holonomy_resource,
        })
    }

    /// `[S1, S2, S3, S4]`.
    pub fn conditions(&self) -> [bool; 4] {
        [
            !self.race.step().is_positive(),
            self.p_floor.is_positive(),
            self.in_cone,
            self.holonomy_resource,
        ]
    }

    /// `S1 and S2 and S3 and S4`.
    pub fn satisfies_set_s(&self) -> bool {
        self.conditions().iter().all(|condition| *condition)
    }
}



use num_traits::Signed;

use engine_number_theory::rational::Rational;
use engine_quantum_physics::u1_graph_connection::U1Connection;
use engine_solvers::data_cochain_packet::FiniteCochainPacket;

use engine_quantum_physics::holonomy_interference::{HolonomyInterferenceError, TreeGaugeFixing};

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

    pub fn step(&self) -> Rational {
        &self.lambda_gen - &self.mu_rep - &self.eps_mix
    }

    pub fn residual_after(&self, rho0: &Rational, cycles: u64) -> Rational {
        rho0 + Rational::from_integer(cycles.into()) * self.step()
    }

    pub fn first_excess_cycle(&self) -> Option<u64> {
        self.step().is_positive().then_some(1)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ArchitectureDeclaration {
    race: ResidualRace,
    p_floor: Rational,
    in_cone: bool,
    holonomy_resource: bool,
}

impl ArchitectureDeclaration {
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

    pub fn conditions(&self) -> [bool; 4] {
        [
            !self.race.step().is_positive(),
            self.p_floor.is_positive(),
            self.in_cone,
            self.holonomy_resource,
        ]
    }

    pub fn satisfies_set_s(&self) -> bool {
        self.conditions().iter().all(|condition| *condition)
    }
}

//! The score vocabulary of `SCORING.md`: capability levels, engineering grades,
//! gates, score tokens, the weakest-link composite and the acceptance floor.
//!
//! Every type here is a closed enumeration or a pair of them, so an invalid
//! level, grade, gate or token cannot be constructed; parsing is the only way
//! in from text and it fails with a typed [`ScoreError`].
//!
//! Cost: every operation is O(1) except [`GateGrades::unassessed`] (at most five gates).

use std::fmt;
use std::str::FromStr;

/// Capability level `L1`..`L5` (SCORING.md section 2). Ordered `L1 < ... < L5`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Level {
    /// Script trainee or single utility.
    L1,
    /// Coursework or standard idioms.
    L2,
    /// Research grade, bounded domain.
    L3,
    /// Senior professional, production craft.
    L4,
    /// Principal fellow, foundational architecture.
    L5,
}

impl Level {
    /// Every level in ascending order.
    pub const ALL: [Level; 5] = [Level::L1, Level::L2, Level::L3, Level::L4, Level::L5];

    /// The spelling used in score records and tokens.
    pub fn as_str(self) -> &'static str {
        match self {
            Level::L1 => "L1",
            Level::L2 => "L2",
            Level::L3 => "L3",
            Level::L4 => "L4",
            Level::L5 => "L5",
        }
    }
}

impl FromStr for Level {
    type Err = ScoreError;

    fn from_str(text: &str) -> Result<Self, Self::Err> {
        Level::ALL
            .into_iter()
            .find(|level| level.as_str() == text)
            .ok_or_else(|| ScoreError::UnknownLevel(text.to_owned()))
    }
}

impl fmt::Display for Level {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

/// Engineering grade (SCORING.md section 1.2), ordered `E < D < C < B < A < A+`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Grade {
    /// Demonstrated defect.
    E,
    /// Required mechanism or evidence shown absent.
    D,
    /// Core invariants preserved on the primary path.
    C,
    /// Comprehensive edge cases and negative tests.
    B,
    /// Substantive challenge and complete alignment.
    A,
    /// `A` plus independent replay; spelled `A+`.
    APlus,
}

impl Grade {
    /// Every grade in ascending order.
    pub const ALL: [Grade; 6] = [Grade::E, Grade::D, Grade::C, Grade::B, Grade::A, Grade::APlus];

    /// The spelling used in score records and tokens.
    pub fn as_str(self) -> &'static str {
        match self {
            Grade::E => "E",
            Grade::D => "D",
            Grade::C => "C",
            Grade::B => "B",
            Grade::A => "A",
            Grade::APlus => "A+",
        }
    }
}

impl FromStr for Grade {
    type Err = ScoreError;

    fn from_str(text: &str) -> Result<Self, Self::Err> {
        Grade::ALL
            .into_iter()
            .find(|grade| grade.as_str() == text)
            .ok_or_else(|| ScoreError::UnknownGrade(text.to_owned()))
    }
}

impl fmt::Display for Grade {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

/// One of the five sovereign gates (SCORING.md section 1.3).
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Gate {
    /// Provenance, claim mapping and authority.
    G1,
    /// Semantic correctness and numeric discipline.
    G2,
    /// Failure behaviour, safety and trusted computation.
    G3,
    /// Verification adequacy and mutation accounting.
    G4,
    /// Structure, cognitive complexity and operational cost.
    G5,
}

impl Gate {
    /// Every gate in order.
    pub const ALL: [Gate; 5] = [Gate::G1, Gate::G2, Gate::G3, Gate::G4, Gate::G5];

    /// The key used for this gate in score records.
    pub fn as_str(self) -> &'static str {
        match self {
            Gate::G1 => "G1",
            Gate::G2 => "G2",
            Gate::G3 => "G3",
            Gate::G4 => "G4",
            Gate::G5 => "G5",
        }
    }
}

impl FromStr for Gate {
    type Err = ScoreError;

    fn from_str(text: &str) -> Result<Self, Self::Err> {
        Gate::ALL
            .into_iter()
            .find(|gate| gate.as_str() == text)
            .ok_or_else(|| ScoreError::UnknownGate(text.to_owned()))
    }
}

impl fmt::Display for Gate {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

/// A completed score token `L<level><grade>`, for example `L4C` or `L5A+`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ScoreToken {
    /// Capability level.
    pub level: Level,
    /// Composite engineering grade.
    pub grade: Grade,
}

impl ScoreToken {
    /// Build a token from its two axes.
    pub fn new(level: Level, grade: Grade) -> Self {
        ScoreToken { level, grade }
    }
}

impl FromStr for ScoreToken {
    type Err = ScoreError;

    /// Accept exactly `L1`..`L5` followed by one grade spelling; nothing else
    /// (no whitespace, no lower case, no `A-` or `B+`).
    fn from_str(text: &str) -> Result<Self, Self::Err> {
        let malformed = || ScoreError::MalformedToken(text.to_owned());
        let level_text = text.get(..2).ok_or_else(malformed)?;
        let grade_text = text.get(2..).ok_or_else(malformed)?;
        let level = level_text.parse::<Level>().map_err(|_| malformed())?;
        let grade = grade_text.parse::<Grade>().map_err(|_| malformed())?;
        Ok(ScoreToken { level, grade })
    }
}

impl fmt::Display for ScoreToken {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}{}", self.level, self.grade)
    }
}

/// The five gate grades of one assessment; `None` is an unassessed gate.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct GateGrades {
    g1: Option<Grade>,
    g2: Option<Grade>,
    g3: Option<Grade>,
    g4: Option<Grade>,
    g5: Option<Grade>,
}

impl GateGrades {
    /// Grades in gate order `G1..G5`.
    pub fn new(grades: [Option<Grade>; 5]) -> Self {
        let [g1, g2, g3, g4, g5] = grades;
        GateGrades { g1, g2, g3, g4, g5 }
    }

    /// The grade of one gate, or `None` when it is unassessed.
    pub fn get(&self, gate: Gate) -> Option<Grade> {
        match gate {
            Gate::G1 => self.g1,
            Gate::G2 => self.g2,
            Gate::G3 => self.g3,
            Gate::G4 => self.g4,
            Gate::G5 => self.g5,
        }
    }

    /// Gates with no grade.
    pub fn unassessed(&self) -> Vec<Gate> {
        Gate::ALL.into_iter().filter(|gate| self.get(*gate).is_none()).collect()
    }

    /// True when all five gates carry a grade.
    pub fn is_complete(&self) -> bool {
        self.unassessed().is_empty()
    }

    /// The minimum over the assessed gates (the known ceiling), if any is assessed.
    pub fn ceiling(&self) -> Option<Grade> {
        Gate::ALL.into_iter().filter_map(|gate| self.get(gate)).min()
    }

    /// The composite grade under the fail-closed weakest-link rule (section 1.2)
    /// and the unassessed discipline (section 1.4): the minimum of all five gates
    /// when complete; `E` whenever a known `E` exists, even with unassessed gates;
    /// otherwise `None`.
    pub fn composite(&self) -> Option<Grade> {
        let ceiling = self.ceiling();
        if self.is_complete() || ceiling == Some(Grade::E) {
            ceiling
        } else {
            None
        }
    }
}

/// The acceptance floor: a minimum level and a minimum composite grade.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Floor {
    /// Lowest admitted capability level.
    pub min_level: Level,
    /// Lowest admitted composite grade.
    pub min_grade: Grade,
}

impl Floor {
    /// True when the token meets both axes of the floor.
    pub fn admits(&self, token: ScoreToken) -> bool {
        token.level >= self.min_level && token.grade >= self.min_grade
    }
}

impl fmt::Display for Floor {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "level >= {} and grade >= {}", self.min_level, self.min_grade)
    }
}

/// A failure to read score vocabulary from text.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ScoreError {
    /// Not one of `L1`..`L5`.
    UnknownLevel(String),
    /// Not one of `E D C B A A+`.
    UnknownGrade(String),
    /// Not one of `G1`..`G5`.
    UnknownGate(String),
    /// Not `L<level><grade>`.
    MalformedToken(String),
}

impl fmt::Display for ScoreError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ScoreError::UnknownLevel(text) => write!(f, "unknown capability level {text:?} (expected L1..L5)"),
            ScoreError::UnknownGrade(text) => write!(f, "unknown grade {text:?} (expected E, D, C, B, A or A+)"),
            ScoreError::UnknownGate(text) => write!(f, "unknown gate {text:?} (expected G1..G5)"),
            ScoreError::MalformedToken(text) => write!(f, "malformed score token {text:?} (expected L<level><grade>, e.g. L4C)"),
        }
    }
}

impl std::error::Error for ScoreError {}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used, clippy::indexing_slicing, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn grade_order_matches_scoring_md() {
        let ordered: Vec<&str> = Grade::ALL.iter().map(|g| g.as_str()).collect();
        assert_eq!(ordered, ["E", "D", "C", "B", "A", "A+"]);
        for pair in Grade::ALL.windows(2) {
            assert!(pair[0] < pair[1], "{} < {}", pair[0], pair[1]);
        }
        assert!(Grade::E < Grade::D && Grade::A < Grade::APlus);
    }

    #[test]
    fn level_order_is_numeric() {
        for pair in Level::ALL.windows(2) {
            assert!(pair[0] < pair[1]);
        }
        assert!(Level::L3 < Level::L4);
    }

    #[test]
    fn every_token_round_trips() {
        let mut count = 0;
        for level in Level::ALL {
            for grade in Grade::ALL {
                let token = ScoreToken::new(level, grade);
                let text = token.to_string();
                assert_eq!(text.parse::<ScoreToken>().unwrap(), token);
                count += 1;
            }
        }
        assert_eq!(count, 30);
        assert_eq!("L5A+".parse::<ScoreToken>().unwrap(), ScoreToken::new(Level::L5, Grade::APlus));
        assert_eq!("L4C".parse::<ScoreToken>().unwrap().to_string(), "L4C");
    }

    #[test]
    fn malformed_tokens_are_rejected() {
        for bad in ["", "L", "L4", "4C", "l4c", "L4c", "L6A", "L0A", "L4A-", "L4B+", "L4 C", " L4C", "L4C ", "L4AA", "L44C", "LL4C", "L4é", "é"] {
            assert_eq!(bad.parse::<ScoreToken>(), Err(ScoreError::MalformedToken(bad.to_owned())), "{bad:?}");
        }
    }

    #[test]
    fn vocabulary_parse_errors_are_typed() {
        assert_eq!("L9".parse::<Level>(), Err(ScoreError::UnknownLevel("L9".into())));
        assert_eq!("F".parse::<Grade>(), Err(ScoreError::UnknownGrade("F".into())));
        assert_eq!("G6".parse::<Gate>(), Err(ScoreError::UnknownGate("G6".into())));
        assert_eq!("A+".parse::<Grade>(), Ok(Grade::APlus));
        assert_eq!("G3".parse::<Gate>(), Ok(Gate::G3));
        for gate in Gate::ALL {
            assert_eq!(gate.to_string().parse::<Gate>(), Ok(gate));
        }
        for level in Level::ALL {
            assert_eq!(level.to_string().parse::<Level>(), Ok(level));
        }
        assert!(ScoreError::MalformedToken("x".into()).to_string().contains("L<level><grade>"));
        assert!(ScoreError::UnknownGate("x".into()).to_string().contains("G1..G5"));
        assert!(ScoreError::UnknownLevel("x".into()).to_string().contains("L1..L5"));
        assert!(ScoreError::UnknownGrade("x".into()).to_string().contains("A+"));
    }

    #[test]
    fn composite_is_the_minimum_of_complete_gates() {
        let g = GateGrades::new([Some(Grade::A), Some(Grade::B), Some(Grade::C), Some(Grade::APlus), Some(Grade::B)]);
        assert_eq!(g.composite(), Some(Grade::C));
        assert!(g.is_complete());
        // Exhaustive check of min over a two-grade sweep at each gate position.
        for gate in Gate::ALL {
            for low in Grade::ALL {
                let mut grades = [Some(Grade::APlus); 5];
                grades[gate as usize] = Some(low);
                let g = GateGrades::new(grades);
                assert_eq!(g.composite(), Some(low));
                assert_eq!(g.get(gate), Some(low));
            }
        }
    }

    #[test]
    fn unassessed_gate_gives_no_composite_unless_a_known_e() {
        let g = GateGrades::new([Some(Grade::A), Some(Grade::A), Some(Grade::B), None, Some(Grade::A)]);
        assert_eq!(g.composite(), None);
        assert_eq!(g.ceiling(), Some(Grade::B));
        assert_eq!(g.unassessed(), vec![Gate::G4]);
        assert!(!g.is_complete());
        // Section 1.4 / scenario 4: a known E stays visible.
        let e = GateGrades::new([Some(Grade::B), Some(Grade::B), Some(Grade::E), None, Some(Grade::B)]);
        assert_eq!(e.composite(), Some(Grade::E));
        let none = GateGrades::default();
        assert_eq!(none.composite(), None);
        assert_eq!(none.ceiling(), None);
        assert_eq!(none.unassessed().len(), 5);
    }

    #[test]
    fn floor_cases() {
        let floor = Floor { min_level: Level::L4, min_grade: Grade::D };
        let t = |s: &str| s.parse::<ScoreToken>().unwrap();
        assert!(floor.admits(t("L4D")));
        assert!(floor.admits(t("L5A+")));
        assert!(floor.admits(t("L4C")));
        assert!(!floor.admits(t("L4E")));
        assert!(!floor.admits(t("L3A")));
        assert!(!floor.admits(t("L3A+")));
        assert!(!floor.admits(t("L5E")));
        let admitted = Level::ALL
            .iter()
            .flat_map(|l| Grade::ALL.iter().map(move |g| ScoreToken::new(*l, *g)))
            .filter(|tok| floor.admits(*tok))
            .count();
        assert_eq!(admitted, 2 * 5);
        assert_eq!(floor.to_string(), "level >= L4 and grade >= D");
    }
}

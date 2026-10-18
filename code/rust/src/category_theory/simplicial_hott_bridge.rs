//! Bridge finite nerves and rewrite paths to HoTT path witnesses.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SimplicialPathWitness {
    pub simplex: String,
    pub hott_path: String,
    pub coherence_cells: Vec<String>,
}

impl SimplicialPathWitness {
    pub fn new(simplex: &str, hott_path: &str) -> Self {
        Self {
            simplex: simplex.into(),
            hott_path: hott_path.into(),
            coherence_cells: Vec::new(),
        }
    }

    pub fn is_coherent_at_level(&self, level: usize) -> bool {
        self.coherence_cells.len() >= level
    }
}

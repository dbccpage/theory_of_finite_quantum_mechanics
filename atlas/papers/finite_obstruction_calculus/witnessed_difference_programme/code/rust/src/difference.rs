// Executable finite evidence; AuthorityEffect: None.
use std::collections::BTreeSet;
use serde::{Deserialize, Serialize};
use crate::error::WdpError;

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct Mark(pub String);

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Carrier {
    pub marks: BTreeSet<Mark>,
}

impl Carrier {
    pub fn new(marks: Vec<String>) -> Result<Self, WdpError> {
        let mut set = BTreeSet::new();
        for m in marks {
            if m.is_empty() {
                return Err(WdpError::InvalidInput {
                    detail: "Empty mark cannot be admitted without constructor".to_string(),
                });
            }
            set.insert(Mark(m));
        }
        Ok(Self { marks: set })
    }

    pub fn size(&self) -> usize {
        self.marks.len()
    }

    pub fn contains(&self, mark: &str) -> bool {
        self.marks.contains(&Mark(mark.to_string()))
    }

    pub fn difference(&self, other: &Self) -> BTreeSet<Mark> {
        self.marks.difference(&other.marks).cloned().collect()
    }
}


use std::fmt;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub struct OperadColour {
    name: String,
}

impl OperadColour {
    pub fn new(name: impl Into<String>) -> Result<Self, String> {
        let n = name.into();
        let trimmed = n.trim();
        if trimmed.is_empty() {
            return Err("OperadColour name cannot be empty or whitespace only.".to_string());
        }
        Ok(Self {
            name: trimmed.to_string(),
        })
    }

    pub fn as_str(&self) -> &str {
        &self.name
    }
}

impl fmt::Display for OperadColour {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.name)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct OperadSignature {
    pub inputs: Vec<OperadColour>,
    pub output: OperadColour,
}

impl OperadSignature {
    pub fn new(inputs: Vec<OperadColour>, output: OperadColour) -> Self {
        Self { inputs, output }
    }

    pub fn arity(&self) -> usize {
        self.inputs.len()
    }

    pub fn is_nullary(&self) -> bool {
        self.inputs.is_empty()
    }

    pub fn is_unary(&self) -> bool {
        self.inputs.len() == 1
    }
}

impl fmt::Display for OperadSignature {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let ins: Vec<&str> = self.inputs.iter().map(|c| c.as_str()).collect();
        write!(f, "({}) -> {}", ins.join(", "), self.output)
    }
}

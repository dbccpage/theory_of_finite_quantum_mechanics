use crate::error::HomologyError;
use crate::hash::Blake3Hash;
use linear_algebra::backend::basic_matrix::{BasicMatrix, CheckedNumeric};
use num_traits::Zero;

/// Cryptographically bound witness proving that a sequence of linear maps
/// is a lawful chain map $f: C \to D$, satisfying $d^D \circ f = f \circ d^C$.
// Sealed witness (PO-AUTH-NC): `_private: ()` blocks external literal construction.
#[allow(clippy::manual_non_exhaustive)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChainMapWitness {
    pub source_complex_hash: [u8; 32],
    pub target_complex_hash: [u8; 32],
    pub map_hashes: Vec<[u8; 32]>,
    _private: (),
}

impl ChainMapWitness {
    pub(crate) fn new(
        source_complex_hash: [u8; 32],
        target_complex_hash: [u8; 32],
        map_hashes: Vec<[u8; 32]>,
    ) -> Self {
        Self {
            source_complex_hash,
            target_complex_hash,
            map_hashes,
            _private: (),
        }
    }
}

/// A certified chain map between two verified chain complexes.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CertifiedChainMap<K> {
    maps: Vec<BasicMatrix<K>>,
    witness: ChainMapWitness,
}

pub trait FiniteChainComplexView<K> {
    fn boundaries(&self) -> &[BasicMatrix<K>];
    fn complex_hash_bytes(&self) -> [u8; 32];
}

impl<K: CheckedNumeric + Zero + PartialEq + Clone + serde::Serialize> CertifiedChainMap<K> {
    pub fn new_checked<C, D>(
        maps: Vec<BasicMatrix<K>>,
        source: &C,
        target: &D,
    ) -> Result<Self, HomologyError>
    where
        C: FiniteChainComplexView<K>,
        D: FiniteChainComplexView<K>,
    {
        if maps.len() != source.boundaries().len() + 1 {
            return Err(HomologyError::DimensionMismatch {
                left: source.boundaries().len() + 1,
                right: maps.len(),
            });
        }

        let mut map_hashes = Vec::with_capacity(maps.len());

        for k in 0..maps.len() {
            let f_k = &maps[k];

            if k > 0 {
                let d_c_k = source
                    .boundaries()
                    .get(k - 1)
                    .ok_or(HomologyError::VerificationUnavailable)?;
                let d_d_k = target
                    .boundaries()
                    .get(k - 1)
                    .ok_or(HomologyError::VerificationUnavailable)?;

                let left = d_d_k
                    .checked_mul(f_k)
                    .map_err(|_| HomologyError::VerificationUnavailable)?;
                let right = maps[k - 1]
                    .checked_mul(d_c_k)
                    .map_err(|_| HomologyError::VerificationUnavailable)?;

                if left != right {
                    return Err(HomologyError::NotAChainMap);
                }
            }

            // Compute canonical map hash
            let mut data = Vec::new();
            data.extend_from_slice(&k.to_le_bytes());
            let entries = serde_json::to_vec(f_k.as_slice()).unwrap_or_default();
            data.extend_from_slice(&entries);
            map_hashes.push(Blake3Hash::new(&data).0);
        }

        Ok(Self {
            maps,
            witness: ChainMapWitness::new(
                source.complex_hash_bytes(),
                target.complex_hash_bytes(),
                map_hashes,
            ),
        })
    }

    pub fn maps(&self) -> &[BasicMatrix<K>] {
        &self.maps
    }

    pub fn witness(&self) -> &ChainMapWitness {
        &self.witness
    }
}

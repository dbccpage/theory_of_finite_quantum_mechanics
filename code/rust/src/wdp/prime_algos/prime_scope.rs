
use engine_kernel::evidence::Hash256;
use serde::Serialize;
use sha2::{Digest, Sha256};
use std::fmt;

const COMMIT_DOMAIN: &str = "oeprm.scope.v1";

pub fn digest(domain: &str, parts: &[&[u8]]) -> Hash256 {
    let mut h = Sha256::new();
    h.update(domain.as_bytes());
    for p in parts {
        h.update((p.len() as u64).to_le_bytes());
        h.update(p);
    }
    let mut out = [0u8; 32];
    out.copy_from_slice(&h.finalize());
    Hash256(out)
}

pub fn short(h: &Hash256) -> String {
    h.0.iter().take(6).map(|b| format!("{b:02x}")).collect()
}

const MANIFEST_DOMAIN: &str = "oeprm.manifest.v1";

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct BoundCarrierManifest {
    carrier: Hash256,
    d0: Hash256,
}

impl BoundCarrierManifest {
    pub fn new(carrier: Hash256, d0: Hash256) -> Self {
        Self { carrier, d0 }
    }

    pub fn carrier(&self) -> &Hash256 {
        &self.carrier
    }

    pub fn d0(&self) -> &Hash256 {
        &self.d0
    }

    pub fn commit(&self) -> Hash256 {
        digest(MANIFEST_DOMAIN, &[&self.carrier.0, &self.d0.0])
    }
}

impl fmt::Display for BoundCarrierManifest {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "carrier {} d0 {}", short(&self.carrier), short(&self.d0))
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CallerAttested<T> {
    inner: T,
    authority: engine_types::authority::AuthorityEffect,
}

impl<T> CallerAttested<T> {
    pub fn new(inner: T) -> Self {
        Self {
            inner,
            authority: engine_types::authority::AuthorityEffect::None,
        }
    }

    pub fn value(&self) -> &T {
        &self.inner
    }

    pub fn inner(&self) -> &T {
        &self.inner
    }

    pub fn into_inner(self) -> T {
        self.inner
    }

    pub fn authority(&self) -> engine_types::authority::AuthorityEffect {
        engine_types::authority::AuthorityEffect::None
    }
}

impl<T: fmt::Display> fmt::Display for CallerAttested<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "CallerAttested({})", self.inner)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ScopeBinding {
    run: Hash256,
    carrier_manifest: BoundCarrierManifest,
    residual: Hash256,
    tape_head: Option<Hash256>,
    step_index: usize,
}

impl ScopeBinding {
    pub fn new(
        run: Hash256,
        carrier_manifest: BoundCarrierManifest,
        residual: Hash256,
        tape_head: Option<Hash256>,
        step_index: usize,
    ) -> Self {
        Self {
            run,
            carrier_manifest,
            residual,
            tape_head,
            step_index,
        }
    }

    pub fn with_carrier_and_d0(
        run: Hash256,
        carrier: Hash256,
        d0: Hash256,
        residual: Hash256,
        tape_head: Option<Hash256>,
        step_index: usize,
    ) -> Self {
        Self::new(
            run,
            BoundCarrierManifest::new(carrier, d0),
            residual,
            tape_head,
            step_index,
        )
    }

    pub fn run(&self) -> &Hash256 {
        &self.run
    }
    pub fn carrier_manifest(&self) -> &BoundCarrierManifest {
        &self.carrier_manifest
    }
    pub fn carrier(&self) -> &Hash256 {
        self.carrier_manifest.carrier()
    }
    pub fn d0(&self) -> &Hash256 {
        self.carrier_manifest.d0()
    }
    pub fn residual(&self) -> &Hash256 {
        &self.residual
    }
    pub fn tape_head(&self) -> Option<&Hash256> {
        self.tape_head.as_ref()
    }
    pub fn step_index(&self) -> usize {
        self.step_index
    }

    pub fn commit(&self) -> Hash256 {
        let empty: [u8; 0] = [];
        digest(
            COMMIT_DOMAIN,
            &[
                &self.run.0,
                &self.carrier_manifest.commit().0,
                &self.residual.0,
                self.tape_head.as_ref().map_or(&empty[..], |h| &h.0[..]),
                &(self.step_index as u64).to_le_bytes(),
            ],
        )
    }

    pub fn same_subject(&self, other: &ScopeBinding) -> bool {
        self.run == other.run
            && self.carrier_manifest == other.carrier_manifest
            && self.residual == other.residual
            && self.tape_head == other.tape_head
    }
}

impl fmt::Display for ScopeBinding {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "run {} manifest [{}] residual {} head {} step {}",
            short(&self.run),
            self.carrier_manifest,
            short(&self.residual),
            self.tape_head.as_ref().map_or("-".into(), short),
            self.step_index
        )
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ScopeMismatch {
    pub what: &'static str,
    pub expected: String,
    pub found: String,
}

impl fmt::Display for ScopeMismatch {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{} bound to [{}] but presented at [{}]",
            self.what, self.found, self.expected
        )
    }
}

impl std::error::Error for ScopeMismatch {}

pub fn require_same_scope(
    what: &'static str,
    evidence: &ScopeBinding,
    site: &ScopeBinding,
) -> Result<(), ScopeMismatch> {
    if evidence.same_subject(site) && evidence.step_index == site.step_index {
        Ok(())
    } else {
        Err(ScopeMismatch {
            what,
            expected: site.to_string(),
            found: evidence.to_string(),
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn h(n: u8) -> Hash256 {
        Hash256([n; 32])
    }

    fn scope(step: usize) -> ScopeBinding {
        ScopeBinding::with_carrier_and_d0(h(1), h(2), h(20), h(3), Some(h(4)), step)
    }

    #[test]
    fn a_binding_commits_to_every_field() {
        let base = scope(0);
        let variants = [
            ScopeBinding::with_carrier_and_d0(h(9), h(2), h(20), h(3), Some(h(4)), 0),
            ScopeBinding::with_carrier_and_d0(h(1), h(9), h(20), h(3), Some(h(4)), 0),
            ScopeBinding::with_carrier_and_d0(h(1), h(2), h(99), h(3), Some(h(4)), 0),
            ScopeBinding::with_carrier_and_d0(h(1), h(2), h(20), h(9), Some(h(4)), 0),
            ScopeBinding::with_carrier_and_d0(h(1), h(2), h(20), h(3), Some(h(9)), 0),
            ScopeBinding::with_carrier_and_d0(h(1), h(2), h(20), h(3), None, 0),
            ScopeBinding::with_carrier_and_d0(h(1), h(2), h(20), h(3), Some(h(4)), 1),
        ];
        for v in variants {
            assert_ne!(
                base.commit(),
                v.commit(),
                "changing any bound field must change the commitment"
            );
        }
    }

    #[test]
    fn independently_built_equal_bindings_commit_identically() {
        let built_here = ScopeBinding::with_carrier_and_d0(
            Hash256([1; 32]),
            Hash256([2; 32]),
            Hash256([20; 32]),
            Hash256([3; 32]),
            Some(Hash256([4; 32])),
            7,
        );
        let built_by_helper = scope(7);
        assert_eq!(built_here, built_by_helper, "the fixtures must agree first");
        assert_eq!(built_here.commit(), built_by_helper.commit());
    }

    #[test]
    fn concatenation_ambiguity_is_impossible() {
        assert_ne!(
            digest("d", &[b"ab", b"c"]),
            digest("d", &[b"a", b"bc"]),
            "unprefixed concatenation would collide these"
        );
    }

    #[test]
    fn domain_separation_is_effective() {
        assert_ne!(digest("a", &[b"x"]), digest("b", &[b"x"]));
    }

    #[test]
    fn evidence_for_another_residual_is_rejected() {
        let site = scope(0);
        let elsewhere = ScopeBinding::with_carrier_and_d0(h(1), h(2), h(20), h(99), Some(h(4)), 0);
        let err = require_same_scope("lift admission", &elsewhere, &site)
            .expect_err("a permit for residual A must not be usable at residual B");
        assert_eq!(err.what, "lift admission");
    }

    #[test]
    fn evidence_for_another_step_is_rejected() {
        let site = scope(4);
        let stale = scope(3);
        require_same_scope("permit", &stale, &site)
            .expect_err("evidence from an earlier step must not be replayed");
    }

    #[test]
    fn matching_evidence_is_accepted() {
        require_same_scope("permit", &scope(2), &scope(2)).expect("same subject and step");
    }

    #[test]
    fn display_never_panics_on_any_byte_pattern() {
        for pattern in [0x00u8, 0x80, 0xC3, 0xFF] {
            let b = ScopeBinding::with_carrier_and_d0(
                Hash256([pattern; 32]),
                Hash256([pattern; 32]),
                Hash256([pattern; 32]),
                Hash256([pattern; 32]),
                Some(Hash256([pattern; 32])),
                0,
            );
            let s = b.to_string();
            assert!(!s.is_empty());
            assert_eq!(short(&Hash256([pattern; 32])).len(), 12);
        }
    }
}

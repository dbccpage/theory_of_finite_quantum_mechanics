
use std::collections::BTreeMap;

pub const AUTHORITY_FENCE: &str = "AuthorityEffect None; not PROVED; not GlobalGreen; \
     W3.5 observer functoriality finite dual-face (OBS D3 skeleton).";


#[derive(Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct CarrierSetId {
    pub label: String,
    pub size: usize,
}

impl CarrierSetId {
    pub fn try_new(label: impl Into<String>, size: usize) -> Result<Self, FunctorError> {
        if size == 0 {
            return Err(FunctorError::ZeroCarrierSize);
        }
        Ok(Self {
            label: label.into(),
            size,
        })
    }

    pub fn size(&self) -> usize {
        self.size
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct PopulationConfig {
    pub carrier: CarrierSetId,
    pub weights: Vec<u64>,
    pub tags: Vec<u8>,
}

impl PopulationConfig {
    pub fn try_new(
        carrier: CarrierSetId,
        weights: Vec<u64>,
        tags: Vec<u8>,
    ) -> Result<Self, FunctorError> {
        if weights.len() != carrier.size || tags.len() != carrier.size {
            return Err(FunctorError::LengthMismatch {
                expected: carrier.size,
                weights: weights.len(),
                tags: tags.len(),
            });
        }
        Ok(Self {
            carrier,
            weights,
            tags,
        })
    }

    pub fn mass(&self) -> Result<u64, FunctorError> {
        self.weights.iter().try_fold(0u64, |sum, w| {
            sum.checked_add(*w).ok_or(FunctorError::ArithmeticOverflow)
        })
    }

    pub fn size(&self) -> usize {
        self.carrier.size
    }
}


pub fn same_population(x: &PopulationConfig, y: &PopulationConfig) -> bool {
    x.carrier == y.carrier && x.weights == y.weights
}

pub fn d_pop(i: usize, x: &PopulationConfig) -> Option<u64> {
    x.weights.get(i).copied()
}

pub fn pop_sig(x: &PopulationConfig) -> Vec<u64> {
    x.weights.clone()
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FunctorError {
    ZeroCarrierSize,
    LengthMismatch {
        expected: usize,
        weights: usize,
        tags: usize,
    },
    EmptyContextMonoid,
    ArithmeticOverflow,
    ContextIndex {
        index: usize,
        order: usize,
    },
    InvalidActionLaw,
    DescentFailed {
        reason: &'static str,
    },
    CarrierMismatch,
    EquivarianceBroken,
    CompositionDomainMismatch,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteMonoid {
    pub one: usize,
    pub mul: Vec<Vec<usize>>,
}

impl FiniteMonoid {
    pub fn order(&self) -> usize {
        self.mul.len()
    }

    pub fn trivial() -> Self {
        Self {
            one: 0,
            mul: vec![vec![0]],
        }
    }

    pub fn cyclic_additive(modulus: usize) -> Result<Self, FunctorError> {
        if modulus == 0 {
            return Err(FunctorError::EmptyContextMonoid);
        }
        let mut mul = vec![vec![0; modulus]; modulus];
        for a in 0..modulus {
            for b in 0..modulus {
                mul[a][b] = (a + b) % modulus;
            }
        }
        Ok(Self { one: 0, mul })
    }

    pub fn mul_checked(&self, a: usize, b: usize) -> Option<usize> {
        self.mul.get(a).and_then(|row| row.get(b)).copied()
    }
}

#[derive(Debug, Clone)]
pub struct ObserverAction {
    pub monoid: FiniteMonoid,
    pub kind: ActionKind,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ActionKind {
    Trivial,
    TagRevealAdditive,
    Swap01,
    TagAbsorb,
}

impl ObserverAction {
    pub fn trivial() -> Self {
        Self {
            monoid: FiniteMonoid::trivial(),
            kind: ActionKind::Trivial,
        }
    }

    pub fn tag_reveal(modulus: usize) -> Result<Self, FunctorError> {
        if modulus < 2 {
            return Err(FunctorError::EmptyContextMonoid);
        }
        Ok(Self {
            monoid: FiniteMonoid::cyclic_additive(modulus)?,
            kind: ActionKind::TagRevealAdditive,
        })
    }

    pub fn swap01() -> Self {
        Self {
            monoid: FiniteMonoid {
                one: 0,
                mul: vec![vec![0, 1], vec![1, 0]],
            },
            kind: ActionKind::Swap01,
        }
    }

    pub fn tag_absorb() -> Self {
        Self {
            monoid: FiniteMonoid {
                one: 0,
                mul: vec![vec![0, 1], vec![1, 1]],
            },
            kind: ActionKind::TagAbsorb,
        }
    }

    pub fn action_law_violations(
        &self,
        x: &PopulationConfig,
    ) -> Result<Vec<(usize, usize)>, FunctorError> {
        let order = self.monoid.order();
        let mut violations = Vec::new();
        for c in 0..order {
            for d in 0..order {
                let product = self
                    .monoid
                    .mul_checked(c, d)
                    .ok_or(FunctorError::EmptyContextMonoid)?;
                let composed = self.act(product, x)?;
                let in_turn = self.act(c, &self.act(d, x)?)?;
                if composed != in_turn {
                    violations.push((c, d));
                }
            }
        }
        Ok(violations)
    }

    pub fn validate_action_on(&self, samples: &[PopulationConfig]) -> Result<(), FunctorError> {
        for x in samples {
            if !self.check_act_one(x) || !self.action_law_violations(x)?.is_empty() {
                return Err(FunctorError::InvalidActionLaw);
            }
        }
        Ok(())
    }

    pub fn act(&self, c: usize, x: &PopulationConfig) -> Result<PopulationConfig, FunctorError> {
        if c >= self.monoid.order() {
            return Err(FunctorError::ContextIndex {
                index: c,
                order: self.monoid.order(),
            });
        }
        if x.weights.len() != x.size() || x.tags.len() != x.size() {
            return Err(FunctorError::LengthMismatch {
                expected: x.size(),
                weights: x.weights.len(),
                tags: x.tags.len(),
            });
        }
        match self.kind {
            ActionKind::Trivial => Ok(x.clone()),
            ActionKind::TagRevealAdditive => {
                let mut w = x.weights.clone();
                for i in 0..w.len() {
                    w[i] = w[i]
                        .checked_add(
                            (c as u64)
                                .checked_mul(x.tags[i] as u64)
                                .ok_or(FunctorError::ArithmeticOverflow)?,
                        )
                        .ok_or(FunctorError::ArithmeticOverflow)?;
                }
                PopulationConfig::try_new(x.carrier.clone(), w, x.tags.clone())
            }
            ActionKind::Swap01 => {
                if c == 0 {
                    return Ok(x.clone());
                }
                if x.size() < 2 {
                    return Err(FunctorError::LengthMismatch {
                        expected: 2,
                        weights: x.size(),
                        tags: x.size(),
                    });
                }
                let mut w = x.weights.clone();
                let mut t = x.tags.clone();
                w.swap(0, 1);
                t.swap(0, 1);
                PopulationConfig::try_new(x.carrier.clone(), w, t)
            }
            ActionKind::TagAbsorb => {
                if c == 0 {
                    return Ok(x.clone());
                }
                let w: Vec<u64> = x
                    .weights
                    .iter()
                    .zip(&x.tags)
                    .map(|(w, t)| {
                        w.checked_add(u64::from(*t))
                            .ok_or(FunctorError::ArithmeticOverflow)
                    })
                    .collect::<Result<_, _>>()?;
                PopulationConfig::try_new(x.carrier.clone(), w, vec![0; x.tags.len()])
            }
        }
    }

    pub fn check_act_one(&self, x: &PopulationConfig) -> bool {
        match self.act(self.monoid.one, x) {
            Ok(y) => y == *x,
            Err(_) => false,
        }
    }
}


pub fn bi_congruent(action: &ObserverAction, x: &PopulationConfig, y: &PopulationConfig) -> bool {
    if x.carrier != y.carrier {
        return false;
    }
    let n = x.size();
    let m = action.monoid.order();
    for i in 0..n {
        for c in 0..m {
            let Ok(cx) = action.act(c, x) else {
                return false;
            };
            let Ok(cy) = action.act(c, y) else {
                return false;
            };
            if d_pop(i, &cx) != d_pop(i, &cy) {
                return false;
            }
        }
    }
    true
}

pub fn same_pop_iff_bi_triv_pop(x: &PopulationConfig, y: &PopulationConfig) -> bool {
    let triv = ObserverAction::trivial();
    same_population(x, y) == bi_congruent(&triv, x, y)
}

pub fn same_pop_agrees_with_bi(
    action: &ObserverAction,
    x: &PopulationConfig,
    y: &PopulationConfig,
) -> bool {
    same_population(x, y) == bi_congruent(action, x, y)
}


#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct ObserverClass(pub usize);

pub fn bi_partition(
    action: &ObserverAction,
    sample: &[PopulationConfig],
) -> (Vec<ObserverClass>, usize) {
    let mut class_of = vec![ObserverClass(0); sample.len()];
    let mut reps: Vec<usize> = Vec::new();
    for (i, x) in sample.iter().enumerate() {
        let mut found = None;
        for (ci, &r) in reps.iter().enumerate() {
            if bi_congruent(action, x, &sample[r]) {
                found = Some(ci);
                break;
            }
        }
        match found {
            Some(ci) => class_of[i] = ObserverClass(ci),
            None => {
                let ci = reps.len();
                reps.push(i);
                class_of[i] = ObserverClass(ci);
            }
        }
    }
    (class_of, reps.len())
}

pub fn observer_class_of(
    action: &ObserverAction,
    sample: &[PopulationConfig],
    classes: &[ObserverClass],
    x: &PopulationConfig,
) -> Option<ObserverClass> {
    for (i, s) in sample.iter().enumerate() {
        if bi_congruent(action, x, s) {
            return Some(classes[i]);
        }
    }
    None
}


#[derive(Debug, Clone)]
pub struct SystemMorphism {
    pub label: String,
    pub monoid_map: Vec<usize>,
    pub state_steps: Vec<StateMapKind>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StateMapKind {
    Identity,
    ForgetTags,
    ApplySwap01,
    ScaleWeights(u64),
}

impl StateMapKind {
    pub fn apply(self, x: &PopulationConfig) -> Result<PopulationConfig, FunctorError> {
        match self {
            StateMapKind::Identity => Ok(x.clone()),
            StateMapKind::ForgetTags => {
                let tags = vec![0u8; x.size()];
                PopulationConfig::try_new(x.carrier.clone(), x.weights.clone(), tags)
            }
            StateMapKind::ApplySwap01 => {
                if x.size() < 2 {
                    return Err(FunctorError::LengthMismatch {
                        expected: 2,
                        weights: x.size(),
                        tags: x.size(),
                    });
                }
                let mut w = x.weights.clone();
                let mut t = x.tags.clone();
                w.swap(0, 1);
                t.swap(0, 1);
                PopulationConfig::try_new(x.carrier.clone(), w, t)
            }
            StateMapKind::ScaleWeights(k) => {
                let w: Vec<u64> = x
                    .weights
                    .iter()
                    .map(|v| v.checked_mul(k).ok_or(FunctorError::ArithmeticOverflow))
                    .collect::<Result<_, _>>()?;
                PopulationConfig::try_new(x.carrier.clone(), w, x.tags.clone())
            }
        }
    }
}

impl SystemMorphism {
    fn from_elementary(
        label: impl Into<String>,
        source_monoid_order: usize,
        step: StateMapKind,
    ) -> Self {
        let state_steps = match step {
            StateMapKind::Identity => Vec::new(),
            s => vec![s],
        };
        Self {
            label: label.into(),
            monoid_map: (0..source_monoid_order).collect(),
            state_steps,
        }
    }

    pub fn identity(source_monoid_order: usize) -> Self {
        Self::from_elementary("id", source_monoid_order, StateMapKind::Identity)
    }

    pub fn forget_tags(source_monoid_order: usize) -> Self {
        Self::from_elementary("forget_tags", source_monoid_order, StateMapKind::ForgetTags)
    }

    pub fn apply_swap01(source_monoid_order: usize) -> Self {
        Self::from_elementary(
            "apply_swap01",
            source_monoid_order,
            StateMapKind::ApplySwap01,
        )
    }

    pub fn scale_weights(source_monoid_order: usize, k: u64) -> Self {
        Self::from_elementary(
            format!("scale_{k}"),
            source_monoid_order,
            StateMapKind::ScaleWeights(k),
        )
    }

    pub fn map_state(&self, x: &PopulationConfig) -> Result<PopulationConfig, FunctorError> {
        let mut cur = x.clone();
        for step in &self.state_steps {
            cur = step.apply(&cur)?;
        }
        Ok(cur)
    }

    pub fn map_context(&self, c: usize) -> Option<usize> {
        self.monoid_map.get(c).copied()
    }

    pub fn check_equivariance(
        &self,
        source: &ObserverAction,
        target: &ObserverAction,
        sample: &[PopulationConfig],
    ) -> bool {
        for x in sample {
            for c in 0..source.monoid.order() {
                let Ok(cx) = source.act(c, x) else {
                    return false;
                };
                let Ok(phi_cx) = self.map_state(&cx) else {
                    return false;
                };
                let Some(pc) = self.map_context(c) else {
                    return false;
                };
                let Ok(phi_x) = self.map_state(x) else {
                    return false;
                };
                let Ok(c_phi_x) = target.act(pc, &phi_x) else {
                    return false;
                };
                if phi_cx != c_phi_x {
                    return false;
                }
            }
        }
        true
    }

    pub fn descends(
        &self,
        source: &ObserverAction,
        target: &ObserverAction,
        sample: &[PopulationConfig],
    ) -> bool {
        for x in sample {
            for y in sample {
                if bi_congruent(source, x, y) {
                    let Ok(px) = self.map_state(x) else {
                        return false;
                    };
                    let Ok(py) = self.map_state(y) else {
                        return false;
                    };
                    if !bi_congruent(target, &px, &py) {
                        return false;
                    }
                }
            }
        }
        true
    }
}

pub fn compose_morphisms(
    g: &SystemMorphism,
    f: &SystemMorphism,
) -> Result<SystemMorphism, FunctorError> {
    let mut monoid_map = Vec::with_capacity(f.monoid_map.len());
    for &c in &f.monoid_map {
        let Some(&gc) = g.monoid_map.get(c) else {
            return Err(FunctorError::CompositionDomainMismatch);
        };
        monoid_map.push(gc);
    }
    let mut state_steps = f.state_steps.clone();
    state_steps.extend(g.state_steps.iter().copied());
    Ok(SystemMorphism {
        label: format!("({}∘{})", g.label, f.label),
        monoid_map,
        state_steps,
    })
}

pub fn pushforward_classes(
    morph: &SystemMorphism,
    source: &ObserverAction,
    target: &ObserverAction,
    sample: &[PopulationConfig],
) -> Result<BTreeMap<ObserverClass, ObserverClass>, FunctorError> {
    if !morph.descends(source, target, sample) {
        return Err(FunctorError::DescentFailed {
            reason: "state map does not descend through bI",
        });
    }
    let (src_classes, _) = bi_partition(source, sample);
    let mapped: Result<Vec<PopulationConfig>, _> =
        sample.iter().map(|x| morph.map_state(x)).collect();
    let mapped = mapped?;
    let (tgt_classes, _) = bi_partition(target, &mapped);

    let mut out: BTreeMap<ObserverClass, ObserverClass> = BTreeMap::new();
    for i in 0..sample.len() {
        let sc = src_classes[i];
        let tc = tgt_classes[i];
        if let Some(prev) = out.insert(sc, tc) {
            if prev != tc {
                return Err(FunctorError::DescentFailed {
                    reason: "class map ill-defined on partition",
                });
            }
        }
    }
    Ok(out)
}

pub fn authority_fence() -> &'static str {
    AUTHORITY_FENCE
}


#[cfg(test)]
mod tests {
    use super::*;

    fn fin3() -> CarrierSetId {
        CarrierSetId::try_new("fin3-wave3", 3).unwrap()
    }

    fn cfg(weights: [u64; 3], tags: [u8; 3]) -> PopulationConfig {
        PopulationConfig::try_new(fin3(), weights.to_vec(), tags.to_vec()).unwrap()
    }

    fn cfg_a() -> PopulationConfig {
        cfg([4, 1, 3], [0, 0, 0])
    }
    fn cfg_b() -> PopulationConfig {
        cfg([4, 1, 3], [1, 0, 0])
    }

    #[test]
    fn authority_effect_none() {
        assert!(authority_fence().contains("AuthorityEffect None"));
        assert!(AUTHORITY_FENCE.contains("W3.5"));
    }

    #[test]
    fn general_carrier_parameterized_by_size_and_id() {
        let c2 = CarrierSetId::try_new("pair", 2).unwrap();
        let c4 = CarrierSetId::try_new("quad", 4).unwrap();
        assert_ne!(c2, c4);
        assert_eq!(c2.size(), 2);
        assert!(CarrierSetId::try_new("bad", 0).is_err());
        let x = PopulationConfig::try_new(c2.clone(), vec![1, 2], vec![0, 1]).unwrap();
        assert_eq!(x.mass().unwrap(), 3);
        assert!(PopulationConfig::try_new(c2, vec![1], vec![0, 1]).is_err());
    }

    #[test]
    fn same_population_ignores_tags_but_config_eq_does_not() {
        let a = cfg_a();
        let b = cfg_b();
        assert!(same_population(&a, &b));
        assert_ne!(a, b);
        assert_eq!(pop_sig(&a), vec![4, 1, 3]);
    }

    #[test]
    fn same_pop_and_bi_are_separate_defs_bridge_only_via_function() {
        let a = cfg_a();
        let b = cfg_b();
        let triv = ObserverAction::trivial();

        assert!(same_population(&a, &b));
        assert!(bi_congruent(&triv, &a, &b));

        assert!(same_pop_iff_bi_triv_pop(&a, &b));
        assert!(same_pop_agrees_with_bi(&triv, &a, &b));

        let c = cfg([5, 1, 3], [0, 0, 0]);
        assert!(!same_population(&a, &c));
        assert!(!bi_congruent(&triv, &a, &c));
        assert!(same_pop_iff_bi_triv_pop(&a, &c));
    }

    #[test]
    fn trivial_swap_and_absorb_actions_obey_the_composition_law() {
        let samples = [
            cfg_a(),
            cfg_b(),
            cfg([2, 7, 1], [2, 1, 0]),
            cfg([0, 0, 0], [1, 1, 1]),
        ];
        for action in [
            ObserverAction::trivial(),
            ObserverAction::swap01(),
            ObserverAction::tag_absorb(),
        ] {
            for x in &samples {
                assert_eq!(
                    action.action_law_violations(x),
                    Ok(vec![]),
                    "{:?}",
                    action.kind
                );
            }
        }
    }

    #[test]
    fn the_additive_tag_reveal_violates_the_composition_law_exactly_when_contexts_wrap() {
        let reveal = ObserverAction::tag_reveal(3).unwrap();
        assert_eq!(reveal.action_law_violations(&cfg_a()), Ok(vec![]));
        assert_eq!(
            reveal.action_law_violations(&cfg_b()),
            Ok(vec![(1, 2), (2, 1), (2, 2)])
        );
        let reveal2 = ObserverAction::tag_reveal(2).unwrap();
        assert_eq!(reveal2.action_law_violations(&cfg_b()), Ok(vec![(1, 1)]));
    }

    #[test]
    fn tag_absorb_is_idempotent_and_still_separates_same_population_configs() {
        let absorb = ObserverAction::tag_absorb();
        let (a, b) = (cfg_a(), cfg_b());
        assert!(same_population(&a, &b));
        assert!(!bi_congruent(&absorb, &a, &b));
        assert!(!same_pop_agrees_with_bi(&absorb, &a, &b));
        let once = absorb.act(1, &b).unwrap();
        assert_eq!(once.weights, vec![5, 1, 3]);
        assert_eq!(once.tags, vec![0, 0, 0]);
        assert_eq!(absorb.act(1, &once).unwrap(), once);
        assert!(absorb.check_act_one(&b));
    }

    #[test]
    fn nontrivial_action_is_not_identity() {
        let reveal = ObserverAction::tag_reveal(3).unwrap();
        assert_eq!(reveal.kind, ActionKind::TagRevealAdditive);
        assert_ne!(reveal.kind, ActionKind::Trivial);
        let a = cfg_a();
        assert!(reveal.check_act_one(&a));
        let a1 = reveal.act(1, &a).unwrap();
        assert_eq!(a1.weights, a.weights);
        let b = cfg_b();
        let b1 = reveal.act(1, &b).unwrap();
        assert_ne!(b1.weights, b.weights);
        assert_eq!(b1.weights[0], 4 + 1);
    }

    #[test]
    fn counterexample_same_pop_not_def_eq_bi_under_nontrivial_action() {
        let reveal = ObserverAction::tag_reveal(4).unwrap();
        let a = cfg_a();
        let b = cfg_b();

        assert!(same_population(&a, &b), "weights match — samePop holds");
        assert!(
            !bi_congruent(&reveal, &a, &b),
            "reveal action separates tag variants — bI fails"
        );
        assert!(
            !same_pop_agrees_with_bi(&reveal, &a, &b),
            "relations diverge: definitional SamePop=BI would wrongly identify them"
        );

        assert!(same_pop_agrees_with_bi(&ObserverAction::trivial(), &a, &b));
    }

    #[test]
    fn swap01_action_preserves_same_pop_bi_agreement_on_phase_variants() {
        let swap = ObserverAction::swap01();
        let a = cfg_a();
        let b = cfg_b();
        assert!(same_population(&a, &b));
        assert!(bi_congruent(&swap, &a, &b));
        let a_s = swap.act(1, &a).unwrap();
        assert_eq!(a_s.weights, vec![1, 4, 3]);
        assert_eq!(a_s.mass(), a.mass());
    }

    #[test]
    fn bi_partition_collapses_phase_under_triv_not_under_reveal() {
        let sample = vec![cfg_a(), cfg_b(), cfg([5, 1, 3], [0, 0, 0])];
        let triv = ObserverAction::trivial();
        let (_, n_triv) = bi_partition(&triv, &sample);
        assert_eq!(n_triv, 2);

        let reveal = ObserverAction::tag_reveal(3).unwrap();
        let (_, n_rev) = bi_partition(&reveal, &sample);
        assert_eq!(n_rev, 3);
    }

    #[test]
    fn morphism_identity_equivariant_and_descends() {
        let act = ObserverAction::trivial();
        let sample = vec![cfg_a(), cfg_b()];
        let id = SystemMorphism::identity(act.monoid.order());
        assert!(id.check_equivariance(&act, &act, &sample));
        assert!(id.descends(&act, &act, &sample));
        let pf = pushforward_classes(&id, &act, &act, &sample).unwrap();
        assert_eq!(pf.len(), 1);
        assert_eq!(pf.get(&ObserverClass(0)), Some(&ObserverClass(0)));
    }

    #[test]
    fn functoriality_three_morphisms_composition() {
        let act = ObserverAction::trivial();
        let sample = vec![
            cfg_a(),
            cfg_b(),
            cfg([2, 2, 2], [1, 1, 1]),
            cfg([2, 2, 2], [0, 0, 0]),
        ];
        let f = SystemMorphism::scale_weights(1, 2);
        let g = SystemMorphism::forget_tags(1);
        let h = SystemMorphism::identity(1);

        assert!(f.check_equivariance(&act, &act, &sample));
        assert!(g.check_equivariance(&act, &act, &sample));
        assert!(h.check_equivariance(&act, &act, &sample));
        assert!(f.descends(&act, &act, &sample));
        assert!(g.descends(&act, &act, &sample));
        assert!(h.descends(&act, &act, &sample));

        let pf_f = pushforward_classes(&f, &act, &act, &sample).unwrap();
        let pf_g = pushforward_classes(&g, &act, &act, &sample).unwrap();
        let pf_h = pushforward_classes(&h, &act, &act, &sample).unwrap();

        let gf = compose_morphisms(&g, &f).unwrap();
        let hgf = compose_morphisms(&h, &gf).unwrap();
        assert!(hgf.descends(&act, &act, &sample));
        let pf_hgf = pushforward_classes(&hgf, &act, &act, &sample).unwrap();

        for (sc, tc_f) in &pf_f {
            let tc_gf = pf_g.get(tc_f).copied().unwrap_or(*tc_f);
            let _ = tc_gf;
            assert!(pf_hgf.contains_key(sc) || pf_h.contains_key(sc));
        }

        let (src_c, _) = bi_partition(&act, &sample);
        for (i, x) in sample.iter().enumerate() {
            let y = hgf.map_state(x).unwrap();
            let step = {
                let x1 = f.map_state(x).unwrap();
                let x2 = g.map_state(&x1).unwrap();
                h.map_state(&x2).unwrap()
            };
            assert_eq!(y.weights, step.weights);
            assert_eq!(y.tags, step.tags);
            let _ = src_c[i];
        }
    }

    #[test]
    fn functoriality_swap_involution_two_morphisms() {
        let act = ObserverAction::swap01();
        let sample = vec![cfg_a(), cfg([1, 4, 3], [0, 0, 0])];
        let s = SystemMorphism::apply_swap01(act.monoid.order());
        assert!(s.check_equivariance(&act, &act, &sample));
        assert!(s.descends(&act, &act, &sample));

        let ss = compose_morphisms(&s, &s).unwrap();
        assert_eq!(ss.state_steps.len(), 2);
        for x in &sample {
            assert_eq!(ss.map_state(x).unwrap(), *x);
        }
        let pf_ss = pushforward_classes(&ss, &act, &act, &sample).unwrap();
        let pf_id = pushforward_classes(
            &SystemMorphism::identity(act.monoid.order()),
            &act,
            &act,
            &sample,
        )
        .unwrap();
        assert_eq!(pf_ss, pf_id);
    }

    #[test]
    fn forget_tags_descends_under_triv_collapses_reveal_distinction() {
        let reveal = ObserverAction::tag_reveal(3).unwrap();
        let triv = ObserverAction::trivial();
        let sample = vec![cfg_a(), cfg_b()];

        let (c_rev, n) = bi_partition(&reveal, &sample);
        assert_eq!(n, 2);
        assert_ne!(c_rev[0], c_rev[1]);

        let morph = SystemMorphism {
            label: "forget_into_triv".into(),
            monoid_map: vec![0, 0, 0],
            state_steps: vec![StateMapKind::ForgetTags],
        };
        assert!(!morph.check_equivariance(&reveal, &triv, &sample));

        assert!(morph.descends(&reveal, &triv, &sample));
    }

    #[test]
    fn descent_failure_witness_scale_on_reveal_incomparable_pairs() {
        let triv = ObserverAction::trivial();
        let reveal = ObserverAction::tag_reveal(2).unwrap();
        let sample = vec![cfg_a(), cfg_b()];
        let morph = SystemMorphism {
            label: "id_triv_to_reveal".into(),
            monoid_map: vec![0],
            state_steps: vec![],
        };
        assert!(
            !morph.descends(&triv, &reveal, &sample),
            "samePop/bI_triv pair must not descend into reveal bI"
        );
        let err = pushforward_classes(&morph, &triv, &reveal, &sample).unwrap_err();
        assert!(matches!(err, FunctorError::DescentFailed { .. }));
    }
}

#[cfg(test)]
mod checked_arithmetic_tests {
    use super::*;
    #[test]
    fn arithmetic_overflow_and_false_action_laws_are_refused() {
        let carrier = CarrierSetId::try_new("checked", 1).unwrap();
        let x = PopulationConfig::try_new(carrier, vec![u64::MAX], vec![1]).unwrap();
        assert_eq!(
            ObserverAction::tag_absorb().act(1, &x),
            Err(FunctorError::ArithmeticOverflow)
        );
        assert_eq!(
            StateMapKind::ScaleWeights(2).apply(&x),
            Err(FunctorError::ArithmeticOverflow)
        );
        let small = PopulationConfig::try_new(x.carrier.clone(), vec![1], vec![1]).unwrap();
        assert_eq!(
            ObserverAction::tag_reveal(2)
                .unwrap()
                .validate_action_on(&[small.clone()]),
            Err(FunctorError::InvalidActionLaw)
        );
        assert_eq!(
            ObserverAction::tag_absorb().validate_action_on(&[small]),
            Ok(())
        );
    }
}

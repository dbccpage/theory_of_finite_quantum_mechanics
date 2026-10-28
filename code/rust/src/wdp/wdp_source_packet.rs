
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::rational_bareiss::{
    RationalBudget, RationalError, RationalLimits,
};
use num_rational::BigRational;
use engine_kernel::{exact_wire, exact_wire_vec};
use engine_number_theory::cyclotomic::GaussianRat;
use engine_quantum_physics::exact_channel::{ExactChannelError, ExactKrausChannel};
use engine_solvers::data_hodge_packet::{
    self as hodge, HodgeAvailabilityModelV1, HodgeCompositionModelV1, HodgePacketError,
    HodgePacketHeaderV1, HodgePositivityModelV1, HodgeQuestionV1, HodgeQuotientModelV1,
    HodgeRequestV1, HodgeResourceLimitsV1, HodgeResultV1, HodgeScalarModelV1, RationalMatrixV1,
};
use engine_types::AuthorityEffect;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

pub const WDP_SOURCE_PACKET_SCHEMA_V1: &str = "omega.wdp.source-packet.v1";
pub const WDP_SOURCE_RESULT_SCHEMA_V1: &str = "omega.wdp.source-packet-result.v1";
pub const WDP_SOURCE_REPLAY_SCHEMA_V1: &str = "omega.wdp.source-packet-replay.v1";
pub const WDP_PACKET_REQUEST_DOMAIN_V1: &str = "omega.wdp.source-packet-request.v1";
pub const WDP_PACKET_CARRIER_DOMAIN_V1: &str = "omega.wdp.source-packet-carrier.v1";
pub const WDP_PACKET_RESULT_DOMAIN_V1: &str = "omega.wdp.source-packet-result-content.v1";
pub const MAX_SOURCE_BYTES: usize = 8_192;
pub const MAX_PACKET_ELEMENTS: usize = 4_096;
pub const MAX_PACKET_SCALAR_OPS: usize = 10_000_000;
pub const MAX_PACKET_BITS: u64 = 1_024;
pub const MAX_CHANNEL_DIMENSION: usize = 16;
pub const MAX_KRAUS_TERMS: usize = 32;

macro_rules! premise_enum {
    ($name:ident { $($variant:ident),+ $(,)? }) => {
        #[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
        #[serde(rename_all = "snake_case")]
        pub enum $name { $($variant),+ }
    };
}

premise_enum!(SourceDigestProfileV1 { Sha256RawBytesV1 });
premise_enum!(WdpPacketQuestionV1 {
    ExactEuclideanHodgeDecomposition,
    ExactWeightedKrausGramStateTransport,
    Other
});
premise_enum!(WdpPacketScopeV1 {
    FiniteDeclaredInputs,
    GeneralTheory
});
premise_enum!(WdpPacketScalarModelV1 {
    ExactRational,
    ExactGaussianRational,
    FloatingPoint
});
premise_enum!(WdpPacketQuotientModelV1 {
    PotentialModuloKernel,
    MatrixEntryEquality,
    Undeclared
});
premise_enum!(WdpPacketPositivityModelV1 {
    NotApplicable,
    NonnegativeKrausWeightsAndGramState,
    Claimed
});
premise_enum!(WdpPacketCompositionModelV1 {
    NotApplicable,
    SingleDeclaredMap,
    AllComposedWords
});
premise_enum!(WdpPacketAvailabilityModelV1 {
    DeclaredFiniteCarrier,
    Unknown
});

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SourceBindingV1 {
    pub source_id: String,
    pub digest_profile: SourceDigestProfileV1,
    pub sha256: String,
    pub bytes: Vec<u8>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct VerifiedSourceBindingV1 {
    pub source_id: String,
    pub digest_profile: SourceDigestProfileV1,
    pub sha256: String,
    pub byte_count: usize,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WdpPacketResourceLimitsV1 {
    pub max_source_bytes: usize,
    pub max_scalar_ops: usize,
    pub max_elements: usize,
    pub max_bits: u64,
}

impl WdpPacketResourceLimitsV1 {
    fn rational_limits(self) -> Result<RationalLimits, WdpPacketRefusalV1> {
        if self.max_source_bytes == 0
            || self.max_source_bytes > MAX_SOURCE_BYTES
            || self.max_scalar_ops == 0
            || self.max_scalar_ops > MAX_PACKET_SCALAR_OPS
            || self.max_elements == 0
            || self.max_elements > MAX_PACKET_ELEMENTS
            || self.max_bits == 0
            || self.max_bits > MAX_PACKET_BITS
        {
            return Err(refuse(
                WdpPacketRefusalCodeV1::ResourceLimits,
                "resource limits must be positive and within the finite boundary ceilings",
            ));
        }
        Ok(RationalLimits {
            max_scalar_ops: self.max_scalar_ops,
            max_elements: self.max_elements,
            max_bits: self.max_bits,
        })
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WdpPacketHeaderV1 {
    pub schema_version: String,
    pub question: WdpPacketQuestionV1,
    pub scope: WdpPacketScopeV1,
    pub scalar_model: WdpPacketScalarModelV1,
    pub quotient_model: WdpPacketQuotientModelV1,
    pub positivity_model: WdpPacketPositivityModelV1,
    pub composition_model: WdpPacketCompositionModelV1,
    pub availability_model: WdpPacketAvailabilityModelV1,
    pub limits: WdpPacketResourceLimitsV1,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GaussianRationalV1 {
    #[serde(with = "exact_wire")]
    pub re: BigRational,
    #[serde(with = "exact_wire")]
    pub im: BigRational,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GaussianMatrixV1 {
    pub rows: usize,
    pub cols: usize,
    pub entries: Vec<GaussianRationalV1>,
}

impl GaussianMatrixV1 {
    fn decode(
        &self,
        fuel: &mut RationalBudget,
    ) -> Result<BasicMatrix<GaussianRat>, WdpPacketRefusalV1> {
        fuel.elements(self.rows, 1).map_err(arithmetic_refusal)?;
        fuel.elements(self.cols, 1).map_err(arithmetic_refusal)?;
        let count = fuel
            .elements(self.rows, self.cols)
            .map_err(arithmetic_refusal)?;
        if count != self.entries.len() {
            return Err(refuse(
                WdpPacketRefusalCodeV1::Shape,
                "Gaussian matrix entry count differs from its dimensions",
            ));
        }
        let mut entries = Vec::new();
        entries
            .try_reserve_exact(count)
            .map_err(|_| arithmetic_refusal(RationalError::Allocation))?;
        for value in &self.entries {
            fuel.rational(&value.re).map_err(arithmetic_refusal)?;
            fuel.rational(&value.im).map_err(arithmetic_refusal)?;
            entries.push(GaussianRat {
                re: value.re.clone(),
                im: value.im.clone(),
            });
        }
        BasicMatrix::from_row_major(self.rows, self.cols, entries)
            .map_err(|error| refuse(WdpPacketRefusalCodeV1::Shape, error.to_string()))
    }

    fn encode(matrix: &BasicMatrix<GaussianRat>) -> Self {
        Self {
            rows: matrix.rows(),
            cols: matrix.cols(),
            entries: matrix
                .as_slice()
                .iter()
                .map(|value| GaussianRationalV1 {
                    re: value.re.clone(),
                    im: value.im.clone(),
                })
                .collect(),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WeightedKrausTermV1 {
    #[serde(with = "exact_wire")]
    pub weight: BigRational,
    pub operator: GaussianMatrixV1,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum WdpPacketOperationV1 {
    Hodge {
        d0: RationalMatrixV1,
        d1: RationalMatrixV1,
        #[serde(with = "exact_wire_vec")]
        flow: Vec<BigRational>,
    },
    WeightedKrausGramStateTransport {
        dim_in: usize,
        dim_out: usize,
        terms: Vec<WeightedKrausTermV1>,
        state_factor: GaussianMatrixV1,
    },
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WdpSourcePacketRequestV1 {
    pub header: WdpPacketHeaderV1,
    pub source: SourceBindingV1,
    pub operation: WdpPacketOperationV1,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum WdpPacketOutputV1 {
    Hodge { result: HodgeResultV1 },
    WeightedKrausGramStateTransport { image: GaussianMatrixV1 },
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WdpSourcePacketResultV1 {
    pub schema_version: String,
    pub header: WdpPacketHeaderV1,
    pub source: VerifiedSourceBindingV1,
    pub input_digest: String,
    pub carrier_digest: String,
    pub output: WdpPacketOutputV1,
    pub authority_effect: AuthorityEffect,
    pub result_digest: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WdpSourcePacketReplayV1 {
    pub schema_version: String,
    pub input_digest: String,
    pub carrier_digest: String,
    pub result_digest: String,
    pub replay_scalar_ops: usize,
    pub authority_effect: AuthorityEffect,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum WdpPacketRefusalCodeV1 {
    Wire,
    Schema,
    SourceBytes,
    SourceDigest,
    ResourceLimits,
    ResourceBudget,
    Question,
    Scope,
    ScalarModel,
    QuotientModel,
    PositivityModel,
    CompositionModel,
    AvailabilityModel,
    Shape,
    RequestBinding,
    CarrierBinding,
    ResultBinding,
    Authority,
    HodgePremise,
    HodgeCertificate,
    ChannelPremise,
    ChannelResult,
    ResultKind,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WdpPacketRefusalV1 {
    pub code: WdpPacketRefusalCodeV1,
    pub detail: String,
    pub authority_effect: AuthorityEffect,
}

impl WdpPacketRefusalV1 {
    pub fn wire(&self) -> String {
        let code = match self.code {
            WdpPacketRefusalCodeV1::Wire => "WIRE",
            WdpPacketRefusalCodeV1::Schema => "SCHEMA",
            WdpPacketRefusalCodeV1::SourceBytes => "SOURCE_BYTES",
            WdpPacketRefusalCodeV1::SourceDigest => "SOURCE_DIGEST",
            WdpPacketRefusalCodeV1::ResourceLimits => "RESOURCE_LIMITS",
            WdpPacketRefusalCodeV1::ResourceBudget => "RESOURCE_BUDGET",
            WdpPacketRefusalCodeV1::Question => "QUESTION",
            WdpPacketRefusalCodeV1::Scope => "SCOPE",
            WdpPacketRefusalCodeV1::ScalarModel => "SCALAR_MODEL",
            WdpPacketRefusalCodeV1::QuotientModel => "QUOTIENT_MODEL",
            WdpPacketRefusalCodeV1::PositivityModel => "POSITIVITY_MODEL",
            WdpPacketRefusalCodeV1::CompositionModel => "COMPOSITION_MODEL",
            WdpPacketRefusalCodeV1::AvailabilityModel => "AVAILABILITY_MODEL",
            WdpPacketRefusalCodeV1::Shape => "SHAPE",
            WdpPacketRefusalCodeV1::RequestBinding => "REQUEST_BINDING",
            WdpPacketRefusalCodeV1::CarrierBinding => "CARRIER_BINDING",
            WdpPacketRefusalCodeV1::ResultBinding => "RESULT_BINDING",
            WdpPacketRefusalCodeV1::Authority => "AUTHORITY",
            WdpPacketRefusalCodeV1::HodgePremise => "HODGE_PREMISE",
            WdpPacketRefusalCodeV1::HodgeCertificate => "HODGE_CERTIFICATE",
            WdpPacketRefusalCodeV1::ChannelPremise => "CHANNEL_PREMISE",
            WdpPacketRefusalCodeV1::ChannelResult => "CHANNEL_RESULT",
            WdpPacketRefusalCodeV1::ResultKind => "RESULT_KIND",
        };
        format!("WDP_PACKET_{code}: {}", self.detail)
    }
}

fn refuse(code: WdpPacketRefusalCodeV1, detail: impl Into<String>) -> WdpPacketRefusalV1 {
    WdpPacketRefusalV1 {
        code,
        detail: detail.into(),
        authority_effect: AuthorityEffect::None,
    }
}

fn arithmetic_refusal(error: RationalError) -> WdpPacketRefusalV1 {
    refuse(WdpPacketRefusalCodeV1::ResourceBudget, error.to_string())
}

fn hodge_refusal(error: HodgePacketError) -> WdpPacketRefusalV1 {
    match error {
        HodgePacketError::Arithmetic(error) => arithmetic_refusal(error),
        HodgePacketError::Hodge(engine_solvers::cert_hodge_decomp::HodgeError::Arithmetic(
            error,
        )) => arithmetic_refusal(error),
        HodgePacketError::Hodge(error) => {
            refuse(WdpPacketRefusalCodeV1::HodgeCertificate, error.to_string())
        }
        error => refuse(WdpPacketRefusalCodeV1::HodgePremise, error.to_string()),
    }
}

fn channel_refusal(error: ExactChannelError) -> WdpPacketRefusalV1 {
    match error {
        ExactChannelError::RationalBudget(error) => arithmetic_refusal(error),
        error => refuse(WdpPacketRefusalCodeV1::ChannelPremise, error.to_string()),
    }
}

pub fn raw_source_sha256(bytes: &[u8]) -> String {
    hex::encode(Sha256::digest(bytes))
}

fn verify_source(
    source: &SourceBindingV1,
    max_bytes: usize,
) -> Result<VerifiedSourceBindingV1, WdpPacketRefusalV1> {
    if source.source_id.is_empty()
        || source.source_id.len() > 256
        || source.source_id.chars().any(char::is_control)
        || source.bytes.is_empty()
        || source.bytes.len() > max_bytes
    {
        return Err(refuse(
            WdpPacketRefusalCodeV1::SourceBytes,
            "source needs an explicit id and 1..max_source_bytes supplied raw bytes",
        ));
    }
    if source.sha256.len() != 64
        || !source
            .sha256
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
        || source.sha256 != raw_source_sha256(&source.bytes)
    {
        return Err(refuse(
            WdpPacketRefusalCodeV1::SourceDigest,
            "source SHA-256 does not match the supplied raw bytes and lowercase hex profile",
        ));
    }
    Ok(VerifiedSourceBindingV1 {
        source_id: source.source_id.clone(),
        digest_profile: source.digest_profile,
        sha256: source.sha256.clone(),
        byte_count: source.bytes.len(),
    })
}

pub fn packet_digest<T: Serialize>(domain: &str, value: &T) -> Result<String, WdpPacketRefusalV1> {
    let value = serde_json::to_value(value)
        .map_err(|error| refuse(WdpPacketRefusalCodeV1::Wire, error.to_string()))?;
    let bytes = serde_json::to_vec(&value)
        .map_err(|error| refuse(WdpPacketRefusalCodeV1::Wire, error.to_string()))?;
    let mut hasher = Sha256::new();
    hasher.update((domain.len() as u32).to_be_bytes());
    hasher.update(domain.as_bytes());
    hasher.update((bytes.len() as u64).to_be_bytes());
    hasher.update(bytes);
    Ok(hex::encode(hasher.finalize()))
}

fn result_digest(result: &WdpSourcePacketResultV1) -> Result<String, WdpPacketRefusalV1> {
    let mut value = serde_json::to_value(result)
        .map_err(|error| refuse(WdpPacketRefusalCodeV1::Wire, error.to_string()))?;
    let fields = value.as_object_mut().ok_or_else(|| {
        refuse(
            WdpPacketRefusalCodeV1::Wire,
            "result commitment needs an object",
        )
    })?;
    fields.remove("result_digest");
    packet_digest(WDP_PACKET_RESULT_DOMAIN_V1, &value)
}

fn validate_header(
    request: &WdpSourcePacketRequestV1,
) -> Result<RationalLimits, WdpPacketRefusalV1> {
    let header = &request.header;
    if header.schema_version != WDP_SOURCE_PACKET_SCHEMA_V1 {
        return Err(refuse(
            WdpPacketRefusalCodeV1::Schema,
            "unsupported source-packet schema",
        ));
    }
    if header.scope != WdpPacketScopeV1::FiniteDeclaredInputs {
        return Err(refuse(
            WdpPacketRefusalCodeV1::Scope,
            "only the supplied finite declared inputs are admitted",
        ));
    }
    if header.availability_model != WdpPacketAvailabilityModelV1::DeclaredFiniteCarrier {
        return Err(refuse(
            WdpPacketRefusalCodeV1::AvailabilityModel,
            "finite operational availability must be declared",
        ));
    }
    let (question, scalar, quotient, positivity, composition) = match &request.operation {
        WdpPacketOperationV1::Hodge { .. } => (
            WdpPacketQuestionV1::ExactEuclideanHodgeDecomposition,
            WdpPacketScalarModelV1::ExactRational,
            WdpPacketQuotientModelV1::PotentialModuloKernel,
            WdpPacketPositivityModelV1::NotApplicable,
            WdpPacketCompositionModelV1::NotApplicable,
        ),
        WdpPacketOperationV1::WeightedKrausGramStateTransport { .. } => (
            WdpPacketQuestionV1::ExactWeightedKrausGramStateTransport,
            WdpPacketScalarModelV1::ExactGaussianRational,
            WdpPacketQuotientModelV1::MatrixEntryEquality,
            WdpPacketPositivityModelV1::NonnegativeKrausWeightsAndGramState,
            WdpPacketCompositionModelV1::SingleDeclaredMap,
        ),
    };
    for (valid, code, name) in [
        (
            header.question == question,
            WdpPacketRefusalCodeV1::Question,
            "protected question",
        ),
        (
            header.scalar_model == scalar,
            WdpPacketRefusalCodeV1::ScalarModel,
            "scalar field",
        ),
        (
            header.quotient_model == quotient,
            WdpPacketRefusalCodeV1::QuotientModel,
            "quotient model",
        ),
        (
            header.positivity_model == positivity,
            WdpPacketRefusalCodeV1::PositivityModel,
            "positivity premise",
        ),
        (
            header.composition_model == composition,
            WdpPacketRefusalCodeV1::CompositionModel,
            "composition premise",
        ),
    ] {
        if !valid {
            return Err(refuse(
                code,
                format!("{name} is incompatible with the requested finite operation"),
            ));
        }
    }
    header.limits.rational_limits()
}

fn preflight_rational_matrix(
    matrix: &RationalMatrixV1,
    fuel: &mut RationalBudget,
) -> Result<usize, WdpPacketRefusalV1> {
    fuel.elements(matrix.rows, 1).map_err(arithmetic_refusal)?;
    fuel.elements(matrix.cols, 1).map_err(arithmetic_refusal)?;
    let count = fuel
        .elements(matrix.rows, matrix.cols)
        .map_err(arithmetic_refusal)?;
    if matrix.entries.len() != count {
        return Err(refuse(
            WdpPacketRefusalCodeV1::Shape,
            "rational matrix entry count differs from its dimensions",
        ));
    }
    for scalar in &matrix.entries {
        fuel.rational(scalar).map_err(arithmetic_refusal)?;
    }
    Ok(count)
}

fn preflight_carrier(
    request: &WdpSourcePacketRequestV1,
    fuel: &mut RationalBudget,
) -> Result<(), WdpPacketRefusalV1> {
    let count = match &request.operation {
        WdpPacketOperationV1::Hodge { d0, d1, flow } => {
            let c0 = preflight_rational_matrix(d0, fuel)?;
            let c1 = preflight_rational_matrix(d1, fuel)?;
            fuel.elements(flow.len(), 1).map_err(arithmetic_refusal)?;
            for scalar in flow {
                fuel.rational(scalar).map_err(arithmetic_refusal)?;
            }
            c0.checked_add(c1)
                .and_then(|count| count.checked_add(flow.len()))
        }
        WdpPacketOperationV1::WeightedKrausGramStateTransport {
            dim_in,
            dim_out,
            terms,
            state_factor,
        } => {
            if *dim_in == 0
                || *dim_out == 0
                || *dim_in > MAX_CHANNEL_DIMENSION
                || *dim_out > MAX_CHANNEL_DIMENSION
                || terms.is_empty()
                || terms.len() > MAX_KRAUS_TERMS
                || state_factor.cols > MAX_CHANNEL_DIMENSION
            {
                return Err(refuse(
                    WdpPacketRefusalCodeV1::Shape,
                    "channel dimensions/count exceed the finite operational boundary",
                ));
            }
            let mut count = state_factor.decode(fuel)?.as_slice().len();
            for term in terms {
                fuel.rational(&term.weight).map_err(arithmetic_refusal)?;
                count = count
                    .checked_add(term.operator.decode(fuel)?.as_slice().len())
                    .ok_or_else(|| arithmetic_refusal(RationalError::ElementLimit))?;
            }
            Some(count)
        }
    }
    .ok_or_else(|| arithmetic_refusal(RationalError::ElementLimit))?;
    fuel.elements(count, 1).map_err(arithmetic_refusal)?;
    Ok(())
}

fn preflight_output(
    output: &WdpPacketOutputV1,
    fuel: &mut RationalBudget,
) -> Result<(), WdpPacketRefusalV1> {
    match output {
        WdpPacketOutputV1::Hodge { result } => {
            let certificate = &result.certificate;
            let mut total = 0usize;
            for values in [
                &certificate.alpha,
                &certificate.beta,
                &certificate.exact,
                &certificate.coexact,
                &certificate.harmonic,
            ] {
                total = total
                    .checked_add(values.len())
                    .ok_or_else(|| arithmetic_refusal(RationalError::ElementLimit))?;
                fuel.elements(values.len(), 1).map_err(arithmetic_refusal)?;
                for value in values {
                    fuel.rational(value).map_err(arithmetic_refusal)?;
                }
            }
            fuel.elements(total, 1).map_err(arithmetic_refusal)?;
        }
        WdpPacketOutputV1::WeightedKrausGramStateTransport { image } => {
            image.decode(fuel)?;
        }
    }
    Ok(())
}

fn hodge_request(
    request: &WdpSourcePacketRequestV1,
    d0: &RationalMatrixV1,
    d1: &RationalMatrixV1,
    flow: &[BigRational],
) -> HodgeRequestV1 {
    let limits = request.header.limits;
    HodgeRequestV1 {
        header: HodgePacketHeaderV1 {
            schema_version: hodge::HODGE_PACKET_SCHEMA_V1.to_owned(),
            source_digest: request.source.sha256.clone(),
            scalar_model: HodgeScalarModelV1::ExactRational,
            quotient_model: HodgeQuotientModelV1::PotentialModuloKernel,
            positivity_model: HodgePositivityModelV1::NotApplicable,
            composition_model: HodgeCompositionModelV1::NotApplicable,
            availability_model: HodgeAvailabilityModelV1::DeclaredFiniteCarrier,
            question: HodgeQuestionV1::ExactEuclideanHodgeDecomposition,
            limits: HodgeResourceLimitsV1 {
                max_scalar_ops: limits.max_scalar_ops,
                max_elements: limits.max_elements,
                max_bits: limits.max_bits,
            },
        },
        d0: d0.clone(),
        d1: d1.clone(),
        flow: flow.to_vec(),
    }
}

fn channel_image(
    dim_in: usize,
    dim_out: usize,
    terms: &[WeightedKrausTermV1],
    state_factor: &GaussianMatrixV1,
    fuel: &mut RationalBudget,
) -> Result<GaussianMatrixV1, WdpPacketRefusalV1> {
    if dim_in == 0
        || dim_out == 0
        || dim_in > MAX_CHANNEL_DIMENSION
        || dim_out > MAX_CHANNEL_DIMENSION
        || terms.is_empty()
        || terms.len() > MAX_KRAUS_TERMS
        || state_factor.cols > MAX_CHANNEL_DIMENSION
    {
        return Err(refuse(
            WdpPacketRefusalCodeV1::Shape,
            "channel dimensions must be 1..16 with 1..32 Kraus terms and Gram width at most 16",
        ));
    }
    let mut decoded = Vec::new();
    decoded
        .try_reserve_exact(terms.len())
        .map_err(|_| arithmetic_refusal(RationalError::Allocation))?;
    for term in terms {
        fuel.rational(&term.weight).map_err(arithmetic_refusal)?;
        decoded.push((term.weight.clone(), term.operator.decode(fuel)?));
    }
    let channel = ExactKrausChannel::try_weighted_with_budget(
        dim_in,
        dim_out,
        decoded,
        "source-packet finite declared channel",
        fuel,
    )
    .map_err(channel_refusal)?;
    let factor = state_factor.decode(fuel)?;
    let image = channel
        .transport_gram_state_with_budget(&factor, fuel)
        .map_err(channel_refusal)?;
    Ok(GaussianMatrixV1::encode(&image))
}

pub fn evaluate_source_packet(
    request: &WdpSourcePacketRequestV1,
) -> Result<WdpSourcePacketResultV1, WdpPacketRefusalV1> {
    let mut fuel = RationalBudget::new(validate_header(request)?);
    let source = verify_source(&request.source, request.header.limits.max_source_bytes)?;
    preflight_carrier(request, &mut fuel)?;
    let input_digest = packet_digest(WDP_PACKET_REQUEST_DOMAIN_V1, request)?;
    let carrier_digest = packet_digest(WDP_PACKET_CARRIER_DOMAIN_V1, &request.operation)?;
    let output = match &request.operation {
        WdpPacketOperationV1::Hodge { d0, d1, flow } => {
            let request = hodge_request(request, d0, d1, flow);
            let result = hodge::solve_hodge_packet_with_budget(request.clone(), &mut fuel)
                .map_err(hodge_refusal)?;
            hodge::replay_hodge_packet_with_budget(request, &result, &mut fuel)
                .map_err(hodge_refusal)?;
            WdpPacketOutputV1::Hodge { result }
        }
        WdpPacketOperationV1::WeightedKrausGramStateTransport {
            dim_in,
            dim_out,
            terms,
            state_factor,
        } => {
            let image = channel_image(*dim_in, *dim_out, terms, state_factor, &mut fuel)?;
            let replay = channel_image(*dim_in, *dim_out, terms, state_factor, &mut fuel)?;
            if image != replay {
                return Err(refuse(
                    WdpPacketRefusalCodeV1::ChannelResult,
                    "fresh channel replay differs",
                ));
            }
            WdpPacketOutputV1::WeightedKrausGramStateTransport { image }
        }
    };
    preflight_output(&output, &mut fuel)?;
    let mut result = WdpSourcePacketResultV1 {
        schema_version: WDP_SOURCE_RESULT_SCHEMA_V1.to_owned(),
        header: request.header.clone(),
        source,
        input_digest,
        carrier_digest,
        output,
        authority_effect: AuthorityEffect::None,
        result_digest: String::new(),
    };
    result.result_digest = result_digest(&result)?;
    Ok(result)
}

pub fn replay_source_packet(
    request: &WdpSourcePacketRequestV1,
    result: &WdpSourcePacketResultV1,
) -> Result<WdpSourcePacketReplayV1, WdpPacketRefusalV1> {
    let mut fuel = RationalBudget::new(validate_header(request)?);
    let source = verify_source(&request.source, request.header.limits.max_source_bytes)?;
    preflight_carrier(request, &mut fuel)?;
    if result.schema_version != WDP_SOURCE_RESULT_SCHEMA_V1 {
        return Err(refuse(
            WdpPacketRefusalCodeV1::Schema,
            "unsupported result schema",
        ));
    }
    if !result.authority_effect.is_none() {
        return Err(refuse(
            WdpPacketRefusalCodeV1::Authority,
            "finite packet results must carry AuthorityEffect::None",
        ));
    }
    let input_digest = packet_digest(WDP_PACKET_REQUEST_DOMAIN_V1, request)?;
    let carrier_digest = packet_digest(WDP_PACKET_CARRIER_DOMAIN_V1, &request.operation)?;
    if result.header != request.header
        || result.source != source
        || result.input_digest != input_digest
    {
        return Err(refuse(WdpPacketRefusalCodeV1::RequestBinding, "candidate is not bound to this source, protected question, premises, and resource limits"));
    }
    if result.carrier_digest != carrier_digest {
        return Err(refuse(
            WdpPacketRefusalCodeV1::CarrierBinding,
            "candidate carrier differs from the supplied operation",
        ));
    }
    preflight_output(&result.output, &mut fuel)?;
    if result.result_digest != result_digest(result)? {
        return Err(refuse(
            WdpPacketRefusalCodeV1::ResultBinding,
            "candidate result commitment does not recompute",
        ));
    }
    match (&request.operation, &result.output) {
        (WdpPacketOperationV1::Hodge { d0, d1, flow }, WdpPacketOutputV1::Hodge { result }) => {
            hodge::replay_hodge_packet_with_budget(
                hodge_request(request, d0, d1, flow),
                result,
                &mut fuel,
            )
            .map_err(hodge_refusal)?;
        }
        (
            WdpPacketOperationV1::WeightedKrausGramStateTransport {
                dim_in,
                dim_out,
                terms,
                state_factor,
            },
            WdpPacketOutputV1::WeightedKrausGramStateTransport { image },
        ) => {
            let claimed = image.decode(&mut fuel)?;
            let replay = channel_image(*dim_in, *dim_out, terms, state_factor, &mut fuel)?;
            if GaussianMatrixV1::encode(&claimed) != replay {
                return Err(refuse(
                    WdpPacketRefusalCodeV1::ChannelResult,
                    "submitted image differs from fresh exact state transport",
                ));
            }
        }
        _ => {
            return Err(refuse(
                WdpPacketRefusalCodeV1::ResultKind,
                "candidate operation does not answer the protected question",
            ))
        }
    }
    Ok(WdpSourcePacketReplayV1 {
        schema_version: WDP_SOURCE_REPLAY_SCHEMA_V1.to_owned(),
        input_digest,
        carrier_digest,
        result_digest: result.result_digest.clone(),
        replay_scalar_ops: fuel.used(),
        authority_effect: AuthorityEffect::None,
    })
}

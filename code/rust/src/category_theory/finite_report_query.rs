
use std::collections::{BTreeMap, BTreeSet};
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum CarrierRole {
    Source,
    ReportCodomain,
    QueryCodomain,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum MapRole {
    Report,
    Query,
    Refinement,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReportQueryRefusal<X> {
    DuplicateIdentity { carrier: CarrierRole, position: usize },
    DuplicateAssignment { map: MapRole, source: X },
    MissingAssignment { map: MapRole, source: X },
    ExtraneousAssignment { map: MapRole, source: X },
    OutsideCodomain { map: MapRole, source: X },
}

impl<X: fmt::Debug> fmt::Display for ReportQueryRefusal<X> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{self:?}")
    }
}

impl<X: fmt::Debug> std::error::Error for ReportQueryRefusal<X> {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReportQueryProblem<X, A, B> {
    source: BTreeSet<X>,
    report_codomain: BTreeSet<A>,
    query_codomain: BTreeSet<B>,
    report: BTreeMap<X, A>,
    query: BTreeMap<X, B>,
}

fn carrier_or_refuse<T: Ord + Clone, X>(
    items: &[T],
    role: CarrierRole,
) -> Result<BTreeSet<T>, ReportQueryRefusal<X>> {
    let mut out = BTreeSet::new();
    for (position, item) in items.iter().enumerate() {
        if !out.insert(item.clone()) {
            return Err(ReportQueryRefusal::DuplicateIdentity {
                carrier: role,
                position,
            });
        }
    }
    Ok(out)
}

pub fn admit_total_table<X, V>(
    source: &BTreeSet<X>,
    codomain: &BTreeSet<V>,
    rows: &[(X, V)],
    map: MapRole,
) -> Result<BTreeMap<X, V>, ReportQueryRefusal<X>>
where
    X: Ord + Clone,
    V: Ord + Clone,
{
    let mut table = BTreeMap::new();
    for (x, v) in rows {
        if !source.contains(x) {
            return Err(ReportQueryRefusal::ExtraneousAssignment {
                map,
                source: x.clone(),
            });
        }
        if table.contains_key(x) {
            return Err(ReportQueryRefusal::DuplicateAssignment {
                map,
                source: x.clone(),
            });
        }
        if !codomain.contains(v) {
            return Err(ReportQueryRefusal::OutsideCodomain {
                map,
                source: x.clone(),
            });
        }
        table.insert(x.clone(), v.clone());
    }
    for x in source {
        if !table.contains_key(x) {
            return Err(ReportQueryRefusal::MissingAssignment {
                map,
                source: x.clone(),
            });
        }
    }
    Ok(table)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReportCollision<X, A, B> {
    pub first: X,
    pub second: X,
    pub report: A,
    pub first_query: B,
    pub second_query: B,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FactorizationCertificate<X, A, B> {
    pub realized_image: BTreeSet<A>,
    pub decoder: BTreeMap<A, B>,
    pub representative: BTreeMap<A, X>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReportQueryDecision<X, A, B> {
    Factorable(FactorizationCertificate<X, A, B>),
    Collision(ReportCollision<X, A, B>),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CertificateRefusal {
    RealizedImageMismatch,
    DecoderKeysMismatch,
    DecoderValueOutsideCodomain,
    RepresentativeKeysMismatch,
    RepresentativeNotInFiber,
    DecoderEquationFailure,
    CollisionPointUnknown,
    CollisionPointsEqual,
    CollisionReportMismatch,
    CollisionQueryMismatch,
    CollisionQueriesEqual,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RefinementRefusal<X, F> {
    ProblemsDiffer,
    RefinementTable(ReportQueryRefusal<F>),
    RefinementEquationFailure { source: X },
    CoarseCertificate(CertificateRefusal),
}

impl<X, A, B> ReportQueryProblem<X, A, B>
where
    X: Ord + Clone + fmt::Debug,
    A: Ord + Clone + fmt::Debug,
    B: Ord + Clone + fmt::Debug,
{
    pub fn new(
        source: &[X],
        report_codomain: &[A],
        query_codomain: &[B],
        report_rows: &[(X, A)],
        query_rows: &[(X, B)],
    ) -> Result<Self, ReportQueryRefusal<X>> {
        let source = carrier_or_refuse(source, CarrierRole::Source)?;
        let report_codomain = carrier_or_refuse(report_codomain, CarrierRole::ReportCodomain)?;
        let query_codomain = carrier_or_refuse(query_codomain, CarrierRole::QueryCodomain)?;
        let report = admit_total_table(&source, &report_codomain, report_rows, MapRole::Report)?;
        let query = admit_total_table(&source, &query_codomain, query_rows, MapRole::Query)?;
        Ok(Self {
            source,
            report_codomain,
            query_codomain,
            report,
            query,
        })
    }

    pub fn source(&self) -> &BTreeSet<X> {
        &self.source
    }
    pub fn report_codomain(&self) -> &BTreeSet<A> {
        &self.report_codomain
    }
    pub fn query_codomain(&self) -> &BTreeSet<B> {
        &self.query_codomain
    }
    pub fn report(&self) -> &BTreeMap<X, A> {
        &self.report
    }
    pub fn query(&self) -> &BTreeMap<X, B> {
        &self.query
    }

    pub fn realized_image(&self) -> BTreeSet<A> {
        self.report.values().cloned().collect()
    }

    pub fn decide(&self) -> ReportQueryDecision<X, A, B> {
        let mut decoder: BTreeMap<A, B> = BTreeMap::new();
        let mut representative: BTreeMap<A, X> = BTreeMap::new();
        for (x, a) in &self.report {
            let Some(b) = self.query.get(x) else { continue };
            match (decoder.get(a), representative.get(a)) {
                (Some(stored), Some(first)) => {
                    if stored != b {
                        return ReportQueryDecision::Collision(ReportCollision {
                            first: first.clone(),
                            second: x.clone(),
                            report: a.clone(),
                            first_query: stored.clone(),
                            second_query: b.clone(),
                        });
                    }
                }
                _ => {
                    decoder.insert(a.clone(), b.clone());
                    representative.insert(a.clone(), x.clone());
                }
            }
        }
        ReportQueryDecision::Factorable(FactorizationCertificate {
            realized_image: decoder.keys().cloned().collect(),
            decoder,
            representative,
        })
    }

    pub fn verify_decision(
        &self,
        decision: &ReportQueryDecision<X, A, B>,
    ) -> Result<(), CertificateRefusal> {
        match decision {
            ReportQueryDecision::Factorable(cert) => self.verify_factorization(cert),
            ReportQueryDecision::Collision(c) => self.verify_collision(c),
        }
    }

    pub fn verify_factorization(
        &self,
        cert: &FactorizationCertificate<X, A, B>,
    ) -> Result<(), CertificateRefusal> {
        let image = self.realized_image();
        if cert.realized_image != image {
            return Err(CertificateRefusal::RealizedImageMismatch);
        }
        let decoder_keys: BTreeSet<A> = cert.decoder.keys().cloned().collect();
        if decoder_keys != image {
            return Err(CertificateRefusal::DecoderKeysMismatch);
        }
        if cert
            .decoder
            .values()
            .any(|b| !self.query_codomain.contains(b))
        {
            return Err(CertificateRefusal::DecoderValueOutsideCodomain);
        }
        let rep_keys: BTreeSet<A> = cert.representative.keys().cloned().collect();
        if rep_keys != image {
            return Err(CertificateRefusal::RepresentativeKeysMismatch);
        }
        for (a, x) in &cert.representative {
            if self.report.get(x) != Some(a) {
                return Err(CertificateRefusal::RepresentativeNotInFiber);
            }
        }
        for (x, a) in &self.report {
            if cert.decoder.get(a) != self.query.get(x) {
                return Err(CertificateRefusal::DecoderEquationFailure);
            }
        }
        Ok(())
    }

    pub fn verify_collision(
        &self,
        c: &ReportCollision<X, A, B>,
    ) -> Result<(), CertificateRefusal> {
        let (Some(pa), Some(pb)) = (self.report.get(&c.first), self.report.get(&c.second)) else {
            return Err(CertificateRefusal::CollisionPointUnknown);
        };
        if c.first == c.second {
            return Err(CertificateRefusal::CollisionPointsEqual);
        }
        if pa != &c.report || pb != &c.report {
            return Err(CertificateRefusal::CollisionReportMismatch);
        }
        if self.query.get(&c.first) != Some(&c.first_query)
            || self.query.get(&c.second) != Some(&c.second_query)
        {
            return Err(CertificateRefusal::CollisionQueryMismatch);
        }
        if c.first_query == c.second_query {
            return Err(CertificateRefusal::CollisionQueriesEqual);
        }
        Ok(())
    }
}

pub fn transfer_refinement<X, F, C, B>(
    fine: &ReportQueryProblem<X, F, B>,
    coarse: &ReportQueryProblem<X, C, B>,
    h_rows: &[(F, C)],
    coarse_cert: &FactorizationCertificate<X, C, B>,
) -> Result<FactorizationCertificate<X, F, B>, RefinementRefusal<X, F>>
where
    X: Ord + Clone + fmt::Debug,
    F: Ord + Clone + fmt::Debug,
    C: Ord + Clone + fmt::Debug,
    B: Ord + Clone + fmt::Debug,
{
    if fine.source != coarse.source
        || fine.query != coarse.query
        || fine.query_codomain != coarse.query_codomain
    {
        return Err(RefinementRefusal::ProblemsDiffer);
    }
    let h = admit_total_table(
        &fine.report_codomain,
        &coarse.report_codomain,
        h_rows,
        MapRole::Refinement,
    )
    .map_err(RefinementRefusal::RefinementTable)?;
    for (x, a_f) in &fine.report {
        if h.get(a_f) != coarse.report.get(x) {
            return Err(RefinementRefusal::RefinementEquationFailure { source: x.clone() });
        }
    }
    coarse
        .verify_factorization(coarse_cert)
        .map_err(RefinementRefusal::CoarseCertificate)?;
    let mut decoder = BTreeMap::new();
    let mut representative = BTreeMap::new();
    for (x, a_f) in &fine.report {
        if representative.contains_key(a_f) {
            continue;
        }
        let value = h
            .get(a_f)
            .and_then(|a_c| coarse_cert.decoder.get(a_c))
            .cloned();
        let Some(value) = value else {
            return Err(RefinementRefusal::CoarseCertificate(
                CertificateRefusal::DecoderKeysMismatch,
            ));
        };
        decoder.insert(a_f.clone(), value);
        representative.insert(a_f.clone(), x.clone());
    }
    let cert = FactorizationCertificate {
        realized_image: decoder.keys().cloned().collect(),
        decoder,
        representative,
    };
    fine.verify_factorization(&cert)
        .map_err(RefinementRefusal::CoarseCertificate)?;
    Ok(cert)
}

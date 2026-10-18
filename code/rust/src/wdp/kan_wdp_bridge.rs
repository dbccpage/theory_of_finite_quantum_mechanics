
use std::collections::{BTreeMap, BTreeSet};

use omega_homology::errors::HomologicalError;
use omega_homology::simplicial::{Simplex, SimplicialComplex};
use omega_homotopy_type_theory::identity::{TermId, TypeId};
use omega_homotopy_type_theory::path::Path as HottPath;
use serde::{Deserialize, Serialize};

use crate::cochains::{Edge, Face, FiniteComplex};
use crate::types::AuthorityEffect;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ZeroDataLossReceipt {
    pub vertices_count: usize,
    pub edges_count: usize,
    pub faces_count: usize,
    pub vertices_lossless: bool,
    pub edges_lossless: bool,
    pub faces_lossless: bool,
    pub is_exact_match: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct KanHornFillingWitness {
    pub dimension: usize,
    pub missing_face_index: usize,
    pub horn_faces: Vec<Vec<String>>,
    pub filler_simplex: Vec<String>,
    pub completed_missing_face: Vec<String>,
    pub is_filled: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Hott2CellHomotopyWitness {
    pub path_left: HottPath,
    pub path_right: HottPath,
    pub composite_path: HottPath,
    pub homotopy_cell: (String, String, String),
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct KanSimplicialComplex {
    pub complex: SimplicialComplex,
    pub vertex_to_id: BTreeMap<String, usize>,
    pub id_to_vertex: Vec<String>,
    pub edge_orientations: BTreeMap<(usize, usize), (String, String)>,
    pub face_orientations: BTreeMap<(usize, usize, usize), (String, String, String)>,
    pub original_edge_order: Vec<Edge>,
    pub original_face_order: Vec<Face>,
    pub max_dimension: usize,
    pub authority_effect: AuthorityEffect,
}

impl KanSimplicialComplex {
    pub fn from_wdp_complex(wdp: &FiniteComplex) -> Result<Self, HomologicalError> {
        wdp.validate_simplicial_admission().map_err(|error| {
            HomologicalError::UnsupportedOperation(format!("simplicial admission refused: {error}"))
        })?;
        if wdp.vertices.is_empty() {
            return Err(HomologicalError::EmptyBasis);
        }

        let mut id_to_vertex: Vec<String> = wdp.vertices.iter().cloned().collect();
        id_to_vertex.sort();
        id_to_vertex.dedup();

        let vertex_to_id: BTreeMap<String, usize> = id_to_vertex
            .iter()
            .enumerate()
            .map(|(i, v)| (v.clone(), i))
            .collect();

        let mut simplices: Vec<Simplex> = Vec::new();

        for i in 0..id_to_vertex.len() {
            simplices.push(Simplex::new(vec![i])?);
        }

        let mut edge_orientations = BTreeMap::new();
        for (u, v) in &wdp.edges {
            let iu = *vertex_to_id
                .get(u)
                .ok_or_else(|| HomologicalError::BasisMismatch {
                    description: format!("vertex {u} not in vertex_to_id"),
                })?;
            let iv = *vertex_to_id
                .get(v)
                .ok_or_else(|| HomologicalError::BasisMismatch {
                    description: format!("vertex {v} not in vertex_to_id"),
                })?;
            let key = if iu < iv { (iu, iv) } else { (iv, iu) };
            edge_orientations.insert(key, (u.clone(), v.clone()));
            simplices.push(Simplex::from_unordered(vec![iu, iv])?);
        }

        let mut face_orientations = BTreeMap::new();
        for (a, b, c) in &wdp.faces {
            let ia = *vertex_to_id
                .get(a)
                .ok_or_else(|| HomologicalError::BasisMismatch {
                    description: format!("vertex {a} not in vertex_to_id"),
                })?;
            let ib = *vertex_to_id
                .get(b)
                .ok_or_else(|| HomologicalError::BasisMismatch {
                    description: format!("vertex {b} not in vertex_to_id"),
                })?;
            let ic = *vertex_to_id
                .get(c)
                .ok_or_else(|| HomologicalError::BasisMismatch {
                    description: format!("vertex {c} not in vertex_to_id"),
                })?;
            let mut sorted = [ia, ib, ic];
            sorted.sort_unstable();
            let key = (sorted[0], sorted[1], sorted[2]);
            face_orientations.insert(key, (a.clone(), b.clone(), c.clone()));
            simplices.push(Simplex::from_unordered(vec![ia, ib, ic])?);
        }

        let complex = SimplicialComplex::from_simplices(simplices)?;
        let max_dimension = complex.max_dimension();

        Ok(Self {
            complex,
            vertex_to_id,
            id_to_vertex,
            edge_orientations,
            face_orientations,
            original_edge_order: wdp.edges.clone(),
            original_face_order: wdp.faces.clone(),
            max_dimension,
            authority_effect: AuthorityEffect::None,
        })
    }

    fn validate_structure(&self) -> Result<(), HomologicalError> {
        let refuse = |detail: &str| HomologicalError::UnsupportedOperation(detail.to_string());
        if self.id_to_vertex.is_empty()
            || self.vertex_to_id.len() != self.id_to_vertex.len()
            || self.max_dimension != self.complex.max_dimension()
            || self.complex.count(0) != self.id_to_vertex.len()
        {
            return Err(refuse("invalid simplicial adapter dimensions/dictionary"));
        }
        for (id, name) in self.id_to_vertex.iter().enumerate() {
            if self.vertex_to_id.get(name) != Some(&id)
                || !self.complex.contains(&Simplex::new(vec![id])?)
            {
                return Err(refuse("simplicial vertex dictionary is not a bijection"));
            }
        }
        for dim in 0..=self.complex.max_dimension() {
            for simplex in self.complex.simplices(dim) {
                Simplex::new(simplex.vertices().to_vec())?;
                if simplex
                    .vertices()
                    .iter()
                    .any(|&id| id >= self.id_to_vertex.len())
                {
                    return Err(refuse(
                        "simplicial cell vertex is outside the adapter dictionary",
                    ));
                }
            }
        }
        let original = FiniteComplex::new(
            self.id_to_vertex.iter().cloned().collect(),
            self.original_edge_order.clone(),
            self.original_face_order.clone(),
        )
        .map_err(|error| refuse(&format!("invalid original cell data: {error}")))?;
        original
            .validate_simplicial_admission()
            .map_err(|error| refuse(&error.to_string()))?;
        for (u, v) in &self.original_edge_order {
            let a = self.vertex_to_id[u];
            let b = self.vertex_to_id[v];
            let key = if a < b { (a, b) } else { (b, a) };
            if !self.complex.contains(&Simplex::from_unordered(vec![a, b])?)
                || self.edge_orientations.get(&key) != Some(&(u.clone(), v.clone()))
            {
                return Err(refuse(
                    "original edge missing or orientation metadata inconsistent",
                ));
            }
        }
        for (a, b, c) in &self.original_face_order {
            let mut ids = [
                self.vertex_to_id[a],
                self.vertex_to_id[b],
                self.vertex_to_id[c],
            ];
            ids.sort();
            let key = (ids[0], ids[1], ids[2]);
            if !self.complex.contains(&Simplex::new(ids.to_vec())?)
                || self.face_orientations.get(&key) != Some(&(a.clone(), b.clone(), c.clone()))
            {
                return Err(refuse(
                    "original face missing or orientation metadata inconsistent",
                ));
            }
        }
        Ok(())
    }

    pub fn to_wdp_complex(&self) -> Result<FiniteComplex, HomologicalError> {
        self.validate_structure()?;
        let vertices: BTreeSet<String> = self.id_to_vertex.iter().cloned().collect();

        let mut edges = Vec::new();
        let mut seen_edges = BTreeSet::new();

        for (u, v) in &self.original_edge_order {
            if let (Some(&iu), Some(&iv)) = (self.vertex_to_id.get(u), self.vertex_to_id.get(v)) {
                let key = if iu < iv { (iu, iv) } else { (iv, iu) };
                if self
                    .complex
                    .contains(&Simplex::from_unordered(vec![iu, iv])?)
                {
                    edges.push((u.clone(), v.clone()));
                    seen_edges.insert(key);
                }
            }
        }

        for s in self.complex.simplices(1) {
            let v = s.vertices();
            let key = (v[0], v[1]);
            if !seen_edges.contains(&key) {
                if let Some(oriented) = self.edge_orientations.get(&key) {
                    edges.push(oriented.clone());
                } else {
                    edges.push((
                        self.id_to_vertex[v[0]].clone(),
                        self.id_to_vertex[v[1]].clone(),
                    ));
                }
                seen_edges.insert(key);
            }
        }

        let mut faces = Vec::new();
        let mut seen_faces = BTreeSet::new();

        for (a, b, c) in &self.original_face_order {
            if let (Some(&ia), Some(&ib), Some(&ic)) = (
                self.vertex_to_id.get(a),
                self.vertex_to_id.get(b),
                self.vertex_to_id.get(c),
            ) {
                let mut sorted = [ia, ib, ic];
                sorted.sort_unstable();
                let key = (sorted[0], sorted[1], sorted[2]);
                if self
                    .complex
                    .contains(&Simplex::from_unordered(vec![ia, ib, ic])?)
                {
                    faces.push((a.clone(), b.clone(), c.clone()));
                    seen_faces.insert(key);
                }
            }
        }

        for s in self.complex.simplices(2) {
            let v = s.vertices();
            let key = (v[0], v[1], v[2]);
            if !seen_faces.contains(&key) {
                if let Some(oriented) = self.face_orientations.get(&key) {
                    faces.push(oriented.clone());
                } else {
                    faces.push((
                        self.id_to_vertex[v[0]].clone(),
                        self.id_to_vertex[v[1]].clone(),
                        self.id_to_vertex[v[2]].clone(),
                    ));
                }
                seen_faces.insert(key);
            }
        }

        FiniteComplex::new(vertices, edges, faces).map_err(|e| {
            HomologicalError::UnsupportedOperation(format!("reconstructed complex error: {e}"))
        })
    }

    pub fn verify_zero_data_loss(
        &self,
        original: &FiniteComplex,
    ) -> Result<ZeroDataLossReceipt, HomologicalError> {
        let reconstructed = self.to_wdp_complex()?;
        let vertices_lossless = reconstructed.vertices == original.vertices;
        let edges_lossless = reconstructed.edges == original.edges;
        let faces_lossless = reconstructed.faces == original.faces;
        let is_exact_match = vertices_lossless && edges_lossless && faces_lossless;

        Ok(ZeroDataLossReceipt {
            vertices_count: self.id_to_vertex.len(),
            edges_count: self.complex.count(1),
            faces_count: self.complex.count(2),
            vertices_lossless,
            edges_lossless,
            faces_lossless,
            is_exact_match,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn extend_with_simplex(
        &self,
        simplex_vertices: &[String],
    ) -> Result<Self, HomologicalError> {
        if simplex_vertices.is_empty() {
            return Err(HomologicalError::EmptyBasis);
        }

        let mut id_to_vertex = self.id_to_vertex.clone();
        let mut vertex_to_id = self.vertex_to_id.clone();

        for name in simplex_vertices {
            if !vertex_to_id.contains_key(name) {
                let new_id = id_to_vertex.len();
                id_to_vertex.push(name.clone());
                vertex_to_id.insert(name.clone(), new_id);
            }
        }

        let mut all_simplices: Vec<Simplex> = Vec::new();
        for dim in 0..=self.complex.max_dimension() {
            for s in self.complex.simplices(dim) {
                all_simplices.push(s.clone());
            }
        }

        let new_indices: Vec<usize> = simplex_vertices
            .iter()
            .map(|name| vertex_to_id[name])
            .collect();
        all_simplices.push(Simplex::from_unordered(new_indices)?);

        let new_complex = SimplicialComplex::from_simplices(all_simplices)?;
        let max_dimension = new_complex.max_dimension();

        Ok(Self {
            complex: new_complex,
            vertex_to_id,
            id_to_vertex,
            edge_orientations: self.edge_orientations.clone(),
            face_orientations: self.face_orientations.clone(),
            original_edge_order: self.original_edge_order.clone(),
            original_face_order: self.original_face_order.clone(),
            max_dimension,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn extend_to_kan_n_simplex(
        &self,
        apex_vertices: &[String],
    ) -> Result<Self, HomologicalError> {
        let mut all_vertices = self.id_to_vertex.clone();
        for apex in apex_vertices {
            if !all_vertices.contains(apex) {
                all_vertices.push(apex.clone());
            }
        }
        self.extend_with_simplex(&all_vertices)
    }

    pub fn verify_kan_horn_filling(
        &self,
        simplex_vertices: &[String],
        missing_k: usize,
    ) -> Result<KanHornFillingWitness, HomologicalError> {
        self.validate_structure()?;
        let n = simplex_vertices.len().saturating_sub(1);
        if n < 1 {
            return Err(HomologicalError::InvalidDegree(n as i32));
        }
        if missing_k > n {
            return Err(HomologicalError::BasisMismatch {
                description: format!(
                    "missing face index {missing_k} exceeds simplex dimension {n}"
                ),
            });
        }

        let mut indices: Vec<usize> = Vec::with_capacity(simplex_vertices.len());
        for name in simplex_vertices {
            let id =
                *self
                    .vertex_to_id
                    .get(name)
                    .ok_or_else(|| HomologicalError::BasisMismatch {
                        description: format!("vertex {name} not in Kan complex dictionary"),
                    })?;
            indices.push(id);
        }
        let canonical_simplex = Simplex::from_unordered(indices)?;
        let sorted_vertices = canonical_simplex.vertices();

        let filler_present = self.complex.contains(&canonical_simplex);

        let mut horn_faces = Vec::new();
        let mut completed_missing_face = Vec::new();
        let mut all_horn_faces_present = true;

        for i in 0..=n {
            let mut face_v = sorted_vertices.to_vec();
            face_v.remove(i);
            let face_simplex = Simplex::new(face_v)?;
            let face_present = self.complex.contains(&face_simplex);

            let face_names: Vec<String> = face_simplex
                .vertices()
                .iter()
                .map(|&idx| self.id_to_vertex[idx].clone())
                .collect();

            if i == missing_k {
                completed_missing_face = face_names;
            } else {
                if !face_present {
                    all_horn_faces_present = false;
                }
                horn_faces.push(face_names);
            }
        }

        let is_filled = filler_present && all_horn_faces_present;

        let filler_names: Vec<String> = sorted_vertices
            .iter()
            .map(|&idx| self.id_to_vertex[idx].clone())
            .collect();

        Ok(KanHornFillingWitness {
            dimension: n,
            missing_face_index: missing_k,
            horn_faces,
            filler_simplex: filler_names,
            completed_missing_face,
            is_filled,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn export_1_cells_as_hott_paths(
        &self,
        type_id: &str,
    ) -> Result<Vec<HottPath>, HomologicalError> {
        let mut paths = Vec::new();
        for (u, v) in self.to_wdp_complex()?.edges {
            let p = HottPath {
                type_id: TypeId(type_id.to_string()),
                source: TermId(u.clone()),
                target: TermId(v.clone()),
                path_ref: format!("{u}->{v}"),
            };
            p.validate()
                .map_err(|e| HomologicalError::UnsupportedOperation(format!("{}", e)))?;
            paths.push(p);
        }
        Ok(paths)
    }

    pub fn export_2_cells_as_hott_homotopies(
        &self,
        type_id: &str,
    ) -> Result<Vec<Hott2CellHomotopyWitness>, HomologicalError> {
        let mut homotopies = Vec::new();
        for (a, b, c) in self.to_wdp_complex()?.faces {
            let path_ab = HottPath {
                type_id: TypeId(type_id.to_string()),
                source: TermId(a.clone()),
                target: TermId(b.clone()),
                path_ref: format!("{a}->{b}"),
            };
            let path_bc = HottPath {
                type_id: TypeId(type_id.to_string()),
                source: TermId(b.clone()),
                target: TermId(c.clone()),
                path_ref: format!("{b}->{c}"),
            };
            let path_ac = HottPath {
                type_id: TypeId(type_id.to_string()),
                source: TermId(a.clone()),
                target: TermId(c.clone()),
                path_ref: format!("{a}->{c}"),
            };
            homotopies.push(Hott2CellHomotopyWitness {
                path_left: path_ab,
                path_right: path_bc,
                composite_path: path_ac,
                homotopy_cell: (a, b, c),
                authority_effect: AuthorityEffect::None,
            });
        }
        Ok(homotopies)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zero_data_loss_ingestion_and_roundtrip() {
        let vertices = BTreeSet::from(["v0".to_string(), "v1".to_string(), "v2".to_string()]);
        let edges = vec![
            ("v0".to_string(), "v1".to_string()),
            ("v1".to_string(), "v2".to_string()),
            ("v2".to_string(), "v0".to_string()),
        ];
        let faces = vec![("v0".to_string(), "v1".to_string(), "v2".to_string())];

        let wdp = FiniteComplex::new(vertices, edges, faces).unwrap();
        let kan = KanSimplicialComplex::from_wdp_complex(&wdp).unwrap();

        assert_eq!(kan.max_dimension, 2);
        assert_eq!(kan.complex.count(0), 3);
        assert_eq!(kan.complex.count(1), 3);
        assert_eq!(kan.complex.count(2), 1);

        let receipt = kan.verify_zero_data_loss(&wdp).unwrap();
        assert!(receipt.is_exact_match);
        assert!(receipt.vertices_lossless);
        assert!(receipt.edges_lossless);
        assert!(receipt.faces_lossless);
        assert_eq!(receipt.authority_effect, AuthorityEffect::None);

        let reconstructed = kan.to_wdp_complex().unwrap();
        assert_eq!(reconstructed, wdp);
    }

    #[test]
    fn test_higher_dimensional_kan_simplex_extension() {
        let vertices = BTreeSet::from(["A".to_string(), "B".to_string(), "C".to_string()]);
        let edges = vec![
            ("A".to_string(), "B".to_string()),
            ("B".to_string(), "C".to_string()),
            ("C".to_string(), "A".to_string()),
        ];
        let hollow = FiniteComplex::new(vertices, edges, vec![]).unwrap();
        let kan_triangle = KanSimplicialComplex::from_wdp_complex(&hollow).unwrap();

        assert_eq!(kan_triangle.max_dimension, 1);

        let kan_tetrahedron = kan_triangle
            .extend_to_kan_n_simplex(&["D".to_string()])
            .unwrap();

        assert_eq!(kan_tetrahedron.max_dimension, 3);
        assert_eq!(kan_tetrahedron.complex.count(0), 4);
        assert_eq!(kan_tetrahedron.complex.count(1), 6);
        assert_eq!(kan_tetrahedron.complex.count(2), 4);
        assert_eq!(kan_tetrahedron.complex.count(3), 1);

        assert!(kan_tetrahedron.complex.verify_boundary_law().unwrap());

        let tet_vertices = vec![
            "A".to_string(),
            "B".to_string(),
            "C".to_string(),
            "D".to_string(),
        ];
        for k in 0..=3 {
            let witness = kan_tetrahedron
                .verify_kan_horn_filling(&tet_vertices, k)
                .unwrap();
            assert!(witness.is_filled);
            assert_eq!(witness.dimension, 3);
            assert_eq!(witness.missing_face_index, k);
            assert_eq!(witness.horn_faces.len(), 3);
            assert_eq!(witness.authority_effect, AuthorityEffect::None);
        }

        let kan_4simplex = kan_tetrahedron
            .extend_to_kan_n_simplex(&["E".to_string()])
            .unwrap();

        assert_eq!(kan_4simplex.max_dimension, 4);
        assert_eq!(kan_4simplex.complex.count(0), 5);
        assert_eq!(kan_4simplex.complex.count(1), 10);
        assert_eq!(kan_4simplex.complex.count(2), 10);
        assert_eq!(kan_4simplex.complex.count(3), 5);
        assert_eq!(kan_4simplex.complex.count(4), 1);
        assert_eq!(kan_4simplex.complex.euler_characteristic(), 1);

        let simplex_4_vertices = vec![
            "A".to_string(),
            "B".to_string(),
            "C".to_string(),
            "D".to_string(),
            "E".to_string(),
        ];
        let witness_4 = kan_4simplex
            .verify_kan_horn_filling(&simplex_4_vertices, 2)
            .unwrap();
        assert!(witness_4.is_filled);
        assert_eq!(witness_4.dimension, 4);
        assert_eq!(witness_4.horn_faces.len(), 4);
    }

    #[test]
    fn test_homology_betti_numbers_via_omega_homology() {
        let vertices = BTreeSet::from(["0".to_string(), "1".to_string(), "2".to_string()]);
        let edges = vec![
            ("0".to_string(), "1".to_string()),
            ("1".to_string(), "2".to_string()),
            ("2".to_string(), "0".to_string()),
        ];
        let hollow = FiniteComplex::new(vertices.clone(), edges.clone(), vec![]).unwrap();
        let kan_hollow = KanSimplicialComplex::from_wdp_complex(&hollow).unwrap();

        let betti_hollow = kan_hollow.complex.rational_betti_numbers().unwrap();
        assert_eq!(betti_hollow, vec![1, 1]);
        assert_eq!(kan_hollow.complex.euler_characteristic(), 0);

        let faces = vec![("0".to_string(), "1".to_string(), "2".to_string())];
        let filled = FiniteComplex::new(vertices, edges, faces).unwrap();
        let kan_filled = KanSimplicialComplex::from_wdp_complex(&filled).unwrap();

        let betti_filled = kan_filled.complex.rational_betti_numbers().unwrap();
        assert_eq!(betti_filled, vec![1, 0, 0]);
        assert_eq!(kan_filled.complex.euler_characteristic(), 1);
    }

    #[test]
    fn test_hott_paths_and_homotopies_export() {
        let vertices = BTreeSet::from(["x".to_string(), "y".to_string(), "z".to_string()]);
        let edges = vec![
            ("x".to_string(), "y".to_string()),
            ("y".to_string(), "z".to_string()),
            ("x".to_string(), "z".to_string()),
        ];
        let faces = vec![("x".to_string(), "y".to_string(), "z".to_string())];
        let wdp = FiniteComplex::new(vertices, edges, faces).unwrap();
        let kan = KanSimplicialComplex::from_wdp_complex(&wdp).unwrap();

        let paths = kan.export_1_cells_as_hott_paths("TypeX").unwrap();
        assert_eq!(paths.len(), 3);
        for p in &paths {
            assert!(p.validate().is_ok());
            assert_eq!(p.type_id.0, "TypeX");
        }

        let homotopies = kan.export_2_cells_as_hott_homotopies("TypeX").unwrap();
        assert_eq!(homotopies.len(), 1);
        let h = &homotopies[0];
        assert_eq!(
            h.homotopy_cell,
            ("x".to_string(), "y".to_string(), "z".to_string())
        );
        assert_eq!(h.path_left.path_ref, "x->y");
        assert_eq!(h.path_right.path_ref, "y->z");
        assert_eq!(h.composite_path.path_ref, "x->z");
        assert_eq!(h.authority_effect, AuthorityEffect::None);
    }
    #[test]
    fn refuses_lossy_multicell_or_incomplete_boundary_ingestion() {
        let digon = FiniteComplex::new(
            BTreeSet::from(["a".into(), "b".into()]),
            vec![("a".into(), "b".into()), ("b".into(), "a".into())],
            vec![],
        )
        .unwrap();
        assert!(KanSimplicialComplex::from_wdp_complex(&digon).is_err());
        let incomplete = FiniteComplex {
            vertices: BTreeSet::from(["a".into(), "b".into(), "c".into()]),
            edges: vec![("a".into(), "b".into())],
            faces: vec![("a".into(), "b".into(), "c".into())],
        };
        assert!(KanSimplicialComplex::from_wdp_complex(&incomplete).is_err());
        let mut filled = FiniteComplex::new(
            incomplete.vertices.clone(),
            vec![
                ("a".into(), "b".into()),
                ("b".into(), "c".into()),
                ("a".into(), "c".into()),
            ],
            incomplete.faces.clone(),
        )
        .unwrap();
        filled.faces.push(("c".into(), "b".into(), "a".into()));
        assert!(KanSimplicialComplex::from_wdp_complex(&filled).is_err());
    }
    #[test]
    fn malformed_public_dictionary_or_original_cells_refuse_without_dropping() {
        let original = FiniteComplex::new(
            BTreeSet::from(["a".into(), "b".into()]),
            vec![("a".into(), "b".into())],
            vec![],
        )
        .unwrap();
        let mut adapter = KanSimplicialComplex::from_wdp_complex(&original).unwrap();
        adapter
            .original_edge_order
            .push(("a".into(), "ghost".into()));
        assert!(adapter.to_wdp_complex().is_err());
        let mut adapter = KanSimplicialComplex::from_wdp_complex(&original).unwrap();
        adapter.id_to_vertex.pop();
        assert!(adapter.to_wdp_complex().is_err());
        assert!(adapter
            .verify_kan_horn_filling(&["a".into(), "b".into()], 0)
            .is_err());
    }
}

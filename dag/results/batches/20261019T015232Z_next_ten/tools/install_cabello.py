import hashlib,json,shutil
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');STAGING=Path(__file__).resolve().parent
RUN=ROOT/'dag/results/FQ-CABELLO-FRAME-POLYTOPE-146/runs/20261019T015232Z_staged'
upstream=Path(r'C:\Users\a343o\source\repos\the_symbol_game\omega_engine\crates_rs\omega_quantum_physics\src\frame_function_polytope.rs')
source=upstream.read_text();needle='''        let edges = self.degree_two_edges()?;
        let frames = self.frames.len();'''
insert='''        self.vertices_with_statistics(limit).map(|(vertices, _)| vertices)
    }

    /// Retain the actual number of size-rank supports visited, not a claimed census.
    pub fn vertices_with_statistics(
        &self, limit: usize,
    ) -> Result<(Vec<Vec<Rational>>, usize), FramePolytopeError> {
        let edges = self.degree_two_edges()?;
        let frames = self.frames.len();'''
if source.count(needle)!=1:raise ValueError('Upstream enumeration layout changed')
source=source.replace(needle,insert).replace('Ok(found.into_iter().collect())','Ok((found.into_iter().collect(), examined))')
header='// Local source port from the_symbol_game/frame_function_polytope.rs.\n// Original SHA256: '+hashlib.sha256(upstream.read_bytes()).hexdigest()+'\n// Only API extension: expose the completed support-visit count.\n'
(ROOT/'code/rust/src/finite_probability/frame_polytope.rs').write_bytes((header+source).encode())
for a,b in [('cabello_frame.py','code/python/src/qm/cabello_frame.py'),('cabello_certificates.rs','code/rust/src/finite_probability/cabello_certificates.rs'),('cabello_replay.rs','code/rust/src/finite_probability/examples/cabello_replay.rs')]:shutil.copyfile(STAGING/a,ROOT/b)
p=ROOT/'code/rust/src/finite_probability/lib.rs';s=p.read_text().replace('pub mod born_ray;','pub mod born_ray;\npub mod frame_polytope;\npub mod cabello_certificates;');p.write_bytes(s.encode())
p=ROOT/'code/rust/src/finite_probability/Cargo.toml';s=p.read_text().replace('[dependencies]','[dependencies]\nomega_combinatorics = { path = "C:/Users/a343o/source/repos/the_symbol_game/omega_engine/crates_rs/omega_combinatorics" }');p.write_bytes(s.encode())
p=ROOT/'code/rust/Cargo.lock';s=p.read_text();start=s.index('name = "tfqm_finite_probability"');end=s.index('\n[[package]]',start);block=s[start:end]
if ' "omega_combinatorics",' not in block:block=block.replace('dependencies = [','dependencies = [\n "omega_combinatorics",');s=s[:start]+block+s[end:]
p.write_bytes(s.encode())
(RUN/'p0/source_port.json').write_bytes((json.dumps({'upstream':str(upstream),'upstream_sha256':hashlib.sha256(upstream.read_bytes()).hexdigest(),'local':'code/rust/src/finite_probability/frame_polytope.rs','changes':'Preserve the original exact enumeration/tomography/inertia algorithms, exposing the actual completed support count through one wrapper API.','acceptance':'Source reuse only; new native and independent checks remain required.'},indent=2)+'\n').encode())

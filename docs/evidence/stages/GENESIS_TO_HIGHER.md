# Stage GENESIS_TO_HIGHER

Part of the [evidence map](../README.md). AuthorityEffect: None.

Nodes: 12. Grades: E1 11, E3 1. Statuses: PROVED_PROSE 1, IMPORTED_ASSUMPTION 3, OPEN 8.

| Node | Status | Grade | Statement | Counted in-repo evidence | Flags |
|---|---|---|---|---|---|
| [GTH-SHADOW](../nodes/GTH-SHADOW.md) | `OPEN` | E3 | Narrowed boundary, status left OPEN. On the triangle with vertices 0, 1 and 2, the edges are (0, 1), (0, 2) and (1, 2). The target of (0,... | [CampaignGthShadow.lean](../../../lean4/CampaignGthShadow.lean): `face_id_01`, `face_id_02`, `face_id_12` +3<br>[gth-shadow.py](../../../checks/independent/gth-shadow.py)<br>[gth-shadow.md](../../../dag/derivations/independent/gth-shadow.md)<br>[gth_shadow.md](../../../dag/derivations/independent/gth_shadow.md)<br>+1 more file(s) | - |
| [GTH-TRUNC](../nodes/GTH-TRUNC.md) | `OPEN` | E1 | Let a finite shadow be a finite semi-simplicial set or a finite globular set as in GTH-SHADOW. Its set of path components, pi_0, is the q... | [gth_trunc.md](../../../dag/derivations/independent/gth_trunc.md) | - |
| [GTH-HORNS](../nodes/GTH-HORNS.md) | `OPEN` | E1 | The horn Lambda^k\[n\] is the union of all faces of the standard n-simplex except the face opposite vertex k. The horn is inner when 0 \< k... | [gth_horns.md](../../../dag/derivations/independent/gth_horns.md) | - |
| [GTH-HOTT-MODEL](../nodes/GTH-HOTT-MODEL.md) | `OPEN` | E1 | No deep embedding of a dependent type theory, and no finite model of such a theory, is constructed. The fragment in view has identity typ... | [gth_hott_model.md](../../../dag/derivations/independent/gth_hott_model.md) | - |
| [GTH-IMPORT-UNIVALENT-UNIVERSE](../nodes/GTH-IMPORT-UNIVALENT-UNIVERSE.md) | `IMPORTED_ASSUMPTION` | E1 | Assumed, and not derived from Genesis admission or from any finite model: a univalent universe in the sense of the Homotopy Type Theory b... | [gth_import_univalent_universe.md](../../../dag/derivations/independent/gth_import_univalent_universe.md) | - |
| [GTH-IMPORT-INFTY-GROUPOID](../nodes/GTH-IMPORT-INFTY-GROUPOID.md) | `IMPORTED_ASSUMPTION` | E1 | Assumed, and not derived: an infinity-groupoid in the sense of a Kan complex, a simplicial set in which every horn has a filler, as used... | [gth_import_infty_groupoid.md](../../../dag/derivations/independent/gth_import_infty_groupoid.md) | - |
| [GTH-IMPORT-INFTY-1-CATEGORY](../nodes/GTH-IMPORT-INFTY-1-CATEGORY.md) | `IMPORTED_ASSUMPTION` | E1 | Assumed, and not derived: an (infinity,1)-category in the sense of a quasicategory, a simplicial set in which every inner horn has a fill... | [gth_import_infty_1_category.md](../../../dag/derivations/independent/gth_import_infty_1_category.md) | - |
| [GTH-LANG-CORE](../nodes/GTH-LANG-CORE.md) | `OPEN` | E1 | The priced admission language is not defined. The reading intended for its primitives, which this node does not derive, is: a two-valued... | [gth_lang_core.md](../../../dag/derivations/independent/gth_lang_core.md) | - |
| [GTH-LANG-REFLECT](../nodes/GTH-LANG-REFLECT.md) | `OPEN` | E1 | No quotation layer for the priced admission language is defined, because that language is not defined. Reflection here means a later laye... | [gth_lang_reflect.md](../../../dag/derivations/independent/gth_lang_reflect.md) | - |
| [GTH-LANG-INTERPRET](../nodes/GTH-LANG-INTERPRET.md) | `OPEN` | E1 | The following three items are targets, not theorems. (a) A stated fragment of Martin-Lof type theory with identity types. (b) Finite semi... | [gth_lang_interpret.md](../../../dag/derivations/independent/gth_lang_interpret.md) | - |
| [GTH-LANG-IMPORT](../nodes/GTH-LANG-IMPORT.md) | `OPEN` | E1 | An import record for the priced admission language names a theory, the axioms added, the cost as the sentences the core does not derive,... | [gth_lang_import.md](../../../dag/derivations/independent/gth_lang_import.md) | - |
| [GTH-LANG-LIMITS](../nodes/GTH-LANG-LIMITS.md) | `PROVED_PROSE` | E1 | Let S be a theory in classical first-order logic with a primitive recursive coding of its syntax. Write code(psi) for the code of a sente... | [gth_lang_limits.md](../../../dag/derivations/independent/gth_lang_limits.md) | - |


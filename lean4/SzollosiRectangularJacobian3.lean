import SzollosiRectangularJacobianCore
namespace MUB.SzollosiRectangularReflection
open SzollosiTermExpansion SzollosiNativeInterval SzollosiIntervalExclusion
open SzollosiExecutableSystem SzollosiQuadraticSystem SzollosiNativeReflection
open SzollosiRectangularExclusion SparseRectangularExclusion
set_option maxRecDepth 30000
set_option maxHeartbeats 100000000

-- Native rectangular receipt SHA-256: eccd3b1c075d0058cf729e2aa0af5e210860da93d2178ea09a9d5cfb3b820a76
-- Executable system SHA-256: 1367d390da36e5ccf65abbc8fbf529ff07f9e154c277bb14c1cd8c36ba24c947
-- Lean coefficient reference SHA-256: 44656965bb72e735febfc69c1bcd599adbeea2e8512ebd6141025f8524e5d2df
-- Native request SHA-256: d44dfd0b14fb610ba354ba2bedbea03c56df5f5d18d141cd58a4bd52c27a76af

def nativeJacobianRow240 : List (Nat × Bounds) := [(116,⟨(-2),(2)⟩),(117,⟨(-2),(2)⟩)]
theorem nativeJacobianRow240_eq :
    nativeJacobianRow240 = expectedJacobianRow 240 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow241 : List (Nat × Bounds) := [(118,⟨(-2),(2)⟩),(119,⟨(-2),(2)⟩)]
theorem nativeJacobianRow241_eq :
    nativeJacobianRow241 = expectedJacobianRow 241 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow242 : List (Nat × Bounds) := [(120,⟨(-2),(2)⟩),(121,⟨(-2),(2)⟩)]
theorem nativeJacobianRow242_eq :
    nativeJacobianRow242 = expectedJacobianRow 242 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow243 : List (Nat × Bounds) := [(122,⟨(-2),(2)⟩),(123,⟨(-2),(2)⟩)]
theorem nativeJacobianRow243_eq :
    nativeJacobianRow243 = expectedJacobianRow 243 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow244 : List (Nat × Bounds) := [(124,⟨(-2),(2)⟩),(125,⟨(-2),(2)⟩)]
theorem nativeJacobianRow244_eq :
    nativeJacobianRow244 = expectedJacobianRow 244 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow245 : List (Nat × Bounds) := [(126,⟨(-2),(2)⟩),(127,⟨(-2),(2)⟩)]
theorem nativeJacobianRow245_eq :
    nativeJacobianRow245 = expectedJacobianRow 245 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow246 : List (Nat × Bounds) := [(128,⟨(-2),(2)⟩),(129,⟨(-2),(2)⟩)]
theorem nativeJacobianRow246_eq :
    nativeJacobianRow246 = expectedJacobianRow 246 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow247 : List (Nat × Bounds) := [(130,⟨(-2),(2)⟩),(131,⟨(-2),(2)⟩)]
theorem nativeJacobianRow247_eq :
    nativeJacobianRow247 = expectedJacobianRow 247 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow248 : List (Nat × Bounds) := [(132,⟨(-2),(2)⟩),(133,⟨(-2),(2)⟩)]
theorem nativeJacobianRow248_eq :
    nativeJacobianRow248 = expectedJacobianRow 248 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow249 : List (Nat × Bounds) := [(134,⟨(-2),(2)⟩),(135,⟨(-2),(2)⟩)]
theorem nativeJacobianRow249_eq :
    nativeJacobianRow249 = expectedJacobianRow 249 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow250 : List (Nat × Bounds) := [(136,⟨(-2),(2)⟩),(137,⟨(-2),(2)⟩)]
theorem nativeJacobianRow250_eq :
    nativeJacobianRow250 = expectedJacobianRow 250 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow251 : List (Nat × Bounds) := [(138,⟨(-2),(2)⟩),(139,⟨(-2),(2)⟩)]
theorem nativeJacobianRow251_eq :
    nativeJacobianRow251 = expectedJacobianRow 251 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow252 : List (Nat × Bounds) := [(140,⟨(-2),(2)⟩),(141,⟨(-2),(2)⟩)]
theorem nativeJacobianRow252_eq :
    nativeJacobianRow252 = expectedJacobianRow 252 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow253 : List (Nat × Bounds) := [(142,⟨(-2),(2)⟩),(143,⟨(-2),(2)⟩)]
theorem nativeJacobianRow253_eq :
    nativeJacobianRow253 = expectedJacobianRow 253 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow254 : List (Nat × Bounds) := [(144,⟨(-2),(2)⟩),(145,⟨(-2),(2)⟩)]
theorem nativeJacobianRow254_eq :
    nativeJacobianRow254 = expectedJacobianRow 254 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow255 : List (Nat × Bounds) := [(146,⟨(-2),(2)⟩),(147,⟨(-2),(2)⟩)]
theorem nativeJacobianRow255_eq :
    nativeJacobianRow255 = expectedJacobianRow 255 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow256 : List (Nat × Bounds) := [(148,⟨(-2),(2)⟩),(149,⟨(-2),(2)⟩)]
theorem nativeJacobianRow256_eq :
    nativeJacobianRow256 = expectedJacobianRow 256 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow257 : List (Nat × Bounds) := [(150,⟨(-2),(2)⟩),(151,⟨(-2),(2)⟩)]
theorem nativeJacobianRow257_eq :
    nativeJacobianRow257 = expectedJacobianRow 257 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow258 : List (Nat × Bounds) := [(152,⟨(-2),(2)⟩),(153,⟨(-2),(2)⟩)]
theorem nativeJacobianRow258_eq :
    nativeJacobianRow258 = expectedJacobianRow 258 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow259 : List (Nat × Bounds) := [(154,⟨(-2),(2)⟩),(155,⟨(-2),(2)⟩)]
theorem nativeJacobianRow259_eq :
    nativeJacobianRow259 = expectedJacobianRow 259 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow260 : List (Nat × Bounds) := [(156,⟨(-2),(2)⟩),(157,⟨(-2),(2)⟩)]
theorem nativeJacobianRow260_eq :
    nativeJacobianRow260 = expectedJacobianRow 260 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow261 : List (Nat × Bounds) := [(158,⟨(-2),(2)⟩),(159,⟨(-2),(2)⟩)]
theorem nativeJacobianRow261_eq :
    nativeJacobianRow261 = expectedJacobianRow 261 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow262 : List (Nat × Bounds) := [(160,⟨(-2),(2)⟩),(161,⟨(-2),(2)⟩)]
theorem nativeJacobianRow262_eq :
    nativeJacobianRow262 = expectedJacobianRow 262 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow263 : List (Nat × Bounds) := [(162,⟨(-2),(2)⟩),(163,⟨(-2),(2)⟩)]
theorem nativeJacobianRow263_eq :
    nativeJacobianRow263 = expectedJacobianRow 263 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow264 : List (Nat × Bounds) := [(164,⟨(-2),(2)⟩),(165,⟨(-2),(2)⟩)]
theorem nativeJacobianRow264_eq :
    nativeJacobianRow264 = expectedJacobianRow 264 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow265 : List (Nat × Bounds) := [(166,⟨(-2),(2)⟩),(167,⟨(-2),(2)⟩)]
theorem nativeJacobianRow265_eq :
    nativeJacobianRow265 = expectedJacobianRow 265 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow266 : List (Nat × Bounds) := [(168,⟨(-2),(2)⟩),(169,⟨(-2),(2)⟩)]
theorem nativeJacobianRow266_eq :
    nativeJacobianRow266 = expectedJacobianRow 266 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow267 : List (Nat × Bounds) := [(170,⟨(-2),(2)⟩),(171,⟨(-2),(2)⟩)]
theorem nativeJacobianRow267_eq :
    nativeJacobianRow267 = expectedJacobianRow 267 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow268 : List (Nat × Bounds) := [(172,⟨(-2),(2)⟩),(173,⟨(-2),(2)⟩)]
theorem nativeJacobianRow268_eq :
    nativeJacobianRow268 = expectedJacobianRow 268 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow269 : List (Nat × Bounds) := [(174,⟨(-2),(2)⟩),(175,⟨(-2),(2)⟩)]
theorem nativeJacobianRow269_eq :
    nativeJacobianRow269 = expectedJacobianRow 269 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow270 : List (Nat × Bounds) := [(176,⟨(-2),(2)⟩),(177,⟨(-2),(2)⟩)]
theorem nativeJacobianRow270_eq :
    nativeJacobianRow270 = expectedJacobianRow 270 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow271 : List (Nat × Bounds) := [(178,⟨(-2),(2)⟩),(179,⟨(-2),(2)⟩)]
theorem nativeJacobianRow271_eq :
    nativeJacobianRow271 = expectedJacobianRow 271 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow272 : List (Nat × Bounds) := [(180,⟨(-2),(2)⟩),(181,⟨(-2),(2)⟩)]
theorem nativeJacobianRow272_eq :
    nativeJacobianRow272 = expectedJacobianRow 272 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow273 : List (Nat × Bounds) := [(182,⟨(-2),(2)⟩),(183,⟨(-2),(2)⟩)]
theorem nativeJacobianRow273_eq :
    nativeJacobianRow273 = expectedJacobianRow 273 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow274 : List (Nat × Bounds) := [(184,⟨(-2),(2)⟩),(185,⟨(-2),(2)⟩)]
theorem nativeJacobianRow274_eq :
    nativeJacobianRow274 = expectedJacobianRow 274 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow275 : List (Nat × Bounds) := [(186,⟨(-2),(2)⟩),(187,⟨(-2),(2)⟩)]
theorem nativeJacobianRow275_eq :
    nativeJacobianRow275 = expectedJacobianRow 275 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow276 : List (Nat × Bounds) := [(188,⟨(-2),(2)⟩),(189,⟨(-2),(2)⟩)]
theorem nativeJacobianRow276_eq :
    nativeJacobianRow276 = expectedJacobianRow 276 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow277 : List (Nat × Bounds) := [(190,⟨(-2),(2)⟩),(191,⟨(-2),(2)⟩)]
theorem nativeJacobianRow277_eq :
    nativeJacobianRow277 = expectedJacobianRow 277 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow278 : List (Nat × Bounds) := [(192,⟨(-2),(2)⟩),(193,⟨(-2),(2)⟩)]
theorem nativeJacobianRow278_eq :
    nativeJacobianRow278 = expectedJacobianRow 278 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow279 : List (Nat × Bounds) := [(194,⟨(-2),(2)⟩),(195,⟨(-2),(2)⟩)]
theorem nativeJacobianRow279_eq :
    nativeJacobianRow279 = expectedJacobianRow 279 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow280 : List (Nat × Bounds) := [(196,⟨(-2),(2)⟩),(197,⟨(-2),(2)⟩)]
theorem nativeJacobianRow280_eq :
    nativeJacobianRow280 = expectedJacobianRow 280 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow281 : List (Nat × Bounds) := [(198,⟨(-2),(2)⟩),(199,⟨(-2),(2)⟩)]
theorem nativeJacobianRow281_eq :
    nativeJacobianRow281 = expectedJacobianRow 281 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow282 : List (Nat × Bounds) := [(200,⟨(-2),(2)⟩),(201,⟨(-2),(2)⟩)]
theorem nativeJacobianRow282_eq :
    nativeJacobianRow282 = expectedJacobianRow 282 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow283 : List (Nat × Bounds) := [(202,⟨(-2),(2)⟩),(203,⟨(-2),(2)⟩)]
theorem nativeJacobianRow283_eq :
    nativeJacobianRow283 = expectedJacobianRow 283 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow284 : List (Nat × Bounds) := [(204,⟨(-2),(2)⟩),(205,⟨(-2),(2)⟩)]
theorem nativeJacobianRow284_eq :
    nativeJacobianRow284 = expectedJacobianRow 284 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow285 : List (Nat × Bounds) := [(206,⟨(-2),(2)⟩),(207,⟨(-2),(2)⟩)]
theorem nativeJacobianRow285_eq :
    nativeJacobianRow285 = expectedJacobianRow 285 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow286 : List (Nat × Bounds) := [(208,⟨(-2),(2)⟩),(209,⟨(-2),(2)⟩)]
theorem nativeJacobianRow286_eq :
    nativeJacobianRow286 = expectedJacobianRow 286 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow287 : List (Nat × Bounds) := [(210,⟨(-2),(2)⟩),(211,⟨(-2),(2)⟩)]
theorem nativeJacobianRow287_eq :
    nativeJacobianRow287 = expectedJacobianRow 287 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow288 : List (Nat × Bounds) := [(212,⟨(-2),(2)⟩),(213,⟨(-2),(2)⟩)]
theorem nativeJacobianRow288_eq :
    nativeJacobianRow288 = expectedJacobianRow 288 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow289 : List (Nat × Bounds) := [(214,⟨(-2),(2)⟩),(215,⟨(-2),(2)⟩)]
theorem nativeJacobianRow289_eq :
    nativeJacobianRow289 = expectedJacobianRow 289 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow290 : List (Nat × Bounds) := [(216,⟨(-2),(2)⟩),(217,⟨(-2),(2)⟩)]
theorem nativeJacobianRow290_eq :
    nativeJacobianRow290 = expectedJacobianRow 290 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow291 : List (Nat × Bounds) := [(218,⟨(-2),(2)⟩),(219,⟨(-2),(2)⟩)]
theorem nativeJacobianRow291_eq :
    nativeJacobianRow291 = expectedJacobianRow 291 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow292 : List (Nat × Bounds) := [(220,⟨(-2),(2)⟩),(221,⟨(-2),(2)⟩)]
theorem nativeJacobianRow292_eq :
    nativeJacobianRow292 = expectedJacobianRow 292 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow293 : List (Nat × Bounds) := [(222,⟨(-2),(2)⟩),(223,⟨(-2),(2)⟩)]
theorem nativeJacobianRow293_eq :
    nativeJacobianRow293 = expectedJacobianRow 293 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow294 : List (Nat × Bounds) := [(8,⟨(-1),(1)⟩),(9,⟨(-1),(1)⟩),(20,⟨(-1),(1)⟩),(21,⟨(-1),(1)⟩),(32,⟨(-1),(1)⟩),(33,⟨(-1),(1)⟩),(44,⟨(-1),(1)⟩),(45,⟨(-1),(1)⟩),(56,⟨(-1),(1)⟩),(57,⟨(-1),(1)⟩),(68,⟨(-1),(1)⟩),(69,⟨(-1),(1)⟩),(80,⟨(-1),(1)⟩),(81,⟨(-1),(1)⟩),(92,⟨(-1),(1)⟩),(93,⟨(-1),(1)⟩),(104,⟨(-1),(1)⟩),(105,⟨(-1),(1)⟩),(116,⟨(-1),(1)⟩),(117,⟨(-1),(1)⟩),(128,⟨(-1),(1)⟩),(129,⟨(-1),(1)⟩),(140,⟨(-1),(1)⟩),(141,⟨(-1),(1)⟩),(224,⟨(1),(1)⟩)]
theorem nativeJacobianRow294_eq :
    nativeJacobianRow294 = expectedJacobianRow 294 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow295 : List (Nat × Bounds) := [(8,⟨(-1),(1)⟩),(9,⟨(-1),(1)⟩),(20,⟨(-1),(1)⟩),(21,⟨(-1),(1)⟩),(32,⟨(-1),(1)⟩),(33,⟨(-1),(1)⟩),(44,⟨(-1),(1)⟩),(45,⟨(-1),(1)⟩),(56,⟨(-1),(1)⟩),(57,⟨(-1),(1)⟩),(68,⟨(-1),(1)⟩),(69,⟨(-1),(1)⟩),(80,⟨(-1),(1)⟩),(81,⟨(-1),(1)⟩),(92,⟨(-1),(1)⟩),(93,⟨(-1),(1)⟩),(104,⟨(-1),(1)⟩),(105,⟨(-1),(1)⟩),(116,⟨(-1),(1)⟩),(117,⟨(-1),(1)⟩),(128,⟨(-1),(1)⟩),(129,⟨(-1),(1)⟩),(140,⟨(-1),(1)⟩),(141,⟨(-1),(1)⟩),(225,⟨(1),(1)⟩)]
theorem nativeJacobianRow295_eq :
    nativeJacobianRow295 = expectedJacobianRow 295 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow296 : List (Nat × Bounds) := [(8,⟨(-1),(1)⟩),(9,⟨(-1),(1)⟩),(20,⟨(-1),(1)⟩),(21,⟨(-1),(1)⟩),(32,⟨(-1),(1)⟩),(33,⟨(-1),(1)⟩),(44,⟨(-1),(1)⟩),(45,⟨(-1),(1)⟩),(56,⟨(-1),(1)⟩),(57,⟨(-1),(1)⟩),(68,⟨(-1),(1)⟩),(69,⟨(-1),(1)⟩),(82,⟨(-1),(1)⟩),(83,⟨(-1),(1)⟩),(94,⟨(-1),(1)⟩),(95,⟨(-1),(1)⟩),(106,⟨(-1),(1)⟩),(107,⟨(-1),(1)⟩),(118,⟨(-1),(1)⟩),(119,⟨(-1),(1)⟩),(130,⟨(-1),(1)⟩),(131,⟨(-1),(1)⟩),(142,⟨(-1),(1)⟩),(143,⟨(-1),(1)⟩),(226,⟨(1),(1)⟩)]
theorem nativeJacobianRow296_eq :
    nativeJacobianRow296 = expectedJacobianRow 296 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow297 : List (Nat × Bounds) := [(8,⟨(-1),(1)⟩),(9,⟨(-1),(1)⟩),(20,⟨(-1),(1)⟩),(21,⟨(-1),(1)⟩),(32,⟨(-1),(1)⟩),(33,⟨(-1),(1)⟩),(44,⟨(-1),(1)⟩),(45,⟨(-1),(1)⟩),(56,⟨(-1),(1)⟩),(57,⟨(-1),(1)⟩),(68,⟨(-1),(1)⟩),(69,⟨(-1),(1)⟩),(82,⟨(-1),(1)⟩),(83,⟨(-1),(1)⟩),(94,⟨(-1),(1)⟩),(95,⟨(-1),(1)⟩),(106,⟨(-1),(1)⟩),(107,⟨(-1),(1)⟩),(118,⟨(-1),(1)⟩),(119,⟨(-1),(1)⟩),(130,⟨(-1),(1)⟩),(131,⟨(-1),(1)⟩),(142,⟨(-1),(1)⟩),(143,⟨(-1),(1)⟩),(227,⟨(1),(1)⟩)]
theorem nativeJacobianRow297_eq :
    nativeJacobianRow297 = expectedJacobianRow 297 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow298 : List (Nat × Bounds) := [(8,⟨(-1),(1)⟩),(9,⟨(-1),(1)⟩),(20,⟨(-1),(1)⟩),(21,⟨(-1),(1)⟩),(32,⟨(-1),(1)⟩),(33,⟨(-1),(1)⟩),(44,⟨(-1),(1)⟩),(45,⟨(-1),(1)⟩),(56,⟨(-1),(1)⟩),(57,⟨(-1),(1)⟩),(68,⟨(-1),(1)⟩),(69,⟨(-1),(1)⟩),(84,⟨(-1),(1)⟩),(85,⟨(-1),(1)⟩),(96,⟨(-1),(1)⟩),(97,⟨(-1),(1)⟩),(108,⟨(-1),(1)⟩),(109,⟨(-1),(1)⟩),(120,⟨(-1),(1)⟩),(121,⟨(-1),(1)⟩),(132,⟨(-1),(1)⟩),(133,⟨(-1),(1)⟩),(144,⟨(-1),(1)⟩),(145,⟨(-1),(1)⟩),(228,⟨(1),(1)⟩)]
theorem nativeJacobianRow298_eq :
    nativeJacobianRow298 = expectedJacobianRow 298 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow299 : List (Nat × Bounds) := [(8,⟨(-1),(1)⟩),(9,⟨(-1),(1)⟩),(20,⟨(-1),(1)⟩),(21,⟨(-1),(1)⟩),(32,⟨(-1),(1)⟩),(33,⟨(-1),(1)⟩),(44,⟨(-1),(1)⟩),(45,⟨(-1),(1)⟩),(56,⟨(-1),(1)⟩),(57,⟨(-1),(1)⟩),(68,⟨(-1),(1)⟩),(69,⟨(-1),(1)⟩),(84,⟨(-1),(1)⟩),(85,⟨(-1),(1)⟩),(96,⟨(-1),(1)⟩),(97,⟨(-1),(1)⟩),(108,⟨(-1),(1)⟩),(109,⟨(-1),(1)⟩),(120,⟨(-1),(1)⟩),(121,⟨(-1),(1)⟩),(132,⟨(-1),(1)⟩),(133,⟨(-1),(1)⟩),(144,⟨(-1),(1)⟩),(145,⟨(-1),(1)⟩),(229,⟨(1),(1)⟩)]
theorem nativeJacobianRow299_eq :
    nativeJacobianRow299 = expectedJacobianRow 299 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow300 : List (Nat × Bounds) := [(8,⟨(-1),(1)⟩),(9,⟨(-1),(1)⟩),(20,⟨(-1),(1)⟩),(21,⟨(-1),(1)⟩),(32,⟨(-1),(1)⟩),(33,⟨(-1),(1)⟩),(44,⟨(-1),(1)⟩),(45,⟨(-1),(1)⟩),(56,⟨(-1),(1)⟩),(57,⟨(-1),(1)⟩),(68,⟨(-1),(1)⟩),(69,⟨(-1),(1)⟩),(86,⟨(-1),(1)⟩),(87,⟨(-1),(1)⟩),(98,⟨(-1),(1)⟩),(99,⟨(-1),(1)⟩),(110,⟨(-1),(1)⟩),(111,⟨(-1),(1)⟩),(122,⟨(-1),(1)⟩),(123,⟨(-1),(1)⟩),(134,⟨(-1),(1)⟩),(135,⟨(-1),(1)⟩),(146,⟨(-1),(1)⟩),(147,⟨(-1),(1)⟩),(230,⟨(1),(1)⟩)]
theorem nativeJacobianRow300_eq :
    nativeJacobianRow300 = expectedJacobianRow 300 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow301 : List (Nat × Bounds) := [(8,⟨(-1),(1)⟩),(9,⟨(-1),(1)⟩),(20,⟨(-1),(1)⟩),(21,⟨(-1),(1)⟩),(32,⟨(-1),(1)⟩),(33,⟨(-1),(1)⟩),(44,⟨(-1),(1)⟩),(45,⟨(-1),(1)⟩),(56,⟨(-1),(1)⟩),(57,⟨(-1),(1)⟩),(68,⟨(-1),(1)⟩),(69,⟨(-1),(1)⟩),(86,⟨(-1),(1)⟩),(87,⟨(-1),(1)⟩),(98,⟨(-1),(1)⟩),(99,⟨(-1),(1)⟩),(110,⟨(-1),(1)⟩),(111,⟨(-1),(1)⟩),(122,⟨(-1),(1)⟩),(123,⟨(-1),(1)⟩),(134,⟨(-1),(1)⟩),(135,⟨(-1),(1)⟩),(146,⟨(-1),(1)⟩),(147,⟨(-1),(1)⟩),(231,⟨(1),(1)⟩)]
theorem nativeJacobianRow301_eq :
    nativeJacobianRow301 = expectedJacobianRow 301 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow302 : List (Nat × Bounds) := [(8,⟨(-1),(1)⟩),(9,⟨(-1),(1)⟩),(20,⟨(-1),(1)⟩),(21,⟨(-1),(1)⟩),(32,⟨(-1),(1)⟩),(33,⟨(-1),(1)⟩),(44,⟨(-1),(1)⟩),(45,⟨(-1),(1)⟩),(56,⟨(-1),(1)⟩),(57,⟨(-1),(1)⟩),(68,⟨(-1),(1)⟩),(69,⟨(-1),(1)⟩),(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(232,⟨(1),(1)⟩)]
theorem nativeJacobianRow302_eq :
    nativeJacobianRow302 = expectedJacobianRow 302 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow303 : List (Nat × Bounds) := [(8,⟨(-1),(1)⟩),(9,⟨(-1),(1)⟩),(20,⟨(-1),(1)⟩),(21,⟨(-1),(1)⟩),(32,⟨(-1),(1)⟩),(33,⟨(-1),(1)⟩),(44,⟨(-1),(1)⟩),(45,⟨(-1),(1)⟩),(56,⟨(-1),(1)⟩),(57,⟨(-1),(1)⟩),(68,⟨(-1),(1)⟩),(69,⟨(-1),(1)⟩),(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(233,⟨(1),(1)⟩)]
theorem nativeJacobianRow303_eq :
    nativeJacobianRow303 = expectedJacobianRow 303 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow304 : List (Nat × Bounds) := [(8,⟨(-1),(1)⟩),(9,⟨(-1),(1)⟩),(20,⟨(-1),(1)⟩),(21,⟨(-1),(1)⟩),(32,⟨(-1),(1)⟩),(33,⟨(-1),(1)⟩),(44,⟨(-1),(1)⟩),(45,⟨(-1),(1)⟩),(56,⟨(-1),(1)⟩),(57,⟨(-1),(1)⟩),(68,⟨(-1),(1)⟩),(69,⟨(-1),(1)⟩),(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(234,⟨(1),(1)⟩)]
theorem nativeJacobianRow304_eq :
    nativeJacobianRow304 = expectedJacobianRow 304 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow305 : List (Nat × Bounds) := [(8,⟨(-1),(1)⟩),(9,⟨(-1),(1)⟩),(20,⟨(-1),(1)⟩),(21,⟨(-1),(1)⟩),(32,⟨(-1),(1)⟩),(33,⟨(-1),(1)⟩),(44,⟨(-1),(1)⟩),(45,⟨(-1),(1)⟩),(56,⟨(-1),(1)⟩),(57,⟨(-1),(1)⟩),(68,⟨(-1),(1)⟩),(69,⟨(-1),(1)⟩),(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(235,⟨(1),(1)⟩)]
theorem nativeJacobianRow305_eq :
    nativeJacobianRow305 = expectedJacobianRow 305 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow306 : List (Nat × Bounds) := [(10,⟨(-1),(1)⟩),(11,⟨(-1),(1)⟩),(22,⟨(-1),(1)⟩),(23,⟨(-1),(1)⟩),(34,⟨(-1),(1)⟩),(35,⟨(-1),(1)⟩),(46,⟨(-1),(1)⟩),(47,⟨(-1),(1)⟩),(58,⟨(-1),(1)⟩),(59,⟨(-1),(1)⟩),(70,⟨(-1),(1)⟩),(71,⟨(-1),(1)⟩),(80,⟨(-1),(1)⟩),(81,⟨(-1),(1)⟩),(92,⟨(-1),(1)⟩),(93,⟨(-1),(1)⟩),(104,⟨(-1),(1)⟩),(105,⟨(-1),(1)⟩),(116,⟨(-1),(1)⟩),(117,⟨(-1),(1)⟩),(128,⟨(-1),(1)⟩),(129,⟨(-1),(1)⟩),(140,⟨(-1),(1)⟩),(141,⟨(-1),(1)⟩),(236,⟨(1),(1)⟩)]
theorem nativeJacobianRow306_eq :
    nativeJacobianRow306 = expectedJacobianRow 306 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow307 : List (Nat × Bounds) := [(10,⟨(-1),(1)⟩),(11,⟨(-1),(1)⟩),(22,⟨(-1),(1)⟩),(23,⟨(-1),(1)⟩),(34,⟨(-1),(1)⟩),(35,⟨(-1),(1)⟩),(46,⟨(-1),(1)⟩),(47,⟨(-1),(1)⟩),(58,⟨(-1),(1)⟩),(59,⟨(-1),(1)⟩),(70,⟨(-1),(1)⟩),(71,⟨(-1),(1)⟩),(80,⟨(-1),(1)⟩),(81,⟨(-1),(1)⟩),(92,⟨(-1),(1)⟩),(93,⟨(-1),(1)⟩),(104,⟨(-1),(1)⟩),(105,⟨(-1),(1)⟩),(116,⟨(-1),(1)⟩),(117,⟨(-1),(1)⟩),(128,⟨(-1),(1)⟩),(129,⟨(-1),(1)⟩),(140,⟨(-1),(1)⟩),(141,⟨(-1),(1)⟩),(237,⟨(1),(1)⟩)]
theorem nativeJacobianRow307_eq :
    nativeJacobianRow307 = expectedJacobianRow 307 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow308 : List (Nat × Bounds) := [(10,⟨(-1),(1)⟩),(11,⟨(-1),(1)⟩),(22,⟨(-1),(1)⟩),(23,⟨(-1),(1)⟩),(34,⟨(-1),(1)⟩),(35,⟨(-1),(1)⟩),(46,⟨(-1),(1)⟩),(47,⟨(-1),(1)⟩),(58,⟨(-1),(1)⟩),(59,⟨(-1),(1)⟩),(70,⟨(-1),(1)⟩),(71,⟨(-1),(1)⟩),(82,⟨(-1),(1)⟩),(83,⟨(-1),(1)⟩),(94,⟨(-1),(1)⟩),(95,⟨(-1),(1)⟩),(106,⟨(-1),(1)⟩),(107,⟨(-1),(1)⟩),(118,⟨(-1),(1)⟩),(119,⟨(-1),(1)⟩),(130,⟨(-1),(1)⟩),(131,⟨(-1),(1)⟩),(142,⟨(-1),(1)⟩),(143,⟨(-1),(1)⟩),(238,⟨(1),(1)⟩)]
theorem nativeJacobianRow308_eq :
    nativeJacobianRow308 = expectedJacobianRow 308 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow309 : List (Nat × Bounds) := [(10,⟨(-1),(1)⟩),(11,⟨(-1),(1)⟩),(22,⟨(-1),(1)⟩),(23,⟨(-1),(1)⟩),(34,⟨(-1),(1)⟩),(35,⟨(-1),(1)⟩),(46,⟨(-1),(1)⟩),(47,⟨(-1),(1)⟩),(58,⟨(-1),(1)⟩),(59,⟨(-1),(1)⟩),(70,⟨(-1),(1)⟩),(71,⟨(-1),(1)⟩),(82,⟨(-1),(1)⟩),(83,⟨(-1),(1)⟩),(94,⟨(-1),(1)⟩),(95,⟨(-1),(1)⟩),(106,⟨(-1),(1)⟩),(107,⟨(-1),(1)⟩),(118,⟨(-1),(1)⟩),(119,⟨(-1),(1)⟩),(130,⟨(-1),(1)⟩),(131,⟨(-1),(1)⟩),(142,⟨(-1),(1)⟩),(143,⟨(-1),(1)⟩),(239,⟨(1),(1)⟩)]
theorem nativeJacobianRow309_eq :
    nativeJacobianRow309 = expectedJacobianRow 309 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow310 : List (Nat × Bounds) := [(10,⟨(-1),(1)⟩),(11,⟨(-1),(1)⟩),(22,⟨(-1),(1)⟩),(23,⟨(-1),(1)⟩),(34,⟨(-1),(1)⟩),(35,⟨(-1),(1)⟩),(46,⟨(-1),(1)⟩),(47,⟨(-1),(1)⟩),(58,⟨(-1),(1)⟩),(59,⟨(-1),(1)⟩),(70,⟨(-1),(1)⟩),(71,⟨(-1),(1)⟩),(84,⟨(-1),(1)⟩),(85,⟨(-1),(1)⟩),(96,⟨(-1),(1)⟩),(97,⟨(-1),(1)⟩),(108,⟨(-1),(1)⟩),(109,⟨(-1),(1)⟩),(120,⟨(-1),(1)⟩),(121,⟨(-1),(1)⟩),(132,⟨(-1),(1)⟩),(133,⟨(-1),(1)⟩),(144,⟨(-1),(1)⟩),(145,⟨(-1),(1)⟩),(240,⟨(1),(1)⟩)]
theorem nativeJacobianRow310_eq :
    nativeJacobianRow310 = expectedJacobianRow 310 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow311 : List (Nat × Bounds) := [(10,⟨(-1),(1)⟩),(11,⟨(-1),(1)⟩),(22,⟨(-1),(1)⟩),(23,⟨(-1),(1)⟩),(34,⟨(-1),(1)⟩),(35,⟨(-1),(1)⟩),(46,⟨(-1),(1)⟩),(47,⟨(-1),(1)⟩),(58,⟨(-1),(1)⟩),(59,⟨(-1),(1)⟩),(70,⟨(-1),(1)⟩),(71,⟨(-1),(1)⟩),(84,⟨(-1),(1)⟩),(85,⟨(-1),(1)⟩),(96,⟨(-1),(1)⟩),(97,⟨(-1),(1)⟩),(108,⟨(-1),(1)⟩),(109,⟨(-1),(1)⟩),(120,⟨(-1),(1)⟩),(121,⟨(-1),(1)⟩),(132,⟨(-1),(1)⟩),(133,⟨(-1),(1)⟩),(144,⟨(-1),(1)⟩),(145,⟨(-1),(1)⟩),(241,⟨(1),(1)⟩)]
theorem nativeJacobianRow311_eq :
    nativeJacobianRow311 = expectedJacobianRow 311 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow312 : List (Nat × Bounds) := [(10,⟨(-1),(1)⟩),(11,⟨(-1),(1)⟩),(22,⟨(-1),(1)⟩),(23,⟨(-1),(1)⟩),(34,⟨(-1),(1)⟩),(35,⟨(-1),(1)⟩),(46,⟨(-1),(1)⟩),(47,⟨(-1),(1)⟩),(58,⟨(-1),(1)⟩),(59,⟨(-1),(1)⟩),(70,⟨(-1),(1)⟩),(71,⟨(-1),(1)⟩),(86,⟨(-1),(1)⟩),(87,⟨(-1),(1)⟩),(98,⟨(-1),(1)⟩),(99,⟨(-1),(1)⟩),(110,⟨(-1),(1)⟩),(111,⟨(-1),(1)⟩),(122,⟨(-1),(1)⟩),(123,⟨(-1),(1)⟩),(134,⟨(-1),(1)⟩),(135,⟨(-1),(1)⟩),(146,⟨(-1),(1)⟩),(147,⟨(-1),(1)⟩),(242,⟨(1),(1)⟩)]
theorem nativeJacobianRow312_eq :
    nativeJacobianRow312 = expectedJacobianRow 312 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow313 : List (Nat × Bounds) := [(10,⟨(-1),(1)⟩),(11,⟨(-1),(1)⟩),(22,⟨(-1),(1)⟩),(23,⟨(-1),(1)⟩),(34,⟨(-1),(1)⟩),(35,⟨(-1),(1)⟩),(46,⟨(-1),(1)⟩),(47,⟨(-1),(1)⟩),(58,⟨(-1),(1)⟩),(59,⟨(-1),(1)⟩),(70,⟨(-1),(1)⟩),(71,⟨(-1),(1)⟩),(86,⟨(-1),(1)⟩),(87,⟨(-1),(1)⟩),(98,⟨(-1),(1)⟩),(99,⟨(-1),(1)⟩),(110,⟨(-1),(1)⟩),(111,⟨(-1),(1)⟩),(122,⟨(-1),(1)⟩),(123,⟨(-1),(1)⟩),(134,⟨(-1),(1)⟩),(135,⟨(-1),(1)⟩),(146,⟨(-1),(1)⟩),(147,⟨(-1),(1)⟩),(243,⟨(1),(1)⟩)]
theorem nativeJacobianRow313_eq :
    nativeJacobianRow313 = expectedJacobianRow 313 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow314 : List (Nat × Bounds) := [(10,⟨(-1),(1)⟩),(11,⟨(-1),(1)⟩),(22,⟨(-1),(1)⟩),(23,⟨(-1),(1)⟩),(34,⟨(-1),(1)⟩),(35,⟨(-1),(1)⟩),(46,⟨(-1),(1)⟩),(47,⟨(-1),(1)⟩),(58,⟨(-1),(1)⟩),(59,⟨(-1),(1)⟩),(70,⟨(-1),(1)⟩),(71,⟨(-1),(1)⟩),(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(244,⟨(1),(1)⟩)]
theorem nativeJacobianRow314_eq :
    nativeJacobianRow314 = expectedJacobianRow 314 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow315 : List (Nat × Bounds) := [(10,⟨(-1),(1)⟩),(11,⟨(-1),(1)⟩),(22,⟨(-1),(1)⟩),(23,⟨(-1),(1)⟩),(34,⟨(-1),(1)⟩),(35,⟨(-1),(1)⟩),(46,⟨(-1),(1)⟩),(47,⟨(-1),(1)⟩),(58,⟨(-1),(1)⟩),(59,⟨(-1),(1)⟩),(70,⟨(-1),(1)⟩),(71,⟨(-1),(1)⟩),(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(245,⟨(1),(1)⟩)]
theorem nativeJacobianRow315_eq :
    nativeJacobianRow315 = expectedJacobianRow 315 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow316 : List (Nat × Bounds) := [(10,⟨(-1),(1)⟩),(11,⟨(-1),(1)⟩),(22,⟨(-1),(1)⟩),(23,⟨(-1),(1)⟩),(34,⟨(-1),(1)⟩),(35,⟨(-1),(1)⟩),(46,⟨(-1),(1)⟩),(47,⟨(-1),(1)⟩),(58,⟨(-1),(1)⟩),(59,⟨(-1),(1)⟩),(70,⟨(-1),(1)⟩),(71,⟨(-1),(1)⟩),(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(246,⟨(1),(1)⟩)]
theorem nativeJacobianRow316_eq :
    nativeJacobianRow316 = expectedJacobianRow 316 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow317 : List (Nat × Bounds) := [(10,⟨(-1),(1)⟩),(11,⟨(-1),(1)⟩),(22,⟨(-1),(1)⟩),(23,⟨(-1),(1)⟩),(34,⟨(-1),(1)⟩),(35,⟨(-1),(1)⟩),(46,⟨(-1),(1)⟩),(47,⟨(-1),(1)⟩),(58,⟨(-1),(1)⟩),(59,⟨(-1),(1)⟩),(70,⟨(-1),(1)⟩),(71,⟨(-1),(1)⟩),(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(247,⟨(1),(1)⟩)]
theorem nativeJacobianRow317_eq :
    nativeJacobianRow317 = expectedJacobianRow 317 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow318 : List (Nat × Bounds) := [(12,⟨(-1),(1)⟩),(13,⟨(-1),(1)⟩),(24,⟨(-1),(1)⟩),(25,⟨(-1),(1)⟩),(36,⟨(-1),(1)⟩),(37,⟨(-1),(1)⟩),(48,⟨(-1),(1)⟩),(49,⟨(-1),(1)⟩),(60,⟨(-1),(1)⟩),(61,⟨(-1),(1)⟩),(72,⟨(-1),(1)⟩),(73,⟨(-1),(1)⟩),(80,⟨(-1),(1)⟩),(81,⟨(-1),(1)⟩),(92,⟨(-1),(1)⟩),(93,⟨(-1),(1)⟩),(104,⟨(-1),(1)⟩),(105,⟨(-1),(1)⟩),(116,⟨(-1),(1)⟩),(117,⟨(-1),(1)⟩),(128,⟨(-1),(1)⟩),(129,⟨(-1),(1)⟩),(140,⟨(-1),(1)⟩),(141,⟨(-1),(1)⟩),(248,⟨(1),(1)⟩)]
theorem nativeJacobianRow318_eq :
    nativeJacobianRow318 = expectedJacobianRow 318 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow319 : List (Nat × Bounds) := [(12,⟨(-1),(1)⟩),(13,⟨(-1),(1)⟩),(24,⟨(-1),(1)⟩),(25,⟨(-1),(1)⟩),(36,⟨(-1),(1)⟩),(37,⟨(-1),(1)⟩),(48,⟨(-1),(1)⟩),(49,⟨(-1),(1)⟩),(60,⟨(-1),(1)⟩),(61,⟨(-1),(1)⟩),(72,⟨(-1),(1)⟩),(73,⟨(-1),(1)⟩),(80,⟨(-1),(1)⟩),(81,⟨(-1),(1)⟩),(92,⟨(-1),(1)⟩),(93,⟨(-1),(1)⟩),(104,⟨(-1),(1)⟩),(105,⟨(-1),(1)⟩),(116,⟨(-1),(1)⟩),(117,⟨(-1),(1)⟩),(128,⟨(-1),(1)⟩),(129,⟨(-1),(1)⟩),(140,⟨(-1),(1)⟩),(141,⟨(-1),(1)⟩),(249,⟨(1),(1)⟩)]
theorem nativeJacobianRow319_eq :
    nativeJacobianRow319 = expectedJacobianRow 319 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

end MUB.SzollosiRectangularReflection

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

def nativeJacobianRow480 : List (Nat × Bounds) := [(86,⟨(-1),(1)⟩),(87,⟨(-1),(1)⟩),(98,⟨(-1),(1)⟩),(99,⟨(-1),(1)⟩),(110,⟨(-1),(1)⟩),(111,⟨(-1),(1)⟩),(122,⟨(-1),(1)⟩),(123,⟨(-1),(1)⟩),(134,⟨(-1),(1)⟩),(135,⟨(-1),(1)⟩),(146,⟨(-1),(1)⟩),(147,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(410,⟨(1),(1)⟩)]
theorem nativeJacobianRow480_eq :
    nativeJacobianRow480 = expectedJacobianRow 480 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow481 : List (Nat × Bounds) := [(86,⟨(-1),(1)⟩),(87,⟨(-1),(1)⟩),(98,⟨(-1),(1)⟩),(99,⟨(-1),(1)⟩),(110,⟨(-1),(1)⟩),(111,⟨(-1),(1)⟩),(122,⟨(-1),(1)⟩),(123,⟨(-1),(1)⟩),(134,⟨(-1),(1)⟩),(135,⟨(-1),(1)⟩),(146,⟨(-1),(1)⟩),(147,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(411,⟨(1),(1)⟩)]
theorem nativeJacobianRow481_eq :
    nativeJacobianRow481 = expectedJacobianRow 481 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow482 : List (Nat × Bounds) := [(86,⟨(-1),(1)⟩),(87,⟨(-1),(1)⟩),(98,⟨(-1),(1)⟩),(99,⟨(-1),(1)⟩),(110,⟨(-1),(1)⟩),(111,⟨(-1),(1)⟩),(122,⟨(-1),(1)⟩),(123,⟨(-1),(1)⟩),(134,⟨(-1),(1)⟩),(135,⟨(-1),(1)⟩),(146,⟨(-1),(1)⟩),(147,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩),(412,⟨(1),(1)⟩)]
theorem nativeJacobianRow482_eq :
    nativeJacobianRow482 = expectedJacobianRow 482 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow483 : List (Nat × Bounds) := [(86,⟨(-1),(1)⟩),(87,⟨(-1),(1)⟩),(98,⟨(-1),(1)⟩),(99,⟨(-1),(1)⟩),(110,⟨(-1),(1)⟩),(111,⟨(-1),(1)⟩),(122,⟨(-1),(1)⟩),(123,⟨(-1),(1)⟩),(134,⟨(-1),(1)⟩),(135,⟨(-1),(1)⟩),(146,⟨(-1),(1)⟩),(147,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩),(413,⟨(1),(1)⟩)]
theorem nativeJacobianRow483_eq :
    nativeJacobianRow483 = expectedJacobianRow 483 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow484 : List (Nat × Bounds) := [(86,⟨(-1),(1)⟩),(87,⟨(-1),(1)⟩),(98,⟨(-1),(1)⟩),(99,⟨(-1),(1)⟩),(110,⟨(-1),(1)⟩),(111,⟨(-1),(1)⟩),(122,⟨(-1),(1)⟩),(123,⟨(-1),(1)⟩),(134,⟨(-1),(1)⟩),(135,⟨(-1),(1)⟩),(146,⟨(-1),(1)⟩),(147,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩),(414,⟨(1),(1)⟩)]
theorem nativeJacobianRow484_eq :
    nativeJacobianRow484 = expectedJacobianRow 484 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow485 : List (Nat × Bounds) := [(86,⟨(-1),(1)⟩),(87,⟨(-1),(1)⟩),(98,⟨(-1),(1)⟩),(99,⟨(-1),(1)⟩),(110,⟨(-1),(1)⟩),(111,⟨(-1),(1)⟩),(122,⟨(-1),(1)⟩),(123,⟨(-1),(1)⟩),(134,⟨(-1),(1)⟩),(135,⟨(-1),(1)⟩),(146,⟨(-1),(1)⟩),(147,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩),(415,⟨(1),(1)⟩)]
theorem nativeJacobianRow485_eq :
    nativeJacobianRow485 = expectedJacobianRow 485 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow486 : List (Nat × Bounds) := [(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(416,⟨(1),(1)⟩)]
theorem nativeJacobianRow486_eq :
    nativeJacobianRow486 = expectedJacobianRow 486 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow487 : List (Nat × Bounds) := [(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(417,⟨(1),(1)⟩)]
theorem nativeJacobianRow487_eq :
    nativeJacobianRow487 = expectedJacobianRow 487 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow488 : List (Nat × Bounds) := [(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(418,⟨(1),(1)⟩)]
theorem nativeJacobianRow488_eq :
    nativeJacobianRow488 = expectedJacobianRow 488 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow489 : List (Nat × Bounds) := [(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(419,⟨(1),(1)⟩)]
theorem nativeJacobianRow489_eq :
    nativeJacobianRow489 = expectedJacobianRow 489 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow490 : List (Nat × Bounds) := [(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(420,⟨(1),(1)⟩)]
theorem nativeJacobianRow490_eq :
    nativeJacobianRow490 = expectedJacobianRow 490 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow491 : List (Nat × Bounds) := [(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(421,⟨(1),(1)⟩)]
theorem nativeJacobianRow491_eq :
    nativeJacobianRow491 = expectedJacobianRow 491 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow492 : List (Nat × Bounds) := [(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(422,⟨(1),(1)⟩)]
theorem nativeJacobianRow492_eq :
    nativeJacobianRow492 = expectedJacobianRow 492 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow493 : List (Nat × Bounds) := [(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(423,⟨(1),(1)⟩)]
theorem nativeJacobianRow493_eq :
    nativeJacobianRow493 = expectedJacobianRow 493 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow494 : List (Nat × Bounds) := [(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩),(424,⟨(1),(1)⟩)]
theorem nativeJacobianRow494_eq :
    nativeJacobianRow494 = expectedJacobianRow 494 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow495 : List (Nat × Bounds) := [(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩),(425,⟨(1),(1)⟩)]
theorem nativeJacobianRow495_eq :
    nativeJacobianRow495 = expectedJacobianRow 495 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow496 : List (Nat × Bounds) := [(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩),(426,⟨(1),(1)⟩)]
theorem nativeJacobianRow496_eq :
    nativeJacobianRow496 = expectedJacobianRow 496 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow497 : List (Nat × Bounds) := [(88,⟨(-1),(1)⟩),(89,⟨(-1),(1)⟩),(100,⟨(-1),(1)⟩),(101,⟨(-1),(1)⟩),(112,⟨(-1),(1)⟩),(113,⟨(-1),(1)⟩),(124,⟨(-1),(1)⟩),(125,⟨(-1),(1)⟩),(136,⟨(-1),(1)⟩),(137,⟨(-1),(1)⟩),(148,⟨(-1),(1)⟩),(149,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩),(427,⟨(1),(1)⟩)]
theorem nativeJacobianRow497_eq :
    nativeJacobianRow497 = expectedJacobianRow 497 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow498 : List (Nat × Bounds) := [(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(428,⟨(1),(1)⟩)]
theorem nativeJacobianRow498_eq :
    nativeJacobianRow498 = expectedJacobianRow 498 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow499 : List (Nat × Bounds) := [(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(429,⟨(1),(1)⟩)]
theorem nativeJacobianRow499_eq :
    nativeJacobianRow499 = expectedJacobianRow 499 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow500 : List (Nat × Bounds) := [(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(430,⟨(1),(1)⟩)]
theorem nativeJacobianRow500_eq :
    nativeJacobianRow500 = expectedJacobianRow 500 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow501 : List (Nat × Bounds) := [(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(431,⟨(1),(1)⟩)]
theorem nativeJacobianRow501_eq :
    nativeJacobianRow501 = expectedJacobianRow 501 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow502 : List (Nat × Bounds) := [(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(432,⟨(1),(1)⟩)]
theorem nativeJacobianRow502_eq :
    nativeJacobianRow502 = expectedJacobianRow 502 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow503 : List (Nat × Bounds) := [(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(433,⟨(1),(1)⟩)]
theorem nativeJacobianRow503_eq :
    nativeJacobianRow503 = expectedJacobianRow 503 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow504 : List (Nat × Bounds) := [(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(434,⟨(1),(1)⟩)]
theorem nativeJacobianRow504_eq :
    nativeJacobianRow504 = expectedJacobianRow 504 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow505 : List (Nat × Bounds) := [(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(435,⟨(1),(1)⟩)]
theorem nativeJacobianRow505_eq :
    nativeJacobianRow505 = expectedJacobianRow 505 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow506 : List (Nat × Bounds) := [(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩),(436,⟨(1),(1)⟩)]
theorem nativeJacobianRow506_eq :
    nativeJacobianRow506 = expectedJacobianRow 506 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow507 : List (Nat × Bounds) := [(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩),(437,⟨(1),(1)⟩)]
theorem nativeJacobianRow507_eq :
    nativeJacobianRow507 = expectedJacobianRow 507 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow508 : List (Nat × Bounds) := [(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩),(438,⟨(1),(1)⟩)]
theorem nativeJacobianRow508_eq :
    nativeJacobianRow508 = expectedJacobianRow 508 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow509 : List (Nat × Bounds) := [(90,⟨(-1),(1)⟩),(91,⟨(-1),(1)⟩),(102,⟨(-1),(1)⟩),(103,⟨(-1),(1)⟩),(114,⟨(-1),(1)⟩),(115,⟨(-1),(1)⟩),(126,⟨(-1),(1)⟩),(127,⟨(-1),(1)⟩),(138,⟨(-1),(1)⟩),(139,⟨(-1),(1)⟩),(150,⟨(-1),(1)⟩),(151,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩),(439,⟨(1),(1)⟩)]
theorem nativeJacobianRow509_eq :
    nativeJacobianRow509 = expectedJacobianRow 509 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow510 : List (Nat × Bounds) := [(224,⟨(-6),(6)⟩),(225,⟨(-6),(6)⟩)]
theorem nativeJacobianRow510_eq :
    nativeJacobianRow510 = expectedJacobianRow 510 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow511 : List (Nat × Bounds) := [(226,⟨(-6),(6)⟩),(227,⟨(-6),(6)⟩)]
theorem nativeJacobianRow511_eq :
    nativeJacobianRow511 = expectedJacobianRow 511 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow512 : List (Nat × Bounds) := [(228,⟨(-6),(6)⟩),(229,⟨(-6),(6)⟩)]
theorem nativeJacobianRow512_eq :
    nativeJacobianRow512 = expectedJacobianRow 512 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow513 : List (Nat × Bounds) := [(230,⟨(-6),(6)⟩),(231,⟨(-6),(6)⟩)]
theorem nativeJacobianRow513_eq :
    nativeJacobianRow513 = expectedJacobianRow 513 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow514 : List (Nat × Bounds) := [(232,⟨(-6),(6)⟩),(233,⟨(-6),(6)⟩)]
theorem nativeJacobianRow514_eq :
    nativeJacobianRow514 = expectedJacobianRow 514 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow515 : List (Nat × Bounds) := [(234,⟨(-6),(6)⟩),(235,⟨(-6),(6)⟩)]
theorem nativeJacobianRow515_eq :
    nativeJacobianRow515 = expectedJacobianRow 515 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow516 : List (Nat × Bounds) := [(236,⟨(-6),(6)⟩),(237,⟨(-6),(6)⟩)]
theorem nativeJacobianRow516_eq :
    nativeJacobianRow516 = expectedJacobianRow 516 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow517 : List (Nat × Bounds) := [(238,⟨(-6),(6)⟩),(239,⟨(-6),(6)⟩)]
theorem nativeJacobianRow517_eq :
    nativeJacobianRow517 = expectedJacobianRow 517 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow518 : List (Nat × Bounds) := [(240,⟨(-6),(6)⟩),(241,⟨(-6),(6)⟩)]
theorem nativeJacobianRow518_eq :
    nativeJacobianRow518 = expectedJacobianRow 518 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow519 : List (Nat × Bounds) := [(242,⟨(-6),(6)⟩),(243,⟨(-6),(6)⟩)]
theorem nativeJacobianRow519_eq :
    nativeJacobianRow519 = expectedJacobianRow 519 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow520 : List (Nat × Bounds) := [(244,⟨(-6),(6)⟩),(245,⟨(-6),(6)⟩)]
theorem nativeJacobianRow520_eq :
    nativeJacobianRow520 = expectedJacobianRow 520 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow521 : List (Nat × Bounds) := [(246,⟨(-6),(6)⟩),(247,⟨(-6),(6)⟩)]
theorem nativeJacobianRow521_eq :
    nativeJacobianRow521 = expectedJacobianRow 521 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow522 : List (Nat × Bounds) := [(248,⟨(-6),(6)⟩),(249,⟨(-6),(6)⟩)]
theorem nativeJacobianRow522_eq :
    nativeJacobianRow522 = expectedJacobianRow 522 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow523 : List (Nat × Bounds) := [(250,⟨(-6),(6)⟩),(251,⟨(-6),(6)⟩)]
theorem nativeJacobianRow523_eq :
    nativeJacobianRow523 = expectedJacobianRow 523 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow524 : List (Nat × Bounds) := [(252,⟨(-6),(6)⟩),(253,⟨(-6),(6)⟩)]
theorem nativeJacobianRow524_eq :
    nativeJacobianRow524 = expectedJacobianRow 524 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow525 : List (Nat × Bounds) := [(254,⟨(-6),(6)⟩),(255,⟨(-6),(6)⟩)]
theorem nativeJacobianRow525_eq :
    nativeJacobianRow525 = expectedJacobianRow 525 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow526 : List (Nat × Bounds) := [(256,⟨(-6),(6)⟩),(257,⟨(-6),(6)⟩)]
theorem nativeJacobianRow526_eq :
    nativeJacobianRow526 = expectedJacobianRow 526 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow527 : List (Nat × Bounds) := [(258,⟨(-6),(6)⟩),(259,⟨(-6),(6)⟩)]
theorem nativeJacobianRow527_eq :
    nativeJacobianRow527 = expectedJacobianRow 527 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow528 : List (Nat × Bounds) := [(260,⟨(-6),(6)⟩),(261,⟨(-6),(6)⟩)]
theorem nativeJacobianRow528_eq :
    nativeJacobianRow528 = expectedJacobianRow 528 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow529 : List (Nat × Bounds) := [(262,⟨(-6),(6)⟩),(263,⟨(-6),(6)⟩)]
theorem nativeJacobianRow529_eq :
    nativeJacobianRow529 = expectedJacobianRow 529 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow530 : List (Nat × Bounds) := [(264,⟨(-6),(6)⟩),(265,⟨(-6),(6)⟩)]
theorem nativeJacobianRow530_eq :
    nativeJacobianRow530 = expectedJacobianRow 530 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow531 : List (Nat × Bounds) := [(266,⟨(-6),(6)⟩),(267,⟨(-6),(6)⟩)]
theorem nativeJacobianRow531_eq :
    nativeJacobianRow531 = expectedJacobianRow 531 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow532 : List (Nat × Bounds) := [(268,⟨(-6),(6)⟩),(269,⟨(-6),(6)⟩)]
theorem nativeJacobianRow532_eq :
    nativeJacobianRow532 = expectedJacobianRow 532 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow533 : List (Nat × Bounds) := [(270,⟨(-6),(6)⟩),(271,⟨(-6),(6)⟩)]
theorem nativeJacobianRow533_eq :
    nativeJacobianRow533 = expectedJacobianRow 533 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow534 : List (Nat × Bounds) := [(272,⟨(-6),(6)⟩),(273,⟨(-6),(6)⟩)]
theorem nativeJacobianRow534_eq :
    nativeJacobianRow534 = expectedJacobianRow 534 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow535 : List (Nat × Bounds) := [(274,⟨(-6),(6)⟩),(275,⟨(-6),(6)⟩)]
theorem nativeJacobianRow535_eq :
    nativeJacobianRow535 = expectedJacobianRow 535 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow536 : List (Nat × Bounds) := [(276,⟨(-6),(6)⟩),(277,⟨(-6),(6)⟩)]
theorem nativeJacobianRow536_eq :
    nativeJacobianRow536 = expectedJacobianRow 536 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow537 : List (Nat × Bounds) := [(278,⟨(-6),(6)⟩),(279,⟨(-6),(6)⟩)]
theorem nativeJacobianRow537_eq :
    nativeJacobianRow537 = expectedJacobianRow 537 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow538 : List (Nat × Bounds) := [(280,⟨(-6),(6)⟩),(281,⟨(-6),(6)⟩)]
theorem nativeJacobianRow538_eq :
    nativeJacobianRow538 = expectedJacobianRow 538 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow539 : List (Nat × Bounds) := [(282,⟨(-6),(6)⟩),(283,⟨(-6),(6)⟩)]
theorem nativeJacobianRow539_eq :
    nativeJacobianRow539 = expectedJacobianRow 539 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow540 : List (Nat × Bounds) := [(284,⟨(-6),(6)⟩),(285,⟨(-6),(6)⟩)]
theorem nativeJacobianRow540_eq :
    nativeJacobianRow540 = expectedJacobianRow 540 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow541 : List (Nat × Bounds) := [(286,⟨(-6),(6)⟩),(287,⟨(-6),(6)⟩)]
theorem nativeJacobianRow541_eq :
    nativeJacobianRow541 = expectedJacobianRow 541 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow542 : List (Nat × Bounds) := [(288,⟨(-6),(6)⟩),(289,⟨(-6),(6)⟩)]
theorem nativeJacobianRow542_eq :
    nativeJacobianRow542 = expectedJacobianRow 542 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow543 : List (Nat × Bounds) := [(290,⟨(-6),(6)⟩),(291,⟨(-6),(6)⟩)]
theorem nativeJacobianRow543_eq :
    nativeJacobianRow543 = expectedJacobianRow 543 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow544 : List (Nat × Bounds) := [(292,⟨(-6),(6)⟩),(293,⟨(-6),(6)⟩)]
theorem nativeJacobianRow544_eq :
    nativeJacobianRow544 = expectedJacobianRow 544 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow545 : List (Nat × Bounds) := [(294,⟨(-6),(6)⟩),(295,⟨(-6),(6)⟩)]
theorem nativeJacobianRow545_eq :
    nativeJacobianRow545 = expectedJacobianRow 545 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow546 : List (Nat × Bounds) := [(296,⟨(-6),(6)⟩),(297,⟨(-6),(6)⟩)]
theorem nativeJacobianRow546_eq :
    nativeJacobianRow546 = expectedJacobianRow 546 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow547 : List (Nat × Bounds) := [(298,⟨(-6),(6)⟩),(299,⟨(-6),(6)⟩)]
theorem nativeJacobianRow547_eq :
    nativeJacobianRow547 = expectedJacobianRow 547 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow548 : List (Nat × Bounds) := [(300,⟨(-6),(6)⟩),(301,⟨(-6),(6)⟩)]
theorem nativeJacobianRow548_eq :
    nativeJacobianRow548 = expectedJacobianRow 548 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow549 : List (Nat × Bounds) := [(302,⟨(-6),(6)⟩),(303,⟨(-6),(6)⟩)]
theorem nativeJacobianRow549_eq :
    nativeJacobianRow549 = expectedJacobianRow 549 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow550 : List (Nat × Bounds) := [(304,⟨(-6),(6)⟩),(305,⟨(-6),(6)⟩)]
theorem nativeJacobianRow550_eq :
    nativeJacobianRow550 = expectedJacobianRow 550 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow551 : List (Nat × Bounds) := [(306,⟨(-6),(6)⟩),(307,⟨(-6),(6)⟩)]
theorem nativeJacobianRow551_eq :
    nativeJacobianRow551 = expectedJacobianRow 551 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow552 : List (Nat × Bounds) := [(308,⟨(-6),(6)⟩),(309,⟨(-6),(6)⟩)]
theorem nativeJacobianRow552_eq :
    nativeJacobianRow552 = expectedJacobianRow 552 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow553 : List (Nat × Bounds) := [(310,⟨(-6),(6)⟩),(311,⟨(-6),(6)⟩)]
theorem nativeJacobianRow553_eq :
    nativeJacobianRow553 = expectedJacobianRow 553 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow554 : List (Nat × Bounds) := [(312,⟨(-6),(6)⟩),(313,⟨(-6),(6)⟩)]
theorem nativeJacobianRow554_eq :
    nativeJacobianRow554 = expectedJacobianRow 554 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow555 : List (Nat × Bounds) := [(314,⟨(-6),(6)⟩),(315,⟨(-6),(6)⟩)]
theorem nativeJacobianRow555_eq :
    nativeJacobianRow555 = expectedJacobianRow 555 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow556 : List (Nat × Bounds) := [(316,⟨(-6),(6)⟩),(317,⟨(-6),(6)⟩)]
theorem nativeJacobianRow556_eq :
    nativeJacobianRow556 = expectedJacobianRow 556 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow557 : List (Nat × Bounds) := [(318,⟨(-6),(6)⟩),(319,⟨(-6),(6)⟩)]
theorem nativeJacobianRow557_eq :
    nativeJacobianRow557 = expectedJacobianRow 557 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow558 : List (Nat × Bounds) := [(320,⟨(-6),(6)⟩),(321,⟨(-6),(6)⟩)]
theorem nativeJacobianRow558_eq :
    nativeJacobianRow558 = expectedJacobianRow 558 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow559 : List (Nat × Bounds) := [(322,⟨(-6),(6)⟩),(323,⟨(-6),(6)⟩)]
theorem nativeJacobianRow559_eq :
    nativeJacobianRow559 = expectedJacobianRow 559 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

end MUB.SzollosiRectangularReflection

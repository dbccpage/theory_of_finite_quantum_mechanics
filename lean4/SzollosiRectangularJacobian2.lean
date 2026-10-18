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

def nativeJacobianRow160 : List (Nat × Bounds) := [(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow160_eq :
    nativeJacobianRow160 = expectedJacobianRow 160 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow161 : List (Nat × Bounds) := [(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow161_eq :
    nativeJacobianRow161 = expectedJacobianRow 161 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow162 : List (Nat × Bounds) := [(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩)]
theorem nativeJacobianRow162_eq :
    nativeJacobianRow162 = expectedJacobianRow 162 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow163 : List (Nat × Bounds) := [(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩)]
theorem nativeJacobianRow163_eq :
    nativeJacobianRow163 = expectedJacobianRow 163 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow164 : List (Nat × Bounds) := [(154,⟨(-2),(2)⟩),(155,⟨(-2),(2)⟩),(166,⟨(-2),(2)⟩),(167,⟨(-2),(2)⟩),(178,⟨(-2),(2)⟩),(179,⟨(-2),(2)⟩),(190,⟨(-2),(2)⟩),(191,⟨(-2),(2)⟩),(202,⟨(-2),(2)⟩),(203,⟨(-2),(2)⟩),(214,⟨(-2),(2)⟩),(215,⟨(-2),(2)⟩)]
theorem nativeJacobianRow164_eq :
    nativeJacobianRow164 = expectedJacobianRow 164 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow165 : List (Nat × Bounds) := []
theorem nativeJacobianRow165_eq :
    nativeJacobianRow165 = expectedJacobianRow 165 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow166 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩)]
theorem nativeJacobianRow166_eq :
    nativeJacobianRow166 = expectedJacobianRow 166 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow167 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩)]
theorem nativeJacobianRow167_eq :
    nativeJacobianRow167 = expectedJacobianRow 167 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow168 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩)]
theorem nativeJacobianRow168_eq :
    nativeJacobianRow168 = expectedJacobianRow 168 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow169 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩)]
theorem nativeJacobianRow169_eq :
    nativeJacobianRow169 = expectedJacobianRow 169 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow170 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow170_eq :
    nativeJacobianRow170 = expectedJacobianRow 170 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow171 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow171_eq :
    nativeJacobianRow171 = expectedJacobianRow 171 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow172 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow172_eq :
    nativeJacobianRow172 = expectedJacobianRow 172 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow173 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow173_eq :
    nativeJacobianRow173 = expectedJacobianRow 173 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow174 : List (Nat × Bounds) := [(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩)]
theorem nativeJacobianRow174_eq :
    nativeJacobianRow174 = expectedJacobianRow 174 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow175 : List (Nat × Bounds) := [(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩)]
theorem nativeJacobianRow175_eq :
    nativeJacobianRow175 = expectedJacobianRow 175 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow176 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩)]
theorem nativeJacobianRow176_eq :
    nativeJacobianRow176 = expectedJacobianRow 176 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow177 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩)]
theorem nativeJacobianRow177_eq :
    nativeJacobianRow177 = expectedJacobianRow 177 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow178 : List (Nat × Bounds) := [(156,⟨(-2),(2)⟩),(157,⟨(-2),(2)⟩),(168,⟨(-2),(2)⟩),(169,⟨(-2),(2)⟩),(180,⟨(-2),(2)⟩),(181,⟨(-2),(2)⟩),(192,⟨(-2),(2)⟩),(193,⟨(-2),(2)⟩),(204,⟨(-2),(2)⟩),(205,⟨(-2),(2)⟩),(216,⟨(-2),(2)⟩),(217,⟨(-2),(2)⟩)]
theorem nativeJacobianRow178_eq :
    nativeJacobianRow178 = expectedJacobianRow 178 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow179 : List (Nat × Bounds) := []
theorem nativeJacobianRow179_eq :
    nativeJacobianRow179 = expectedJacobianRow 179 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow180 : List (Nat × Bounds) := [(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩)]
theorem nativeJacobianRow180_eq :
    nativeJacobianRow180 = expectedJacobianRow 180 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow181 : List (Nat × Bounds) := [(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩)]
theorem nativeJacobianRow181_eq :
    nativeJacobianRow181 = expectedJacobianRow 181 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow182 : List (Nat × Bounds) := [(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow182_eq :
    nativeJacobianRow182 = expectedJacobianRow 182 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow183 : List (Nat × Bounds) := [(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow183_eq :
    nativeJacobianRow183 = expectedJacobianRow 183 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow184 : List (Nat × Bounds) := [(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow184_eq :
    nativeJacobianRow184 = expectedJacobianRow 184 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow185 : List (Nat × Bounds) := [(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow185_eq :
    nativeJacobianRow185 = expectedJacobianRow 185 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow186 : List (Nat × Bounds) := [(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩)]
theorem nativeJacobianRow186_eq :
    nativeJacobianRow186 = expectedJacobianRow 186 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow187 : List (Nat × Bounds) := [(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩)]
theorem nativeJacobianRow187_eq :
    nativeJacobianRow187 = expectedJacobianRow 187 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow188 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩)]
theorem nativeJacobianRow188_eq :
    nativeJacobianRow188 = expectedJacobianRow 188 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow189 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩)]
theorem nativeJacobianRow189_eq :
    nativeJacobianRow189 = expectedJacobianRow 189 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow190 : List (Nat × Bounds) := [(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩)]
theorem nativeJacobianRow190_eq :
    nativeJacobianRow190 = expectedJacobianRow 190 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow191 : List (Nat × Bounds) := [(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩)]
theorem nativeJacobianRow191_eq :
    nativeJacobianRow191 = expectedJacobianRow 191 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow192 : List (Nat × Bounds) := [(158,⟨(-2),(2)⟩),(159,⟨(-2),(2)⟩),(170,⟨(-2),(2)⟩),(171,⟨(-2),(2)⟩),(182,⟨(-2),(2)⟩),(183,⟨(-2),(2)⟩),(194,⟨(-2),(2)⟩),(195,⟨(-2),(2)⟩),(206,⟨(-2),(2)⟩),(207,⟨(-2),(2)⟩),(218,⟨(-2),(2)⟩),(219,⟨(-2),(2)⟩)]
theorem nativeJacobianRow192_eq :
    nativeJacobianRow192 = expectedJacobianRow 192 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow193 : List (Nat × Bounds) := []
theorem nativeJacobianRow193_eq :
    nativeJacobianRow193 = expectedJacobianRow 193 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow194 : List (Nat × Bounds) := [(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow194_eq :
    nativeJacobianRow194 = expectedJacobianRow 194 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow195 : List (Nat × Bounds) := [(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow195_eq :
    nativeJacobianRow195 = expectedJacobianRow 195 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow196 : List (Nat × Bounds) := [(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow196_eq :
    nativeJacobianRow196 = expectedJacobianRow 196 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow197 : List (Nat × Bounds) := [(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow197_eq :
    nativeJacobianRow197 = expectedJacobianRow 197 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow198 : List (Nat × Bounds) := [(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow198_eq :
    nativeJacobianRow198 = expectedJacobianRow 198 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow199 : List (Nat × Bounds) := [(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow199_eq :
    nativeJacobianRow199 = expectedJacobianRow 199 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow200 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow200_eq :
    nativeJacobianRow200 = expectedJacobianRow 200 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow201 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow201_eq :
    nativeJacobianRow201 = expectedJacobianRow 201 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow202 : List (Nat × Bounds) := [(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow202_eq :
    nativeJacobianRow202 = expectedJacobianRow 202 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow203 : List (Nat × Bounds) := [(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow203_eq :
    nativeJacobianRow203 = expectedJacobianRow 203 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow204 : List (Nat × Bounds) := [(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow204_eq :
    nativeJacobianRow204 = expectedJacobianRow 204 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow205 : List (Nat × Bounds) := [(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩)]
theorem nativeJacobianRow205_eq :
    nativeJacobianRow205 = expectedJacobianRow 205 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow206 : List (Nat × Bounds) := [(160,⟨(-2),(2)⟩),(161,⟨(-2),(2)⟩),(172,⟨(-2),(2)⟩),(173,⟨(-2),(2)⟩),(184,⟨(-2),(2)⟩),(185,⟨(-2),(2)⟩),(196,⟨(-2),(2)⟩),(197,⟨(-2),(2)⟩),(208,⟨(-2),(2)⟩),(209,⟨(-2),(2)⟩),(220,⟨(-2),(2)⟩),(221,⟨(-2),(2)⟩)]
theorem nativeJacobianRow206_eq :
    nativeJacobianRow206 = expectedJacobianRow 206 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow207 : List (Nat × Bounds) := []
theorem nativeJacobianRow207_eq :
    nativeJacobianRow207 = expectedJacobianRow 207 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow208 : List (Nat × Bounds) := [(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow208_eq :
    nativeJacobianRow208 = expectedJacobianRow 208 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow209 : List (Nat × Bounds) := [(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow209_eq :
    nativeJacobianRow209 = expectedJacobianRow 209 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow210 : List (Nat × Bounds) := [(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow210_eq :
    nativeJacobianRow210 = expectedJacobianRow 210 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow211 : List (Nat × Bounds) := [(152,⟨(-1),(1)⟩),(153,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(164,⟨(-1),(1)⟩),(165,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(176,⟨(-1),(1)⟩),(177,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(188,⟨(-1),(1)⟩),(189,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(200,⟨(-1),(1)⟩),(201,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(212,⟨(-1),(1)⟩),(213,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow211_eq :
    nativeJacobianRow211 = expectedJacobianRow 211 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow212 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow212_eq :
    nativeJacobianRow212 = expectedJacobianRow 212 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow213 : List (Nat × Bounds) := [(154,⟨(-1),(1)⟩),(155,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(166,⟨(-1),(1)⟩),(167,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(178,⟨(-1),(1)⟩),(179,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(190,⟨(-1),(1)⟩),(191,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(202,⟨(-1),(1)⟩),(203,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(214,⟨(-1),(1)⟩),(215,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow213_eq :
    nativeJacobianRow213 = expectedJacobianRow 213 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow214 : List (Nat × Bounds) := [(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow214_eq :
    nativeJacobianRow214 = expectedJacobianRow 214 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow215 : List (Nat × Bounds) := [(156,⟨(-1),(1)⟩),(157,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(168,⟨(-1),(1)⟩),(169,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(180,⟨(-1),(1)⟩),(181,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(192,⟨(-1),(1)⟩),(193,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(204,⟨(-1),(1)⟩),(205,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(216,⟨(-1),(1)⟩),(217,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow215_eq :
    nativeJacobianRow215 = expectedJacobianRow 215 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow216 : List (Nat × Bounds) := [(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow216_eq :
    nativeJacobianRow216 = expectedJacobianRow 216 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow217 : List (Nat × Bounds) := [(158,⟨(-1),(1)⟩),(159,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(170,⟨(-1),(1)⟩),(171,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(182,⟨(-1),(1)⟩),(183,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(194,⟨(-1),(1)⟩),(195,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(206,⟨(-1),(1)⟩),(207,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(218,⟨(-1),(1)⟩),(219,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow217_eq :
    nativeJacobianRow217 = expectedJacobianRow 217 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow218 : List (Nat × Bounds) := [(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow218_eq :
    nativeJacobianRow218 = expectedJacobianRow 218 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow219 : List (Nat × Bounds) := [(160,⟨(-1),(1)⟩),(161,⟨(-1),(1)⟩),(162,⟨(-1),(1)⟩),(163,⟨(-1),(1)⟩),(172,⟨(-1),(1)⟩),(173,⟨(-1),(1)⟩),(174,⟨(-1),(1)⟩),(175,⟨(-1),(1)⟩),(184,⟨(-1),(1)⟩),(185,⟨(-1),(1)⟩),(186,⟨(-1),(1)⟩),(187,⟨(-1),(1)⟩),(196,⟨(-1),(1)⟩),(197,⟨(-1),(1)⟩),(198,⟨(-1),(1)⟩),(199,⟨(-1),(1)⟩),(208,⟨(-1),(1)⟩),(209,⟨(-1),(1)⟩),(210,⟨(-1),(1)⟩),(211,⟨(-1),(1)⟩),(220,⟨(-1),(1)⟩),(221,⟨(-1),(1)⟩),(222,⟨(-1),(1)⟩),(223,⟨(-1),(1)⟩)]
theorem nativeJacobianRow219_eq :
    nativeJacobianRow219 = expectedJacobianRow 219 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow220 : List (Nat × Bounds) := [(162,⟨(-2),(2)⟩),(163,⟨(-2),(2)⟩),(174,⟨(-2),(2)⟩),(175,⟨(-2),(2)⟩),(186,⟨(-2),(2)⟩),(187,⟨(-2),(2)⟩),(198,⟨(-2),(2)⟩),(199,⟨(-2),(2)⟩),(210,⟨(-2),(2)⟩),(211,⟨(-2),(2)⟩),(222,⟨(-2),(2)⟩),(223,⟨(-2),(2)⟩)]
theorem nativeJacobianRow220_eq :
    nativeJacobianRow220 = expectedJacobianRow 220 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow221 : List (Nat × Bounds) := []
theorem nativeJacobianRow221_eq :
    nativeJacobianRow221 = expectedJacobianRow 221 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow222 : List (Nat × Bounds) := [(80,⟨(-2),(2)⟩),(81,⟨(-2),(2)⟩)]
theorem nativeJacobianRow222_eq :
    nativeJacobianRow222 = expectedJacobianRow 222 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow223 : List (Nat × Bounds) := [(82,⟨(-2),(2)⟩),(83,⟨(-2),(2)⟩)]
theorem nativeJacobianRow223_eq :
    nativeJacobianRow223 = expectedJacobianRow 223 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow224 : List (Nat × Bounds) := [(84,⟨(-2),(2)⟩),(85,⟨(-2),(2)⟩)]
theorem nativeJacobianRow224_eq :
    nativeJacobianRow224 = expectedJacobianRow 224 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow225 : List (Nat × Bounds) := [(86,⟨(-2),(2)⟩),(87,⟨(-2),(2)⟩)]
theorem nativeJacobianRow225_eq :
    nativeJacobianRow225 = expectedJacobianRow 225 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow226 : List (Nat × Bounds) := [(88,⟨(-2),(2)⟩),(89,⟨(-2),(2)⟩)]
theorem nativeJacobianRow226_eq :
    nativeJacobianRow226 = expectedJacobianRow 226 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow227 : List (Nat × Bounds) := [(90,⟨(-2),(2)⟩),(91,⟨(-2),(2)⟩)]
theorem nativeJacobianRow227_eq :
    nativeJacobianRow227 = expectedJacobianRow 227 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow228 : List (Nat × Bounds) := [(92,⟨(-2),(2)⟩),(93,⟨(-2),(2)⟩)]
theorem nativeJacobianRow228_eq :
    nativeJacobianRow228 = expectedJacobianRow 228 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow229 : List (Nat × Bounds) := [(94,⟨(-2),(2)⟩),(95,⟨(-2),(2)⟩)]
theorem nativeJacobianRow229_eq :
    nativeJacobianRow229 = expectedJacobianRow 229 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow230 : List (Nat × Bounds) := [(96,⟨(-2),(2)⟩),(97,⟨(-2),(2)⟩)]
theorem nativeJacobianRow230_eq :
    nativeJacobianRow230 = expectedJacobianRow 230 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow231 : List (Nat × Bounds) := [(98,⟨(-2),(2)⟩),(99,⟨(-2),(2)⟩)]
theorem nativeJacobianRow231_eq :
    nativeJacobianRow231 = expectedJacobianRow 231 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow232 : List (Nat × Bounds) := [(100,⟨(-2),(2)⟩),(101,⟨(-2),(2)⟩)]
theorem nativeJacobianRow232_eq :
    nativeJacobianRow232 = expectedJacobianRow 232 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow233 : List (Nat × Bounds) := [(102,⟨(-2),(2)⟩),(103,⟨(-2),(2)⟩)]
theorem nativeJacobianRow233_eq :
    nativeJacobianRow233 = expectedJacobianRow 233 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow234 : List (Nat × Bounds) := [(104,⟨(-2),(2)⟩),(105,⟨(-2),(2)⟩)]
theorem nativeJacobianRow234_eq :
    nativeJacobianRow234 = expectedJacobianRow 234 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow235 : List (Nat × Bounds) := [(106,⟨(-2),(2)⟩),(107,⟨(-2),(2)⟩)]
theorem nativeJacobianRow235_eq :
    nativeJacobianRow235 = expectedJacobianRow 235 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow236 : List (Nat × Bounds) := [(108,⟨(-2),(2)⟩),(109,⟨(-2),(2)⟩)]
theorem nativeJacobianRow236_eq :
    nativeJacobianRow236 = expectedJacobianRow 236 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow237 : List (Nat × Bounds) := [(110,⟨(-2),(2)⟩),(111,⟨(-2),(2)⟩)]
theorem nativeJacobianRow237_eq :
    nativeJacobianRow237 = expectedJacobianRow 237 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow238 : List (Nat × Bounds) := [(112,⟨(-2),(2)⟩),(113,⟨(-2),(2)⟩)]
theorem nativeJacobianRow238_eq :
    nativeJacobianRow238 = expectedJacobianRow 238 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow239 : List (Nat × Bounds) := [(114,⟨(-2),(2)⟩),(115,⟨(-2),(2)⟩)]
theorem nativeJacobianRow239_eq :
    nativeJacobianRow239 = expectedJacobianRow 239 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

end MUB.SzollosiRectangularReflection

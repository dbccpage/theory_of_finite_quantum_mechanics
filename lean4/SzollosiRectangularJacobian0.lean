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

def nativeJacobianRow0 : List (Nat × Bounds) := [(0,⟨(-2),(2)⟩),(1,⟨(-2),(2)⟩)]
theorem nativeJacobianRow0_eq :
    nativeJacobianRow0 = expectedJacobianRow 0 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow1 : List (Nat × Bounds) := [(2,⟨(-2),(2)⟩),(3,⟨(-2),(2)⟩)]
theorem nativeJacobianRow1_eq :
    nativeJacobianRow1 = expectedJacobianRow 1 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow2 : List (Nat × Bounds) := [(4,⟨(-2),(2)⟩),(5,⟨(-2),(2)⟩)]
theorem nativeJacobianRow2_eq :
    nativeJacobianRow2 = expectedJacobianRow 2 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow3 : List (Nat × Bounds) := [(6,⟨(-2),(2)⟩),(7,⟨(-2),(2)⟩)]
theorem nativeJacobianRow3_eq :
    nativeJacobianRow3 = expectedJacobianRow 3 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow4 : List (Nat × Bounds) := [(0,⟨(0),(2)⟩),(1,⟨(-1),(1)⟩),(2,⟨(0),(2)⟩),(3,⟨(-1),(1)⟩),(4,⟨(0),(2)⟩),(5,⟨(-1),(1)⟩),(6,⟨(0),(2)⟩),(7,⟨(-1),(1)⟩)]
theorem nativeJacobianRow4_eq :
    nativeJacobianRow4 = expectedJacobianRow 4 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow5 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(0),(2)⟩),(2,⟨(-1),(1)⟩),(3,⟨(0),(2)⟩),(4,⟨(-1),(1)⟩),(5,⟨(0),(2)⟩),(6,⟨(-1),(1)⟩),(7,⟨(0),(2)⟩)]
theorem nativeJacobianRow5_eq :
    nativeJacobianRow5 = expectedJacobianRow 5 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow6 : List (Nat × Bounds) := [(8,⟨(1),(1)⟩)]
theorem nativeJacobianRow6_eq :
    nativeJacobianRow6 = expectedJacobianRow 6 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow7 : List (Nat × Bounds) := [(9,⟨(1),(1)⟩)]
theorem nativeJacobianRow7_eq :
    nativeJacobianRow7 = expectedJacobianRow 7 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow8 : List (Nat × Bounds) := [(0,⟨(-1),(-1)⟩),(10,⟨(1),(1)⟩)]
theorem nativeJacobianRow8_eq :
    nativeJacobianRow8 = expectedJacobianRow 8 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow9 : List (Nat × Bounds) := [(1,⟨(-1),(-1)⟩),(11,⟨(1),(1)⟩)]
theorem nativeJacobianRow9_eq :
    nativeJacobianRow9 = expectedJacobianRow 9 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow10 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(-1),(1)⟩),(2,⟨(-1),(1)⟩),(3,⟨(-1),(1)⟩),(12,⟨(1),(1)⟩)]
theorem nativeJacobianRow10_eq :
    nativeJacobianRow10 = expectedJacobianRow 10 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow11 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(-1),(1)⟩),(2,⟨(-1),(1)⟩),(3,⟨(-1),(1)⟩),(13,⟨(1),(1)⟩)]
theorem nativeJacobianRow11_eq :
    nativeJacobianRow11 = expectedJacobianRow 11 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow12 : List (Nat × Bounds) := [(14,⟨(1),(1)⟩)]
theorem nativeJacobianRow12_eq :
    nativeJacobianRow12 = expectedJacobianRow 12 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow13 : List (Nat × Bounds) := [(15,⟨(1),(1)⟩)]
theorem nativeJacobianRow13_eq :
    nativeJacobianRow13 = expectedJacobianRow 13 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow14 : List (Nat × Bounds) := [(4,⟨(-1),(-1)⟩),(16,⟨(1),(1)⟩)]
theorem nativeJacobianRow14_eq :
    nativeJacobianRow14 = expectedJacobianRow 14 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow15 : List (Nat × Bounds) := [(5,⟨(-1),(-1)⟩),(17,⟨(1),(1)⟩)]
theorem nativeJacobianRow15_eq :
    nativeJacobianRow15 = expectedJacobianRow 15 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow16 : List (Nat × Bounds) := [(4,⟨(-1),(1)⟩),(5,⟨(-1),(1)⟩),(6,⟨(-1),(1)⟩),(7,⟨(-1),(1)⟩),(18,⟨(1),(1)⟩)]
theorem nativeJacobianRow16_eq :
    nativeJacobianRow16 = expectedJacobianRow 16 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow17 : List (Nat × Bounds) := [(4,⟨(-1),(1)⟩),(5,⟨(-1),(1)⟩),(6,⟨(-1),(1)⟩),(7,⟨(-1),(1)⟩),(19,⟨(1),(1)⟩)]
theorem nativeJacobianRow17_eq :
    nativeJacobianRow17 = expectedJacobianRow 17 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow18 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(-1),(1)⟩),(2,⟨(-1),(1)⟩),(3,⟨(-1),(1)⟩),(20,⟨(1),(1)⟩)]
theorem nativeJacobianRow18_eq :
    nativeJacobianRow18 = expectedJacobianRow 18 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow19 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(-1),(1)⟩),(2,⟨(-1),(1)⟩),(3,⟨(-1),(1)⟩),(21,⟨(1),(1)⟩)]
theorem nativeJacobianRow19_eq :
    nativeJacobianRow19 = expectedJacobianRow 19 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow20 : List (Nat × Bounds) := [(22,⟨(1),(1)⟩)]
theorem nativeJacobianRow20_eq :
    nativeJacobianRow20 = expectedJacobianRow 20 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow21 : List (Nat × Bounds) := [(23,⟨(1),(1)⟩)]
theorem nativeJacobianRow21_eq :
    nativeJacobianRow21 = expectedJacobianRow 21 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow22 : List (Nat × Bounds) := [(0,⟨(-1),(-1)⟩),(24,⟨(1),(1)⟩)]
theorem nativeJacobianRow22_eq :
    nativeJacobianRow22 = expectedJacobianRow 22 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow23 : List (Nat × Bounds) := [(1,⟨(-1),(-1)⟩),(25,⟨(1),(1)⟩)]
theorem nativeJacobianRow23_eq :
    nativeJacobianRow23 = expectedJacobianRow 23 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow24 : List (Nat × Bounds) := [(4,⟨(-1),(1)⟩),(5,⟨(-1),(1)⟩),(6,⟨(-1),(1)⟩),(7,⟨(-1),(1)⟩),(26,⟨(1),(1)⟩)]
theorem nativeJacobianRow24_eq :
    nativeJacobianRow24 = expectedJacobianRow 24 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow25 : List (Nat × Bounds) := [(4,⟨(-1),(1)⟩),(5,⟨(-1),(1)⟩),(6,⟨(-1),(1)⟩),(7,⟨(-1),(1)⟩),(27,⟨(1),(1)⟩)]
theorem nativeJacobianRow25_eq :
    nativeJacobianRow25 = expectedJacobianRow 25 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow26 : List (Nat × Bounds) := [(28,⟨(1),(1)⟩)]
theorem nativeJacobianRow26_eq :
    nativeJacobianRow26 = expectedJacobianRow 26 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow27 : List (Nat × Bounds) := [(29,⟨(1),(1)⟩)]
theorem nativeJacobianRow27_eq :
    nativeJacobianRow27 = expectedJacobianRow 27 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow28 : List (Nat × Bounds) := [(4,⟨(-1),(-1)⟩),(30,⟨(1),(1)⟩)]
theorem nativeJacobianRow28_eq :
    nativeJacobianRow28 = expectedJacobianRow 28 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow29 : List (Nat × Bounds) := [(5,⟨(-1),(-1)⟩),(31,⟨(1),(1)⟩)]
theorem nativeJacobianRow29_eq :
    nativeJacobianRow29 = expectedJacobianRow 29 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow30 : List (Nat × Bounds) := [(0,⟨(-1),(-1)⟩),(32,⟨(1),(1)⟩)]
theorem nativeJacobianRow30_eq :
    nativeJacobianRow30 = expectedJacobianRow 30 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow31 : List (Nat × Bounds) := [(1,⟨(-1),(-1)⟩),(33,⟨(1),(1)⟩)]
theorem nativeJacobianRow31_eq :
    nativeJacobianRow31 = expectedJacobianRow 31 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow32 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(-1),(1)⟩),(2,⟨(-1),(1)⟩),(3,⟨(-1),(1)⟩),(34,⟨(1),(1)⟩)]
theorem nativeJacobianRow32_eq :
    nativeJacobianRow32 = expectedJacobianRow 32 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow33 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(-1),(1)⟩),(2,⟨(-1),(1)⟩),(3,⟨(-1),(1)⟩),(35,⟨(1),(1)⟩)]
theorem nativeJacobianRow33_eq :
    nativeJacobianRow33 = expectedJacobianRow 33 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow34 : List (Nat × Bounds) := [(36,⟨(1),(1)⟩)]
theorem nativeJacobianRow34_eq :
    nativeJacobianRow34 = expectedJacobianRow 34 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow35 : List (Nat × Bounds) := [(37,⟨(1),(1)⟩)]
theorem nativeJacobianRow35_eq :
    nativeJacobianRow35 = expectedJacobianRow 35 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow36 : List (Nat × Bounds) := [(4,⟨(-1),(-1)⟩),(38,⟨(1),(1)⟩)]
theorem nativeJacobianRow36_eq :
    nativeJacobianRow36 = expectedJacobianRow 36 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow37 : List (Nat × Bounds) := [(5,⟨(-1),(-1)⟩),(39,⟨(1),(1)⟩)]
theorem nativeJacobianRow37_eq :
    nativeJacobianRow37 = expectedJacobianRow 37 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow38 : List (Nat × Bounds) := [(4,⟨(-1),(1)⟩),(5,⟨(-1),(1)⟩),(6,⟨(-1),(1)⟩),(7,⟨(-1),(1)⟩),(40,⟨(1),(1)⟩)]
theorem nativeJacobianRow38_eq :
    nativeJacobianRow38 = expectedJacobianRow 38 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow39 : List (Nat × Bounds) := [(4,⟨(-1),(1)⟩),(5,⟨(-1),(1)⟩),(6,⟨(-1),(1)⟩),(7,⟨(-1),(1)⟩),(41,⟨(1),(1)⟩)]
theorem nativeJacobianRow39_eq :
    nativeJacobianRow39 = expectedJacobianRow 39 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow40 : List (Nat × Bounds) := [(42,⟨(1),(1)⟩)]
theorem nativeJacobianRow40_eq :
    nativeJacobianRow40 = expectedJacobianRow 40 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow41 : List (Nat × Bounds) := [(43,⟨(1),(1)⟩)]
theorem nativeJacobianRow41_eq :
    nativeJacobianRow41 = expectedJacobianRow 41 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow42 : List (Nat × Bounds) := [(44,⟨(1),(1)⟩)]
theorem nativeJacobianRow42_eq :
    nativeJacobianRow42 = expectedJacobianRow 42 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow43 : List (Nat × Bounds) := [(45,⟨(1),(1)⟩)]
theorem nativeJacobianRow43_eq :
    nativeJacobianRow43 = expectedJacobianRow 43 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow44 : List (Nat × Bounds) := [(4,⟨(-1),(1)⟩),(5,⟨(-1),(1)⟩),(6,⟨(-1),(1)⟩),(7,⟨(-1),(1)⟩),(46,⟨(1),(1)⟩)]
theorem nativeJacobianRow44_eq :
    nativeJacobianRow44 = expectedJacobianRow 44 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow45 : List (Nat × Bounds) := [(4,⟨(-1),(1)⟩),(5,⟨(-1),(1)⟩),(6,⟨(-1),(1)⟩),(7,⟨(-1),(1)⟩),(47,⟨(1),(1)⟩)]
theorem nativeJacobianRow45_eq :
    nativeJacobianRow45 = expectedJacobianRow 45 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow46 : List (Nat × Bounds) := [(4,⟨(-1),(-1)⟩),(48,⟨(1),(1)⟩)]
theorem nativeJacobianRow46_eq :
    nativeJacobianRow46 = expectedJacobianRow 46 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow47 : List (Nat × Bounds) := [(5,⟨(1),(1)⟩),(49,⟨(1),(1)⟩)]
theorem nativeJacobianRow47_eq :
    nativeJacobianRow47 = expectedJacobianRow 47 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow48 : List (Nat × Bounds) := [(50,⟨(1),(1)⟩)]
theorem nativeJacobianRow48_eq :
    nativeJacobianRow48 = expectedJacobianRow 48 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow49 : List (Nat × Bounds) := [(51,⟨(1),(1)⟩)]
theorem nativeJacobianRow49_eq :
    nativeJacobianRow49 = expectedJacobianRow 49 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow50 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(-1),(1)⟩),(2,⟨(-1),(1)⟩),(3,⟨(-1),(1)⟩),(52,⟨(1),(1)⟩)]
theorem nativeJacobianRow50_eq :
    nativeJacobianRow50 = expectedJacobianRow 50 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow51 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(-1),(1)⟩),(2,⟨(-1),(1)⟩),(3,⟨(-1),(1)⟩),(53,⟨(1),(1)⟩)]
theorem nativeJacobianRow51_eq :
    nativeJacobianRow51 = expectedJacobianRow 51 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow52 : List (Nat × Bounds) := [(0,⟨(1),(1)⟩),(54,⟨(1),(1)⟩)]
theorem nativeJacobianRow52_eq :
    nativeJacobianRow52 = expectedJacobianRow 52 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow53 : List (Nat × Bounds) := [(1,⟨(-1),(-1)⟩),(55,⟨(1),(1)⟩)]
theorem nativeJacobianRow53_eq :
    nativeJacobianRow53 = expectedJacobianRow 53 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow54 : List (Nat × Bounds) := [(4,⟨(-1),(-1)⟩),(56,⟨(1),(1)⟩)]
theorem nativeJacobianRow54_eq :
    nativeJacobianRow54 = expectedJacobianRow 54 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow55 : List (Nat × Bounds) := [(5,⟨(1),(1)⟩),(57,⟨(1),(1)⟩)]
theorem nativeJacobianRow55_eq :
    nativeJacobianRow55 = expectedJacobianRow 55 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow56 : List (Nat × Bounds) := [(58,⟨(1),(1)⟩)]
theorem nativeJacobianRow56_eq :
    nativeJacobianRow56 = expectedJacobianRow 56 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow57 : List (Nat × Bounds) := [(59,⟨(1),(1)⟩)]
theorem nativeJacobianRow57_eq :
    nativeJacobianRow57 = expectedJacobianRow 57 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow58 : List (Nat × Bounds) := [(4,⟨(-1),(1)⟩),(5,⟨(-1),(1)⟩),(6,⟨(-1),(1)⟩),(7,⟨(-1),(1)⟩),(60,⟨(1),(1)⟩)]
theorem nativeJacobianRow58_eq :
    nativeJacobianRow58 = expectedJacobianRow 58 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow59 : List (Nat × Bounds) := [(4,⟨(-1),(1)⟩),(5,⟨(-1),(1)⟩),(6,⟨(-1),(1)⟩),(7,⟨(-1),(1)⟩),(61,⟨(1),(1)⟩)]
theorem nativeJacobianRow59_eq :
    nativeJacobianRow59 = expectedJacobianRow 59 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow60 : List (Nat × Bounds) := [(0,⟨(1),(1)⟩),(62,⟨(1),(1)⟩)]
theorem nativeJacobianRow60_eq :
    nativeJacobianRow60 = expectedJacobianRow 60 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow61 : List (Nat × Bounds) := [(1,⟨(-1),(-1)⟩),(63,⟨(1),(1)⟩)]
theorem nativeJacobianRow61_eq :
    nativeJacobianRow61 = expectedJacobianRow 61 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow62 : List (Nat × Bounds) := [(64,⟨(1),(1)⟩)]
theorem nativeJacobianRow62_eq :
    nativeJacobianRow62 = expectedJacobianRow 62 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow63 : List (Nat × Bounds) := [(65,⟨(1),(1)⟩)]
theorem nativeJacobianRow63_eq :
    nativeJacobianRow63 = expectedJacobianRow 63 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow64 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(-1),(1)⟩),(2,⟨(-1),(1)⟩),(3,⟨(-1),(1)⟩),(66,⟨(1),(1)⟩)]
theorem nativeJacobianRow64_eq :
    nativeJacobianRow64 = expectedJacobianRow 64 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow65 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(-1),(1)⟩),(2,⟨(-1),(1)⟩),(3,⟨(-1),(1)⟩),(67,⟨(1),(1)⟩)]
theorem nativeJacobianRow65_eq :
    nativeJacobianRow65 = expectedJacobianRow 65 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow66 : List (Nat × Bounds) := [(4,⟨(-1),(1)⟩),(5,⟨(-1),(1)⟩),(6,⟨(-1),(1)⟩),(7,⟨(-1),(1)⟩),(68,⟨(1),(1)⟩)]
theorem nativeJacobianRow66_eq :
    nativeJacobianRow66 = expectedJacobianRow 66 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow67 : List (Nat × Bounds) := [(4,⟨(-1),(1)⟩),(5,⟨(-1),(1)⟩),(6,⟨(-1),(1)⟩),(7,⟨(-1),(1)⟩),(69,⟨(1),(1)⟩)]
theorem nativeJacobianRow67_eq :
    nativeJacobianRow67 = expectedJacobianRow 67 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow68 : List (Nat × Bounds) := [(4,⟨(-1),(-1)⟩),(70,⟨(1),(1)⟩)]
theorem nativeJacobianRow68_eq :
    nativeJacobianRow68 = expectedJacobianRow 68 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow69 : List (Nat × Bounds) := [(5,⟨(1),(1)⟩),(71,⟨(1),(1)⟩)]
theorem nativeJacobianRow69_eq :
    nativeJacobianRow69 = expectedJacobianRow 69 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow70 : List (Nat × Bounds) := [(72,⟨(1),(1)⟩)]
theorem nativeJacobianRow70_eq :
    nativeJacobianRow70 = expectedJacobianRow 70 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow71 : List (Nat × Bounds) := [(73,⟨(1),(1)⟩)]
theorem nativeJacobianRow71_eq :
    nativeJacobianRow71 = expectedJacobianRow 71 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow72 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(-1),(1)⟩),(2,⟨(-1),(1)⟩),(3,⟨(-1),(1)⟩),(74,⟨(1),(1)⟩)]
theorem nativeJacobianRow72_eq :
    nativeJacobianRow72 = expectedJacobianRow 72 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow73 : List (Nat × Bounds) := [(0,⟨(-1),(1)⟩),(1,⟨(-1),(1)⟩),(2,⟨(-1),(1)⟩),(3,⟨(-1),(1)⟩),(75,⟨(1),(1)⟩)]
theorem nativeJacobianRow73_eq :
    nativeJacobianRow73 = expectedJacobianRow 73 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow74 : List (Nat × Bounds) := [(0,⟨(1),(1)⟩),(76,⟨(1),(1)⟩)]
theorem nativeJacobianRow74_eq :
    nativeJacobianRow74 = expectedJacobianRow 74 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow75 : List (Nat × Bounds) := [(1,⟨(-1),(-1)⟩),(77,⟨(1),(1)⟩)]
theorem nativeJacobianRow75_eq :
    nativeJacobianRow75 = expectedJacobianRow 75 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow76 : List (Nat × Bounds) := [(78,⟨(1),(1)⟩)]
theorem nativeJacobianRow76_eq :
    nativeJacobianRow76 = expectedJacobianRow 76 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow77 : List (Nat × Bounds) := [(79,⟨(1),(1)⟩)]
theorem nativeJacobianRow77_eq :
    nativeJacobianRow77 = expectedJacobianRow 77 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow78 : List (Nat × Bounds) := [(80,⟨(-2),(2)⟩),(81,⟨(-2),(2)⟩),(92,⟨(-2),(2)⟩),(93,⟨(-2),(2)⟩),(104,⟨(-2),(2)⟩),(105,⟨(-2),(2)⟩),(116,⟨(-2),(2)⟩),(117,⟨(-2),(2)⟩),(128,⟨(-2),(2)⟩),(129,⟨(-2),(2)⟩),(140,⟨(-2),(2)⟩),(141,⟨(-2),(2)⟩)]
theorem nativeJacobianRow78_eq :
    nativeJacobianRow78 = expectedJacobianRow 78 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

def nativeJacobianRow79 : List (Nat × Bounds) := []
theorem nativeJacobianRow79_eq :
    nativeJacobianRow79 = expectedJacobianRow 79 := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel

end MUB.SzollosiRectangularReflection

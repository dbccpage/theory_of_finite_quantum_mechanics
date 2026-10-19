import BellOperad
open QuantumMechanics.BellOperad QuantumMechanics.BellClassicalJointExtension
-- Deliberately false: the valid all-minus assignment gives four here, not two.
example : products plusAssignment 0 + products plusAssignment 1 +
    products plusAssignment 2 + products plusAssignment 3 = score plusAssignment := by decide

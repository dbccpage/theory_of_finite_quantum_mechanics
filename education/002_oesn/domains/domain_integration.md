---
documentation_contract: symbol-game-documentation/v1
title: 'Declaring a downstream interpretation'
kind: application-reference
layer: downstream_application
realizes: null
authority_effect: 'None'
genesis_effect: 'None'
---

# Declaring a downstream interpretation

An interpretation specifies an actual source carrier, a target carrier and
the protected questions. It does not acquire a native Genesis stage by
sharing notation with S(n). Work through the
[domain integration model](../code/sn_applications.py)
after the [reading guide](../reading_guide.md); its lesson was retired on 2026-10-06.

## State what the adapter must preserve

For an adapter r and protected answer F, a decoder on r's actual image
exists iff `r(x)=r(y)` implies `F(x)=F(y)`. Give a conflicting pair when
that condition fails. For stateful systems, also require that source
transitions commute with target transitions and that equivalence respects
future admitted events. Preserving today's report can lose tomorrow's
observable behavior.

| Example | Protected data | Failure to expose |
| --- | --- | --- |
| [Finite join](databases/s21_topological_query.md) | Selected query answers | Projection can merge rows with opposite answers |
| [Request-reply protocol](protocols/s24_session_types.md) | Ordered events, queues, terminal flags | Unordered events can lose executability |
| Cochain realization | Repair image and declared diagnostics | Matching dimensions do not imply commuting maps |

For the last example, use the checked `linear_algebra::finite_cochain_map`
owner and the [admission/transport lab](../../006_oewdp/curriculum/710_wdp_finite_obstruction/concepts/lesson_710_04_admission_and_transport.md).
The maps must bind the actual differential matrices. A retraction preserves
its old image; equality of the opposite composite requires additional evidence.

## Preserve the meaning of the result

A set relation, a protocol state and a cochain are different carriers.
Assign Phi or Gamma only through a declared cochain bridge with checked
equations. Record lost fields, costs, policy and permission separately.
Counterexamples identify missing preservation; they do not automatically
license extension, change a native survivor register or establish physical
truth. A composition claim must bind the intermediate carrier and every
protected question needed by the next adapter.

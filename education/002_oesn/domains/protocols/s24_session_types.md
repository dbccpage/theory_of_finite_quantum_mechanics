---
documentation_contract: symbol-game-documentation/v1
title: 'Finite request-reply protocols and scheduling'
kind: application-reference
layer: downstream_application
realizes: null
legacy_level: 24
authority_effect: 'None'
genesis_effect: 'None'
---

# Finite request-reply protocols and scheduling

This is a downstream protocol interpretation, not native S(24). The [local channel example](../../code/sn_applications.py) is a two-step
state machine; it does not implement the two-actor FIFO system specified below.
The retired lesson and notebook are not verification evidence. One successful execution alone does not
prove general deadlock freedom.

## Declare the transition system

Take a client that sends one request and receives one reply; its server
receives that request and sends that reply. Each directed FIFO has capacity
one and starts empty. Sending requires space; receiving requires the right
message. A transition consumes the scheduled actor's next action exactly
once. No message loss, external writes or additional actor is permitted.

The complete reachable sequence in this model is:

| State | Enabled action | Request FIFO | Reply FIFO |
| --- | --- | --- | --- |
| Initial | Client sends request | Empty | Empty |
| Request sent | Server receives request | Request | Empty |
| Request consumed | Server sends reply | Empty | Empty |
| Reply sent | Client receives reply | Empty | Reply |
| Both complete | Terminal | Empty | Empty |

Every nonterminal reachable state has an enabled action, so none is a
deadlock. Four enabled transitions reach the terminal state. A scheduler
that continually selects a disabled actor can still starve the enabled
one; eventual execution needs a scheduling assumption. An asynchronous
network additionally needs its delivery and failure model.

## Countermodel and protected observations

If both actors start by receiving from empty queues, neither transition is
enabled. This is a deadlock on the same finite queue carrier. Complementary
labels alone do not repair the wrong initial protocol.

Protect the action order, queue contents and completion flags when adapting
this system. Collapsing logs to a multiset loses the send-before-receive
condition. The [S(n) reading guide](../../reading_guide.md) and
[WDP replay bridge](../../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md)
explain why a receipt must replay actual ordered transitions. Such a receipt
does not grant network or institutional execution permission.

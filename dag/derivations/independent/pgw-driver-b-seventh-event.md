Status: AI-drafted, awaiting human review.

# PGW-DRIVER-B-SEVENTH-EVENT

Node status stays OPEN. This note records the six constructor names of the sealed derivation Event.

## Constructor names

The sealed derivation Event has six constructors. Their names, in constructor order, are Supply, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, and Impose.

Supply carries a token. AdmitForm carries an arity. AdmitInst carries a form index and an argument list. AdmitRuleAll carries a form index. Impose carries a pair of indices. AdmitDatum carries no payload. The constructor name does not depend on those payloads.

## Finite check

The name list has length 6. The six strings are pairwise distinct. Each string is the constructor name of one event: Supply at token 0, AdmitDatum, AdmitForm at arity 1, AdmitInst at form 0 with an empty argument list, AdmitRuleAll at form 0, and Impose at the pair 0, 1. The string Seventh is not in the list. For every event, the constructor name is in the list and differs from Seventh.

## What is proved

The sealed derivation Event has those six constructor names, the list has length 6 and no duplicates, every event name lands in the list, each listed name occurs, and Seventh is outside the list.

## What is assumed

The sealed derivation Event is the inductive type in the imported derivation core. The name of a constructor is the string recorded above.

## What is open

A harness guard that refuses a seventh constructor, a seal amendment, and a theorem that six kinds suffice for every lift stay open. Status stays OPEN.

Status: AI-drafted, awaiting human review.

# PGW-K-ITEM-DELTA-GRAMMAR, one arity-one census

The sealed grammar in the node statement allows items of arity at most two and sequences of cost at most two, and it asks for pruning lemmas against the unpruned space at every larger item count. This note treats one smaller base.

## Base and atoms

The base has data count 2, form count 0, no instances and no rules. An atom is one of ten admissions:

- a fresh datum;
- one unary form;
- a uniform rule on form 0 or on form 1;
- a unary instance on form 0 or form 1 whose argument is 0, 1 or 2.

An instance is admitted only when its form index is already present and its argument is strictly below the current data count. A rule is admitted only when its form index is already present. A fresh datum always increases the data count by 1. A unary form always increases the form count by 1.

The target profile bit of an argument on a form is true when that form exists and either the uniform rule names the form or the instance list contains that form and argument. The two target arguments are 0 and 1. A state separates when those two bits differ on form 0, or when form 1 exists and those two bits differ on form 1.

## Census of length at most two

There are 10 atoms and 100 ordered pairs. Replaying each one from the base leaves 2 well-formed single items and 7 well-formed pairs, 9 in total:

- datum;
- form;
- datum then datum;
- datum then form;
- form then datum;
- form then form;
- form then rule on form 0;
- form then instance of argument 0 on form 0;
- form then instance of argument 1 on form 0.

No other single item or ordered pair in the ten-atom universe is admitted. No single item separates. Exactly 2 pairs separate: form then argument 0, and form then argument 1. The other 7 well-formed deltas leave the target bits equal.

The three two-item deltas that admit a fresh datum are datum-datum, datum-form and form-datum. Each ends with data count greater than 2, and none separates.

Form then the uniform rule on form 0 sets both target bits on form 0 to true, so it does not separate.

## Two histories of length three

Form, then the instance of argument 0, has length 2. The target bits are true and false, so the state separates. Adding the uniform rule on form 0 makes length 3. Both target bits are then true, so the longer history does not separate. The two-item prefix is shorter than the three-item rule extension.

Datum, then form, then the instance of argument 2, has length 3. The instance list records the pair (0, 2). Both target bits stay false, so the state does not separate. The instance argument is not a target datum.

## What is proved

On this base and this ten-atom universe, the nine well-formed deltas of length at most 2 are the list above. Two of them separate the target bits. Seven do not. The form-rule delta sets both bits true. The three-item rule extension equalizes a pair of bits that the two-item prefix separates, and it is longer. The three-item instance of argument 2 keeps both target bits false.

## What is assumed

Admission, profile bits and separation are the functions defined in this note and in the campaign module. The base starts empty of forms, instances and rules. Every form in the universe has arity one. AuthorityEffect is None.

## What is open

Arity two is not in the atom universe. A grammar for every sequence of three or more items is not enumerated. The sealed cost-two minimum on the unpruned space of the original candidate generator is not rechecked. The mention file and the rule-bridge file are not rechecked. The node stays OPEN.

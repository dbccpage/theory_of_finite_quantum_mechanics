"""Explicit nested shape specifications, independent of source guard text."""
from copy import deepcopy

from collection_metadata import challenge as collection_challenge
from collection_metadata import inventory, invalidate, loop_block, schema_cases
from collection_metadata import variants as collection_variants
from parameter_metadata import challenge as parameter_challenge
from parameter_metadata import variants as parameter_variants


def child_cases(child):
    rows = []
    for patch, error in schema_cases(child):
        for mask in range(1 << len(child["required_fields"])):
            raw = deepcopy(child["defaults"])
            raw.update(patch)
            for index, field in enumerate(child["required_fields"]):
                raw[field] = "" if mask & (1 << index) else child["label_values"][field]
            missing = next((field for field in child["required_fields"] if raw[field] == ""),None)
            rows.append((raw,"empty " + missing if missing else error))
    return rows


def parent_cases(record):
    child = record["child"]
    rows = []
    for raw, error in child_cases(child):
        if record["type"] == "SmallCategoryShell":
            for claimed in (False,True):
                patch = {"label":"C","claims_small":claimed,record["child_field"]:raw}
                failure = error if claimed else "claims_small must be true for SmallCategoryShell"
                rows.append((patch,failure))
        else:
            prefix = record["child_field"] + ": "
            rows.append(({record["child_field"]:raw},prefix + error if error else None))
    rows.extend(record.get("additional_cases", []))
    return rows


def product_cases(record):
    first, second = record["collection_schema"]
    first_field, second_field = first["field"], second["field"]
    rows = []
    for length in range(4):
        for supplied in range(4):
            patch = {first_field:inventory(first,length),second_field:inventory(second,supplied)}
            error = record["empty_inventory"] if length == 0 else record["alignment_error"] if supplied not in (0,length) else None
            rows.append((patch,error))
            for group, size in [(first,length),(second,supplied)]:
                for index in range(size):
                    bad = deepcopy(patch)
                    bad[group["field"]] = invalidate(group,bad[group["field"]],index,1)
                    failure = record["empty_inventory"] if length == 0 else group["diagnostic"].format(i=index)
                    rows.append((bad,failure))
            if length and supplied:
                bad = deepcopy(patch)
                for group in (first,second):
                    bad[group["field"]] = invalidate(group,bad[group["field"]],0,1)
                rows.append((bad,first["diagnostic"].format(i=0)))
    return rows


def challenge(record):
    if record["mode"] == "collection":
        return collection_challenge(record)
    if record["mode"] == "dual-cone":
        blocks = []
        for child in record["types"]:
            blocks.append(collection_challenge(child).replace("mod parameter_challenge", "mod challenge_" + child["type"]))
        blocks.append(r'''
#[cfg(test)] mod context_error_challenge {
    use super::*;
    #[test] fn every_typed_variant_preserves_its_payload_and_shape_location() {
        for text in ["", "detail\0\u{03b1}"] {
            for location in ["cone", "cocone", "place\0"] {
                assert_eq!(shape_context(location,ArithmosError::InvalidShape(text.into())),
                    ArithmosError::InvalidShape(format!("{location}: {text}")));
                for error in [ArithmosError::LawViolation(text.into()),ArithmosError::PreconditionFailed(text.into())] {
                    assert_eq!(shape_context(location,error.clone()),error);
                }
            }
        }
    }
}
''')
        return "\n".join(blocks)
    cases = parent_cases(record) if record["mode"] == "parent" else product_cases(record)
    return parameter_challenge(dict(record,parameter_cases=cases))


def impl_block(source, owner):
    return loop_block(source,"impl " + owner + " {")


def variants(record, source):
    if record["mode"] == "collection":
        return collection_variants(record,source)
    if record["mode"] == "parent":
        return parameter_variants(record,source)
    if record["mode"] == "product":
        return collection_variants(record,source)
    rows = []
    for child in record["types"]:
        block = impl_block(source,child["type"])
        for name, candidate, needle, replacement in collection_variants(child,block):
            rows.append((child["type"] + "-" + name,source.replace(block,candidate,1),needle,replacement))
    for name, needle, replacement in record["faults"]:
        if source.count(needle) != 1:
            raise ValueError("Nonunique context fault: " + name)
        rows.append((name,source.replace(needle,replacement,1),needle,replacement))
    return rows

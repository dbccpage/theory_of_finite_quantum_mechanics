"""Independent literal-inventory specifications and designated loop faults.

Expected cases use the explicit policy schema, never source guard extraction.
Source loop extraction is used only to place one independently dispatched fault.
"""
from copy import deepcopy
import re

from parameter_metadata import challenge as parameter_challenge
from parameter_metadata import variants as parameter_variants


def valid_entry(group, index):
    fields = group["fields"]
    if group["kind"] == "strings":
        return "entry:" + str(index) + ":\u03b1\0"
    if group["kind"] == "records":
        return {field:field + ":" + str(index) for field in fields}
    return [field + ":" + str(index) for field in fields]


def inventory(group, length):
    if group["kind"] == "map":
        return {"key:" + str(i):"value:" + str(i) for i in range(length)}
    return [valid_entry(group,i) for i in range(length)]


def invalidate(group, collection, index, mask):
    collection = deepcopy(collection)
    if group["kind"] == "map":
        key = list(collection)[index]
        value = collection.pop(key)
        collection["" if mask & 1 else key] = "" if mask & 2 else value
    elif group["kind"] == "strings":
        collection[index] = ""
    else:
        for bit, field in enumerate(group["fields"]):
            if mask & (1 << bit):
                collection[index][field if group["kind"] == "records" else bit] = ""
    return collection


def schema_cases(record):
    groups = record["collection_schema"]
    cases = []
    for length in (0,1,3):
        cases.append(({g["field"]:inventory(g,length) for g in groups},None))
    full = {g["field"]:inventory(g,3) for g in groups}
    for group in groups:
        for index in range(3):
            for mask in range(1,1 << len(group["fields"])):
                patch = deepcopy(full)
                patch[group["field"]] = invalidate(group,patch[group["field"]],index,mask)
                cases.append((patch,group["diagnostic"].format(i=index)))
        # A later second invalid entry must not replace the first failure.
        if group["kind"] != "map":
            patch = deepcopy(full)
            for index in (1,2):
                patch[group["field"]] = invalidate(group,patch[group["field"]],index,1)
            cases.append((patch,group["diagnostic"].format(i=1)))
    if len(groups) > 1:
        patch = deepcopy(full)
        for group in groups:
            patch[group["field"]] = invalidate(group,patch[group["field"]],1,1)
        cases.append((patch,groups[0]["diagnostic"].format(i=1)))
    return cases


def challenge(record):
    expanded = dict(record,parameter_cases=schema_cases(record))
    return parameter_challenge(expanded)


def loop_block(source, marker):
    if source.count(marker) != 1:
        raise ValueError("Nonunique designated loop: " + marker)
    start = source.index(marker)
    end = source.index("{",start)+1
    depth = 1
    while depth:
        depth += (source[end] == "{") - (source[end] == "}")
        end += 1
    return source[start:end]


def variants(record, source):
    rows = parameter_variants(dict(record,faults=record.get("faults",[])),source)
    for group in record["collection_schema"]:
        block = loop_block(source,group["loop"])
        replacements = [("skip-inventory","")]
        for index, operand in enumerate(group["source_operands"]):
            if block.count(operand) != 1:
                raise ValueError("Nonunique designated element guard: " + operand)
            replacements.append(("skip-component-" + str(index),block.replace(operand,"false",1)))
        literal = '"' + group["diagnostic"] + '"'
        if block.count(literal) != 1:
            raise ValueError("Nonunique designated collection diagnostic")
        replacements.append(("diagnostic",block.replace(literal,'"wrong collection diagnostic"',1)))
        needle = "&self." + group["field"] if group["kind"] == "map" else "self." + group["field"] + ".iter()"
        replacement = "self." + group["field"] + ".iter().skip(1)"
        if block.count(needle) != 1:
            raise ValueError("Nonunique designated collection iteration")
        replacements.append(("skip-first-entry",block.replace(needle,replacement,1)))
        for name, candidate in replacements:
            rows.append((group["field"] + "-" + name,source.replace(block,candidate,1),block,candidate))
    return rows

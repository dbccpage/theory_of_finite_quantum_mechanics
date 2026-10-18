"""Verifier-owned packet/router loop for the isolated OESOS laboratory."""

from __future__ import annotations


import ast
import copy
import dataclasses
import dis
import inspect
import math
import os
import platform
import sys
import textwrap
import types
from dataclasses import field
from dataclasses import dataclass
from typing import Any, Iterable

from omega_engine_pfp.domain.shared_kernel.canonical import domain_digest, freeze
from omega_engine.crates.operator.projector.proj_symbol_game import (
    CandidateSolver,
    DdaLetter,
    ProjectionReceipt,
    RuntimeProblem,
    SolverManifest,
    TerminalStatus,
)
from omega_engine_pfp.domain.entities.obstruction import (
    ObstructionLedger,
    ObstructionLedgerEvent,
    ProcessEvent,
    ProcessEventLog,
    verify_event_chain,
)
from omega_engine_pfp.domain.entities.candidate_artifact import (
    CANDIDATE_SCHEMA,
    CandidateArtifactV1,
)
from omega_engine_pfp.domain.entities.packet_envelope import (
    AttemptEvidenceV1,
    EvaluationReceiptV1,
    PACKET_SCHEMA,
)


TERMINALIZER_ID = "oesos-lab-proposal-terminalizer-v2"


def _is_sha256(value: str | None) -> bool:
    return bool(
        value
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _solver_fingerprint(solver: CandidateSolver) -> str:
    """Bind a registered solver's implementation source and initial config."""

    try:
        implementation_source = inspect.getsource(type(solver))
    except (OSError, TypeError) as exc:
        raise ValueError(
            f"solver source is not inspectable: {type(solver).__qualname__}"
        ) from exc
    if dataclasses.is_dataclass(solver):
        config = {
            item.name: getattr(solver, item.name)
            for item in dataclasses.fields(solver)
            if item.name != "manifest"
        }
    else:
        config = dict(vars(solver))
    return domain_digest(
        "omega.oesos.solver-implementation.v1",
        {
            "module": type(solver).__module__,
            "qualname": type(solver).__qualname__,
            "source": implementation_source,
            "config": config,
            "manifest_id": solver.manifest.manifest_id,
        },
    )


def _runtime_environment_digest() -> str:
    return domain_digest(
        "omega.oesos.python-runtime-environment.v1",
        {
            "implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "python_executable": os.path.realpath(sys.executable),
            "cache_tag": sys.implementation.cache_tag or "",
            "hash_randomization": sys.flags.hash_randomization,
            "platform": sys.platform,
            "byteorder": sys.byteorder,
            "python_hash_seed": os.environ.get("PYTHONHASHSEED", "<unset>"),
            "lang": os.environ.get("LANG", "<unset>"),
            "lc_all": os.environ.get("LC_ALL", "<unset>"),
            "timezone": os.environ.get("TZ", "<unset>"),
        },
    )


def _canonical_binding(value: Any) -> tuple[Any, bool]:
    try:
        return freeze(value), True
    except Exception:
        return (
            {
                "module": type(value).__module__,
                "qualname": type(value).__qualname__,
            },
            False,
        )


_STRUCTURAL_CLASS_NAMES = frozenset(
    {
        "__module__",
        "__doc__",
        "__dict__",
        "__weakref__",
        "__annotations__",
        "__dataclass_fields__",
        "__dataclass_params__",
        "__match_args__",
        "__slots__",
        "__slotnames__",
        "__hash__",
        "__firstlineno__",
        "__static_attributes__",
    }
)
_SAFE_BUILTINS = frozenset(
    {
        "abs",
        "all",
        "any",
        "bool",
        "bytes",
        "dict",
        "enumerate",
        "Exception",
        "float",
        "frozenset",
        "int",
        "isinstance",
        "issubclass",
        "len",
        "list",
        "max",
        "min",
        "object",
        "range",
        "reversed",
        "set",
        "sorted",
        "str",
        "sum",
        "super",
        "tuple",
        "type",
        "TypeError",
        "ValueError",
        "zip",
    }
)
_AMBIENT_BUILTINS = frozenset(
    {
        "__import__",
        "breakpoint",
        "compile",
        "delattr",
        "dir",
        "eval",
        "exec",
        "getattr",
        "globals",
        "hasattr",
        "help",
        "input",
        "locals",
        "memoryview",
        "open",
        "setattr",
        "vars",
    }
)
_TRUSTED_PURE_MODULES = frozenset(
    {
        "_collections_abc",
        "collections",
        "collections.abc",
        "dataclasses",
        "enum",
        "fractions",
        "hashlib",
        "json",
        "math",
    }
)
_TRUSTED_PASSIVE_CONSTRUCTORS = frozenset(
    {
        "symbol_game.contracts.SolverProposal",
        "symbol_game.packets.CandidateArtifactV1",
    }
)


def _is_deeply_immutable(value: Any) -> bool:
    if value is None or isinstance(value, (str, bool, int, float, bytes)):
        return True
    if isinstance(value, tuple):
        return all(_is_deeply_immutable(item) for item in value)
    if isinstance(value, frozenset):
        return all(_is_deeply_immutable(item) for item in value)
    if isinstance(value, SolverManifest):
        return True
    return dataclasses.is_dataclass(value) and bool(
        getattr(type(value), "__dataclass_params__", None).frozen
    )


def _code_identity(code: types.CodeType) -> Any:
    constants: list[Any] = []
    for constant in code.co_consts:
        if isinstance(constant, types.CodeType):
            constants.append(("nested-code", _code_identity(constant)))
            continue
        bound, canonical = _canonical_binding(constant)
        constants.append(
            ("constant", bound)
            if canonical
            else (
                "uncanonical-constant-type",
                type(constant).__module__,
                type(constant).__qualname__,
            )
        )
    return {
        "bytecode": code.co_code,
        "constants": tuple(constants),
        "names": code.co_names,
        "varnames": code.co_varnames,
        "freevars": code.co_freevars,
        "cellvars": code.co_cellvars,
        "argcount": code.co_argcount,
        "posonlyargcount": code.co_posonlyargcount,
        "kwonlyargcount": code.co_kwonlyargcount,
        "flags": code.co_flags,
    }


class _CallableDependencyScanner:
    def __init__(self, root_solver: CandidateSolver) -> None:
        self.dependencies: dict[str, tuple[str, str]] = {}
        self.execution_state: dict[str, Any] = {}
        self.findings: set[str] = set()
        self._root_solver = root_solver
        self._visited_callables: set[int] = set()
        self._visited_classes: set[int] = set()
        self._visited_class_entries: set[int] = set()

    def _bind_state(
        self,
        label: str,
        value: Any,
        *,
        finding: str | None = None,
    ) -> None:
        bound, canonical = _canonical_binding(value)
        self.execution_state[label] = bound
        if finding is not None:
            self.findings.add(finding)
        if not canonical:
            self.findings.add(f"uncanonical-execution-binding:{label}")

    def _record_dependency(
        self,
        label: str,
        kind: str,
        identity: Any,
    ) -> None:
        self.dependencies[label] = (
            kind,
            domain_digest("omega.oesos.callable-dependency.v1", identity),
        )

    @staticmethod
    def _loaded_globals(
        function: types.FunctionType,
    ) -> tuple[tuple[str, str | None], ...]:
        try:
            instructions = tuple(dis.get_instructions(function))
        except (TypeError, ValueError):
            return ()
        loaded: list[tuple[str, str | None]] = []
        for index, instruction in enumerate(instructions):
            if instruction.opname not in {
                "LOAD_GLOBAL",
                "LOAD_NAME",
                "LOAD_FROM_DICT_OR_GLOBALS",
            }:
                continue
            name = instruction.argval
            if not isinstance(name, str):
                continue
            attribute: str | None = None
            if index + 1 < len(instructions):
                successor = instructions[index + 1]
                if successor.opname in {"LOAD_ATTR", "LOAD_METHOD"} and isinstance(
                    successor.argval, str
                ):
                    attribute = successor.argval
            loaded.append((name, attribute))
        return tuple(loaded)

    @staticmethod
    def _direct_call_names(function: types.FunctionType) -> frozenset[str]:
        try:
            tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
        except (OSError, TypeError, SyntaxError, IndentationError):
            return frozenset()
        return frozenset(
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        )

    @staticmethod
    def _owner_attribute_edges(
        function: types.FunctionType,
    ) -> tuple[tuple[str, tuple[str, ...]], ...]:
        try:
            instructions = tuple(dis.get_instructions(function))
        except (TypeError, ValueError):
            return ()
        parameter_names = function.__code__.co_varnames[: function.__code__.co_argcount]
        if not parameter_names or parameter_names[0] not in {"self", "cls"}:
            return ()
        owner_parameter = parameter_names[0]
        edges: list[tuple[str, tuple[str, ...]]] = []
        for index, instruction in enumerate(instructions):
            if (
                instruction.opname not in {"LOAD_FAST", "LOAD_FAST_BORROW"}
                or instruction.argval != owner_parameter
            ):
                continue
            chain: list[str] = []
            for successor in instructions[index + 1 :]:
                if successor.opname not in {"LOAD_ATTR", "LOAD_METHOD"}:
                    break
                if not isinstance(successor.argval, str):
                    break
                chain.append(successor.argval)
            if chain:
                edges.append((owner_parameter, tuple(chain)))
        return tuple(edges)

    def scan_solver_class_state(self, solver_type: type[Any]) -> None:
        for owner in reversed(solver_type.__mro__[:-1]):
            for name, value in sorted(vars(owner).items()):
                if name in _STRUCTURAL_CLASS_NAMES or name == "manifest":
                    continue
                if (
                    inspect.isroutine(value)
                    or isinstance(value, (property, staticmethod, classmethod))
                    or inspect.ismemberdescriptor(value)
                    or inspect.isdatadescriptor(value)
                ):
                    continue
                label = f"{owner.__module__}.{owner.__qualname__}.{name}"
                self._bind_state(
                    label,
                    value,
                    finding=f"unisolated-class-binding:{label}",
                )

    def scan_callable(
        self,
        value: Any,
        path: str,
        *,
        owner_class: type[Any] | None = None,
        method_name: str | None = None,
    ) -> None:
        if inspect.ismethod(value):
            bound_self = value.__self__
            if bound_self is not None and not inspect.isclass(bound_self):
                self._bind_state(
                    f"{path}:bound-self",
                    bound_self,
                    finding=f"unisolated-bound-method-state:{path}",
                )
            self.scan_callable(
                value.__func__,
                path,
                owner_class=owner_class,
                method_name=method_name,
            )
            return
        if inspect.isfunction(value):
            self._scan_function(
                value,
                path,
                owner_class=owner_class,
                method_name=method_name,
            )
            return
        if inspect.isclass(value):
            self._scan_class(value, path, invoked=True)
            return
        if inspect.isbuiltin(value):
            module_name = str(getattr(value, "__module__", "builtins"))
            name = str(getattr(value, "__qualname__", getattr(value, "__name__", path)))
            self._record_dependency(
                path,
                "builtin-callable",
                {
                    "module": module_name,
                    "qualname": name,
                    "runtime": _runtime_environment_digest(),
                },
            )
            if module_name not in _TRUSTED_PURE_MODULES and module_name != "builtins":
                self.findings.add(f"unreviewed-builtin-callable:{path}")
            return
        if callable(value):
            if type(value).__module__ == "typing":
                self._record_dependency(
                    path,
                    "typing-runtime-token",
                    {
                        "type": type(value).__qualname__,
                        "value": str(value),
                        "runtime": _runtime_environment_digest(),
                    },
                )
                return
            if id(value) in self._visited_callables:
                return
            self._visited_callables.add(id(value))
            self._bind_state(
                f"{path}:callable-object",
                getattr(value, "__dict__", value),
                finding=f"unisolated-callable-object:{path}",
            )
            call_method = getattr(type(value), "__call__", None)
            if call_method is None:
                self.findings.add(f"unresolved-callable-edge:{path}")
            else:
                self.scan_callable(
                    call_method,
                    f"{path}.__call__",
                    owner_class=type(value),
                    method_name="__call__",
                )
            return
        self.findings.add(f"unresolved-dynamic-callable:{path}")

    def _scan_function(
        self,
        function: types.FunctionType,
        path: str,
        *,
        owner_class: type[Any] | None,
        method_name: str | None,
    ) -> None:
        if id(function) in self._visited_callables:
            return
        self._visited_callables.add(id(function))
        code = function.__code__
        try:
            source = inspect.getsource(function)
        except (OSError, TypeError):
            source = ""
            self.findings.add(f"uninspectable-code-dependency:{path}")
        self._record_dependency(
            path,
            "python-function",
            {
                "module": function.__module__,
                "qualname": function.__qualname__,
                "source": source,
                "code": _code_identity(code),
            },
        )
        try:
            instructions = tuple(dis.get_instructions(function))
        except (TypeError, ValueError):
            instructions = ()
            self.findings.add(f"uninspectable-bytecode:{path}")
        for instruction in instructions:
            if instruction.opname in {"IMPORT_NAME", "IMPORT_FROM"}:
                self.findings.add(f"runtime-import-edge:{path}:{instruction.argval}")
        for constant in code.co_consts:
            if isinstance(constant, types.CodeType):
                self.findings.add(
                    f"nested-executable-code:{path}:{constant.co_qualname}"
                )

        defaults = function.__defaults__ or ()
        for index, default in enumerate(defaults):
            label = f"{path}:default:{index}"
            self._bind_state(
                label,
                default,
                finding=(
                    None
                    if _is_deeply_immutable(default)
                    else f"mutable-callable-default:{label}"
                ),
            )
        for name, default in sorted((function.__kwdefaults__ or {}).items()):
            label = f"{path}:kwdefault:{name}"
            self._bind_state(
                label,
                default,
                finding=(
                    None
                    if _is_deeply_immutable(default)
                    else f"mutable-callable-default:{label}"
                ),
            )
        for name, attribute in sorted(vars(function).items()):
            self._bind_state(
                f"{path}:function-attribute:{name}",
                attribute,
                finding=f"unisolated-function-attribute:{path}:{name}",
            )
        closure = function.__closure__ or ()
        for freevar, cell in zip(code.co_freevars, closure):
            label = f"{path}:closure:{freevar}"
            try:
                cell_value = cell.cell_contents
            except ValueError:
                self.findings.add(f"empty-closure-cell:{label}")
                continue
            if freevar == "__class__" and inspect.isclass(cell_value):
                self._scan_class(cell_value, label, invoked=False)
                continue
            self._bind_state(
                label,
                cell_value,
                finding=f"unisolated-closure-binding:{label}",
            )
            if callable(cell_value):
                self.scan_callable(cell_value, f"{label}:callable")

        loaded_globals = self._loaded_globals(function)
        direct_call_names = self._direct_call_names(function)
        globals_map = function.__globals__
        for name, attribute in loaded_globals:
            dependency_path = f"{path}:global:{name}"
            if name not in globals_map:
                if name == "super":
                    self._scan_super_edge(owner_class, method_name, dependency_path)
                    continue
                if name in _AMBIENT_BUILTINS:
                    self.findings.add(f"ambient-reflective-builtin:{dependency_path}")
                    continue
                if name in _SAFE_BUILTINS:
                    self._record_dependency(
                        dependency_path,
                        "safe-builtin",
                        {"name": name, "runtime": _runtime_environment_digest()},
                    )
                    continue
                self.findings.add(f"unresolved-global-edge:{dependency_path}")
                continue
            global_value = globals_map[name]
            if inspect.ismodule(global_value):
                self._scan_module_dependency(
                    global_value,
                    dependency_path,
                    attribute,
                )
            elif inspect.isclass(global_value):
                self._scan_class(
                    global_value,
                    dependency_path,
                    invoked=name in direct_call_names,
                )
                if attribute is not None:
                    self._scan_static_attribute(
                        global_value,
                        attribute,
                        dependency_path,
                    )
            elif callable(global_value):
                self.scan_callable(global_value, dependency_path)
            else:
                self._bind_state(
                    dependency_path,
                    global_value,
                    finding=f"unisolated-module-binding:{dependency_path}",
                )
        if owner_class is not None:
            for owner_parameter, edge in self._owner_attribute_edges(function):
                self._scan_owner_attribute_chain(
                    owner_class,
                    owner_parameter,
                    edge,
                    path,
                )
        loaded_names = {name for name, _ in loaded_globals}
        if "type" in loaded_names:
            reflective_names = {
                "__bases__",
                "__class__",
                "__dict__",
                "__getattribute__",
                "__mro__",
                "__subclasses__",
            }
            code_names = set(function.__code__.co_names)
            for reflective_name in sorted(reflective_names & code_names):
                self.findings.add(
                    f"reflective-owner-access:{path}:type(self).{reflective_name}"
                )

    def _scan_super_edge(
        self,
        owner_class: type[Any] | None,
        method_name: str | None,
        path: str,
    ) -> None:
        if owner_class is None or method_name is None:
            self.findings.add(f"unresolved-super-edge:{path}")
            return
        try:
            owner_index = owner_class.__mro__.index(owner_class)
        except ValueError:
            self.findings.add(f"unresolved-super-edge:{path}")
            return
        for parent in owner_class.__mro__[owner_index + 1 :]:
            if method_name not in vars(parent):
                continue
            raw = inspect.getattr_static(parent, method_name)
            if isinstance(raw, (staticmethod, classmethod)):
                raw = raw.__func__
            self.scan_callable(
                raw,
                f"{path}:{parent.__module__}.{parent.__qualname__}.{method_name}",
                owner_class=parent,
                method_name=method_name,
            )
            return
        self.findings.add(f"unresolved-super-edge:{path}")

    def _scan_module_dependency(
        self,
        module: types.ModuleType,
        path: str,
        attribute: str | None,
    ) -> None:
        module_name = module.__name__
        version = str(getattr(module, "__version__", "<runtime-bound>"))
        self._record_dependency(
            path,
            "module",
            {
                "name": module_name,
                "version": version,
                "runtime": _runtime_environment_digest(),
            },
        )
        trusted = module_name in _TRUSTED_PURE_MODULES
        if not trusted:
            self.findings.add(f"ambient-module-dependency:{path}")
        if attribute is None:
            return
        if not hasattr(module, attribute):
            self.findings.add(f"unresolved-module-attribute:{path}.{attribute}")
            return
        member = getattr(module, attribute)
        member_path = f"{path}.{attribute}"
        if trusted:
            if inspect.isfunction(member) or inspect.ismethod(member):
                self.scan_callable(member, member_path)
            elif inspect.isbuiltin(member):
                self._record_dependency(
                    member_path,
                    "trusted-module-callable",
                    {
                        "module": module_name,
                        "attribute": attribute,
                        "runtime": _runtime_environment_digest(),
                    },
                )
            elif callable(member):
                self.scan_callable(member, member_path)
            else:
                self._bind_state(member_path, member)
            return
        if callable(member):
            self.scan_callable(member, member_path)
        else:
            self._bind_state(
                member_path,
                member,
                finding=f"unisolated-module-binding:{member_path}",
            )

    def _scan_class(
        self,
        cls: type[Any],
        path: str,
        *,
        invoked: bool = False,
    ) -> None:
        if id(cls) in self._visited_classes:
            if invoked:
                self._scan_class_entry(cls, path)
            return
        self._visited_classes.add(id(cls))
        if cls.__module__ == "builtins":
            if cls.__name__ not in _SAFE_BUILTINS:
                self.findings.add(f"unreviewed-builtin-class:{path}")
            self._record_dependency(
                path,
                "builtin-class",
                {
                    "qualname": cls.__qualname__,
                    "runtime": _runtime_environment_digest(),
                },
            )
            return
        mro_identity: list[tuple[str, str, str]] = []
        for owner in cls.__mro__[:-1]:
            try:
                source = inspect.getsource(owner)
            except (OSError, TypeError):
                source = ""
                if owner.__module__.split(".", 1)[0] not in sys.stdlib_module_names:
                    self.findings.add(
                        f"uninspectable-class-dependency:{path}:{owner.__qualname__}"
                    )
            mro_identity.append((owner.__module__, owner.__qualname__, source))
        self._record_dependency(path, "python-class", tuple(mro_identity))

        if cls.__module__.split(".", 1)[0] in sys.stdlib_module_names:
            return

        for name, member in sorted(vars(cls).items()):
            if name in _STRUCTURAL_CLASS_NAMES or name == "manifest":
                continue
            if (
                inspect.isroutine(member)
                or isinstance(member, (property, staticmethod, classmethod))
                or inspect.ismemberdescriptor(member)
                or inspect.isdatadescriptor(member)
            ):
                continue
            label = f"{path}:class-binding:{name}"
            self._bind_state(
                label,
                member,
                finding=f"unisolated-class-binding:{label}",
            )
        if invoked:
            self._scan_class_entry(cls, path)

    def _scan_class_entry(self, cls: type[Any], path: str) -> None:
        if id(cls) in self._visited_class_entries:
            return
        self._visited_class_entries.add(id(cls))
        class_identity = f"{cls.__module__}.{cls.__qualname__}"
        if class_identity in _TRUSTED_PASSIVE_CONSTRUCTORS:
            self._record_dependency(
                f"{path}:trusted-constructor",
                "trusted-passive-constructor",
                {"class": class_identity, "runtime": _runtime_environment_digest()},
            )
            return
        scanned_entry = False
        for entry_name in ("__new__", "__init__", "__post_init__"):
            if entry_name not in vars(cls):
                continue
            raw = inspect.getattr_static(cls, entry_name)
            if isinstance(raw, (staticmethod, classmethod)):
                raw = raw.__func__
            if (
                entry_name == "__init__"
                and dataclasses.is_dataclass(cls)
                and getattr(getattr(raw, "__code__", None), "co_filename", "")
                == "<string>"
            ):
                continue
            scanned_entry = True
            self.scan_callable(
                raw,
                f"{path}.{entry_name}",
                owner_class=cls,
                method_name=entry_name,
            )
        if not scanned_entry:
            self.findings.add(f"unresolved-class-call-edge:{path}")

    def _scan_owner_attribute_chain(
        self,
        owner: type[Any],
        owner_parameter: str,
        chain: tuple[str, ...],
        path: str,
    ) -> None:
        reflective_names = {
            "__bases__",
            "__class__",
            "__dict__",
            "__getattribute__",
            "__mro__",
            "__subclasses__",
        }
        current: Any = owner if owner_parameter == "cls" else self._root_solver
        for index, attribute in enumerate(chain):
            member_path = f"{path}:owner:{'.'.join(chain[: index + 1])}"
            if attribute in reflective_names:
                self.findings.add(f"reflective-owner-access:{member_path}")
                return
            try:
                instance_values = vars(current)
            except TypeError:
                instance_values = {}
            if not inspect.isclass(current) and attribute in instance_values:
                current = instance_values[attribute]
                self._bind_state(member_path, current)
                if callable(current):
                    self.scan_callable(current, f"{member_path}:callable")
                    if index + 1 < len(chain):
                        self.findings.add(
                            f"unresolved-callable-result-chain:{member_path}"
                        )
                        return
                continue
            try:
                member = inspect.getattr_static(current, attribute)
            except AttributeError:
                self.findings.add(f"unresolved-owner-attribute:{member_path}")
                return
            current_type = current if inspect.isclass(current) else type(current)
            if isinstance(member, (staticmethod, classmethod)):
                member = member.__func__
            if isinstance(member, property):
                if member.fget is None:
                    self.findings.add(f"unresolved-property-edge:{member_path}")
                else:
                    self.scan_callable(
                        member.fget,
                        f"{member_path}.fget",
                        owner_class=current_type,
                        method_name=attribute,
                    )
                if index + 1 < len(chain):
                    self.findings.add(f"unresolved-property-result:{member_path}")
                return
            if inspect.isfunction(member) or inspect.ismethod(member):
                defining_owner = next(
                    (
                        candidate
                        for candidate in current_type.__mro__
                        if attribute in vars(candidate)
                    ),
                    current_type,
                )
                self.scan_callable(
                    member,
                    member_path,
                    owner_class=defining_owner,
                    method_name=attribute,
                )
                if index + 1 < len(chain):
                    self.findings.add(f"unresolved-callable-result-chain:{member_path}")
                return
            if isinstance(
                member,
                (types.MemberDescriptorType, types.GetSetDescriptorType),
            ):
                self._record_dependency(
                    member_path,
                    "factory-bound-member-descriptor",
                    {
                        "owner": current_type.__qualname__,
                        "attribute": attribute,
                        "runtime": _runtime_environment_digest(),
                    },
                )
                try:
                    current = member.__get__(current, current_type)
                except Exception:
                    self.findings.add(f"unresolved-member-descriptor:{member_path}")
                    return
                self._bind_state(member_path, current)
                continue
            descriptor_get = inspect.getattr_static(type(member), "__get__", None)
            if descriptor_get is not None:
                self.findings.add(f"custom-owner-descriptor:{member_path}")
                self.scan_callable(
                    descriptor_get,
                    f"{member_path}.__get__",
                    owner_class=type(member),
                    method_name="__get__",
                )
                return
            current = member
            self._bind_state(
                member_path,
                current,
                finding=(
                    None
                    if attribute == "manifest" and isinstance(current, SolverManifest)
                    else f"unisolated-class-binding:{member_path}"
                ),
            )

    def _scan_static_attribute(
        self,
        owner: type[Any],
        attribute: str,
        path: str,
    ) -> None:
        defining_owner = next(
            (candidate for candidate in owner.__mro__ if attribute in vars(candidate)),
            owner,
        )
        try:
            member = inspect.getattr_static(defining_owner, attribute)
        except AttributeError:
            self.findings.add(f"unresolved-class-attribute:{path}.{attribute}")
            return
        if isinstance(member, (staticmethod, classmethod)):
            member = member.__func__
        member_path = f"{path}.{attribute}"
        if isinstance(member, property):
            if member.fget is None:
                self.findings.add(f"unresolved-property-edge:{member_path}")
            else:
                self.scan_callable(
                    member.fget,
                    f"{member_path}.fget",
                    owner_class=defining_owner,
                    method_name=attribute,
                )
        elif callable(member):
            self.scan_callable(
                member,
                member_path,
                owner_class=defining_owner,
                method_name=attribute,
            )
        elif not inspect.isdatadescriptor(member):
            self._bind_state(
                member_path,
                member,
                finding=f"unisolated-class-binding:{member_path}",
            )


def _solver_execution_profile(
    solver: CandidateSolver,
) -> tuple[str, str, tuple[str, ...]]:
    solver_type = type(solver)
    scanner = _CallableDependencyScanner(solver)
    scanner.scan_solver_class_state(solver_type)
    owner = next(
        (
            candidate
            for candidate in solver_type.__mro__
            if "propose" in vars(candidate)
        ),
        None,
    )
    if owner is None:
        scanner.findings.add("unresolved-solver-propose-edge")
    else:
        raw_propose = inspect.getattr_static(owner, "propose")
        if isinstance(raw_propose, (staticmethod, classmethod)):
            raw_propose = raw_propose.__func__
        scanner.scan_callable(
            raw_propose,
            f"{owner.__module__}.{owner.__qualname__}.propose",
            owner_class=owner,
            method_name="propose",
        )

    dependency_digest = domain_digest(
        "omega.oesos.solver-dependencies.v1",
        tuple(sorted(scanner.dependencies.items())),
    )
    execution_state_digest = domain_digest(
        "omega.oesos.solver-execution-state.v1",
        tuple(sorted(scanner.execution_state.items())),
    )
    return (
        dependency_digest,
        execution_state_digest,
        tuple(sorted(scanner.findings)),
    )


def _constructor_recipe(
    solver: CandidateSolver,
) -> tuple[str, dict[str, Any]]:
    if dataclasses.is_dataclass(solver):
        return (
            "dataclass-init",
            {
                item.name: copy.deepcopy(getattr(solver, item.name))
                for item in dataclasses.fields(solver)
                if item.init
            },
        )
    try:
        signature = inspect.signature(type(solver))
    except (TypeError, ValueError):
        return "snapshot-copy", {}
    instance_values = vars(solver)
    kwargs: dict[str, Any] = {}
    for name, parameter in signature.parameters.items():
        if parameter.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue
        if name in instance_values:
            kwargs[name] = copy.deepcopy(instance_values[name])
        elif parameter.default is inspect.Parameter.empty:
            return "snapshot-copy", {}
    try:
        candidate = type(solver)(**copy.deepcopy(kwargs))
    except Exception:
        return "snapshot-copy", {}
    if _solver_fingerprint(candidate) != _solver_fingerprint(solver):
        return "snapshot-copy", {}
    return "constructor-init", kwargs


@dataclass(frozen=True, slots=True)
class SolverFactoryV1:
    solver_id: str
    manifest_id: str
    executable_config_digest: str
    dependency_digest: str
    execution_state_digest: str
    runtime_environment_digest: str
    seed_policy: str
    construction_mode: str
    isolation_findings: tuple[str, ...]
    _prototype: CandidateSolver = field(repr=False, compare=False)
    _constructor_kwargs: dict[str, Any] = field(repr=False, compare=False)

    @classmethod
    def from_solver(cls, solver: CandidateSolver) -> "SolverFactoryV1":
        prototype = copy.deepcopy(solver)
        construction_mode, constructor_kwargs = _constructor_recipe(prototype)
        dependency_digest, execution_state_digest, findings = _solver_execution_profile(
            prototype
        )
        if construction_mode == "snapshot-copy":
            findings = (*findings, "snapshot-copy-construction")
        return cls(
            solver_id=prototype.manifest.solver_id,
            manifest_id=prototype.manifest.manifest_id,
            executable_config_digest=_solver_fingerprint(prototype),
            dependency_digest=dependency_digest,
            execution_state_digest=execution_state_digest,
            runtime_environment_digest=_runtime_environment_digest(),
            seed_policy="ambient-randomness-forbidden",
            construction_mode=construction_mode,
            isolation_findings=tuple(sorted(set(findings))),
            _prototype=prototype,
            _constructor_kwargs=constructor_kwargs,
        )

    @property
    def factory_id(self) -> str:
        return domain_digest(
            "omega.oesos.solver-factory.v1",
            {
                "solver_id": self.solver_id,
                "manifest_id": self.manifest_id,
                "executable_config_digest": self.executable_config_digest,
                "dependency_digest": self.dependency_digest,
                "execution_state_digest": self.execution_state_digest,
                "runtime_environment_digest": self.runtime_environment_digest,
                "seed_policy": self.seed_policy,
                "construction_mode": self.construction_mode,
                "isolation_findings": self.isolation_findings,
            },
        )

    @property
    def promotion_isolation_attested(self) -> bool:
        return not self.isolation_findings

    def current_identity_matches(self) -> bool:
        dependency_digest, execution_state_digest, _ = _solver_execution_profile(
            self._prototype
        )
        return (
            self._prototype.manifest.manifest_id == self.manifest_id
            and _solver_fingerprint(self._prototype) == self.executable_config_digest
            and dependency_digest == self.dependency_digest
            and execution_state_digest == self.execution_state_digest
            and _runtime_environment_digest() == self.runtime_environment_digest
        )

    def construct(self) -> CandidateSolver:
        if not self.current_identity_matches():
            raise ValueError(f"solver factory environment drift: {self.solver_id}")
        if self.construction_mode == "snapshot-copy":
            solver = copy.deepcopy(self._prototype)
        else:
            solver = type(self._prototype)(**copy.deepcopy(self._constructor_kwargs))
        if (
            solver.manifest.manifest_id != self.manifest_id
            or _solver_fingerprint(solver) != self.executable_config_digest
        ):
            raise ValueError(
                f"solver factory reconstruction mismatch: {self.solver_id}"
            )
        return solver


@dataclass(frozen=True, slots=True)
class Prime000ShapeReceipt:
    declarations: tuple[str, ...]
    blockers: tuple[str, ...]
    authority_effect: str = field(default="None")

    @property
    def accepted(self) -> bool:
        return not self.blockers


@dataclass(frozen=True, slots=True)
class Prime001ShapeReceipt:
    adapter_id: str
    source_carrier_id: str
    target_carrier_id: str
    sound: bool
    loss_ledger: tuple[str, ...]
    detail: str
    authority_effect: str = field(default="None")


@dataclass(frozen=True, slots=True)
class DetectorAdequacyReceipt:
    projector_id: str
    adequate: bool
    cases_checked: int
    failures: tuple[str, ...]
    authority_effect: str = field(default="None")


@dataclass(frozen=True, slots=True)
class LocalContinuationCheck:
    may_continue_locally: bool
    blockers: tuple[str, ...]
    authority_effect: str = field(default="None")


@dataclass(frozen=True, slots=True)
class SolverAttempt:
    solver_id: str
    candidate_id: str | None
    candidate_state_hash: str | None
    accepted: bool
    reason: str
    before_measure: tuple[float, float, int]
    after_measure: tuple[float, float, int] | None
    before_raw_mass: float | None
    after_raw_mass: float | None
    claimed_terminal: str | None = None
    candidate_payload_hash: str | None = None


def _run_evidence_digest(
    *,
    packet_id: str,
    runtime_id: str,
    solver_registry_hash: str,
    parent_event_id: str | None,
    prime000: Prime000ShapeReceipt,
    adapter: Prime001ShapeReceipt,
    detector: DetectorAdequacyReceipt,
    terminal_status: TerminalStatus,
    stop_reasons: tuple[str, ...],
    input_state_hash: str,
    output_state_hash: str,
    final_native_state: Any,
    final_projection: ProjectionReceipt | None,
    attempts: Iterable[SolverAttempt],
    candidate_artifacts: Iterable[CandidateArtifactV1],
    accepted_steps: int,
    obstruction_events: Iterable[ObstructionLedgerEvent],
    active_obstructions: tuple[str, ...],
    process_events: Iterable[ProcessEvent],
    authority_effect: str,
) -> str:
    """Commit every field that can affect local admission or replay."""

    return domain_digest(
        "omega.oesos.run-evidence.v1",
        {
            "terminalizer_id": TERMINALIZER_ID,
            "packet_id": packet_id,
            "runtime_id": runtime_id,
            "solver_registry_hash": solver_registry_hash,
            "parent_event_id": parent_event_id,
            "prime000": prime000,
            "adapter": adapter,
            "detector": detector,
            "terminal_status": terminal_status.value,
            "stop_reasons": stop_reasons,
            "input_state_hash": input_state_hash,
            "output_state_hash": output_state_hash,
            "final_native_state": final_native_state,
            "final_projection": final_projection,
            "attempts": tuple(attempts),
            "candidate_artifacts": tuple(candidate_artifacts),
            "accepted_steps": accepted_steps,
            "obstruction_events": tuple(obstruction_events),
            "active_obstructions": active_obstructions,
            "process_events": tuple(process_events),
            "authority_effect": authority_effect,
        },
    )


@dataclass(frozen=True, slots=True)
class RunReceipt:
    packet_id: str
    runtime_id: str
    solver_registry_hash: str
    parent_event_id: str | None
    prime000: Prime000ShapeReceipt
    adapter: Prime001ShapeReceipt
    detector: DetectorAdequacyReceipt
    terminal_status: TerminalStatus
    stop_reasons: tuple[str, ...]
    input_state_hash: str
    output_state_hash: str
    final_native_state: Any
    final_projection: ProjectionReceipt | None
    attempts: tuple[SolverAttempt, ...]
    candidate_artifacts: tuple[CandidateArtifactV1, ...]
    accepted_steps: int
    obstruction_events: tuple[ObstructionLedgerEvent, ...]
    active_obstructions: tuple[str, ...]
    process_events: tuple[ProcessEvent, ...]
    event_root: str
    authority_effect: str = field(default="None")

    def evidence_valid(self) -> bool:
        """Reconcile evidence, returning ``False`` for every malformed shape."""

        try:
            return self._evidence_valid_unchecked()
        except Exception:
            return False

    def _evidence_valid_unchecked(self) -> bool:
        """Validate the exact in-memory receipt algebra after type closure."""

        if (
            type(self.authority_effect) is not str
            or self.authority_effect != "None"
            or type(self.terminal_status) is not TerminalStatus
            or type(self.stop_reasons) is not tuple
            or any(type(reason) is not str for reason in self.stop_reasons)
            or type(self.attempts) is not tuple
            or type(self.candidate_artifacts) is not tuple
            or type(self.obstruction_events) is not tuple
            or type(self.active_obstructions) is not tuple
            or any(type(item) is not str for item in self.active_obstructions)
            or type(self.process_events) is not tuple
            or not self.process_events
            or type(self.accepted_steps) is not int
            or type(self.prime000) is not Prime000ShapeReceipt
            or type(self.adapter) is not Prime001ShapeReceipt
            or type(self.detector) is not DetectorAdequacyReceipt
            or (
                self.final_projection is not None
                and type(self.final_projection) is not ProjectionReceipt
            )
            or any(
                type(event) is not ObstructionLedgerEvent
                for event in self.obstruction_events
            )
            or any(type(event) is not ProcessEvent for event in self.process_events)
        ):
            return False
        if (
            type(self.prime000.declarations) is not tuple
            or type(self.prime000.blockers) is not tuple
            or any(type(item) is not str for item in self.prime000.declarations)
            or any(type(item) is not str for item in self.prime000.blockers)
            or type(self.prime000.authority_effect) is not str
            or type(self.adapter.adapter_id) is not str
            or type(self.adapter.source_carrier_id) is not str
            or type(self.adapter.target_carrier_id) is not str
            or type(self.adapter.sound) is not bool
            or type(self.adapter.loss_ledger) is not tuple
            or any(type(item) is not str for item in self.adapter.loss_ledger)
            or type(self.adapter.detail) is not str
            or type(self.adapter.authority_effect) is not str
            or type(self.detector.projector_id) is not str
            or type(self.detector.adequate) is not bool
            or type(self.detector.cases_checked) is not int
            or type(self.detector.failures) is not tuple
            or any(type(item) is not str for item in self.detector.failures)
            or type(self.detector.authority_effect) is not str
        ):
            return False
        if self.final_projection is not None and (
            type(self.final_projection.projector_id) is not str
            or type(self.final_projection.state_hash) is not str
            or type(self.final_projection.obstructions) is not tuple
            or type(self.final_projection.witness) is not str
            or type(self.final_projection.authority_effect) is not str
            or (
                self.final_projection.raw_mass is not None
                and (
                    type(self.final_projection.raw_mass) is not float
                    or not math.isfinite(self.final_projection.raw_mass)
                    or self.final_projection.raw_mass < 0.0
                )
            )
        ):
            return False
        if any(
            receipt.authority_effect != "None"
            for receipt in (self.prime000, self.adapter, self.detector)
        ):
            return False
        if any(
            type(value) is not str or not _is_sha256(value)
            for value in (
                self.packet_id,
                self.runtime_id,
                self.solver_registry_hash,
                self.input_state_hash,
                self.output_state_hash,
                self.event_root,
            )
        ):
            return False
        if self.parent_event_id is not None and (
            type(self.parent_event_id) is not str
            or not _is_sha256(self.parent_event_id)
        ):
            return False
        if any(
            type(event.sequence) is not int
            or type(event.event_type) is not str
            or type(event.dda_letter) is not str
            or type(event.input_state_hash) is not str
            or type(event.output_state_hash) is not str
            or (event.parent_hash is not None and type(event.parent_hash) is not str)
            or type(event.event_hash) is not str
            or type(event.authority_effect) is not str
            for event in self.process_events
        ):
            return False
        if not verify_event_chain(self.process_events, self.parent_event_id):
            return False
        if self.event_root != self.process_events[-1].event_hash:
            return False
        if self.process_events[0].event_type != "declare-carrier":
            return False
        if self.process_events[0].details != freeze(
            {"packet_id": self.packet_id, "runtime_id": self.runtime_id}
        ):
            return False
        terminal_event = self.process_events[-1]
        if terminal_event.event_type != "terminal" or terminal_event.dda_letter != "T":
            return False
        if (
            terminal_event.input_state_hash != self.output_state_hash
            or terminal_event.output_state_hash != self.output_state_hash
        ):
            return False
        if self.final_projection is not None:
            if self.final_projection.authority_effect != "None":
                return False
            if self.final_projection.state_hash != self.output_state_hash:
                return False
            if self.final_projection.active_ids != self.active_obstructions:
                return False
            if self.final_projection.projector_id != self.detector.projector_id:
                return False
        if any(
            type(attempt) is not SolverAttempt
            or type(attempt.solver_id) is not str
            or not attempt.solver_id
            or type(attempt.accepted) is not bool
            or type(attempt.reason) is not str
            or not attempt.reason
            or type(attempt.before_measure) is not tuple
            or len(attempt.before_measure) != 3
            or type(attempt.before_measure[0]) is not float
            or type(attempt.before_measure[1]) is not float
            or type(attempt.before_measure[2]) is not int
            or (
                attempt.before_raw_mass is not None
                and (
                    type(attempt.before_raw_mass) is not float
                    or not math.isfinite(attempt.before_raw_mass)
                    or attempt.before_raw_mass < 0.0
                )
            )
            or (
                attempt.after_raw_mass is not None
                and (
                    type(attempt.after_raw_mass) is not float
                    or not math.isfinite(attempt.after_raw_mass)
                    or attempt.after_raw_mass < 0.0
                )
            )
            or (
                attempt.after_measure is not None
                and (
                    type(attempt.after_measure) is not tuple
                    or len(attempt.after_measure) != 3
                    or type(attempt.after_measure[0]) is not float
                    or type(attempt.after_measure[1]) is not float
                    or type(attempt.after_measure[2]) is not int
                )
            )
            or (
                attempt.claimed_terminal is not None
                and type(attempt.claimed_terminal) is not str
            )
            or (
                attempt.candidate_id is not None
                and (
                    type(attempt.candidate_id) is not str
                    or not _is_sha256(attempt.candidate_id)
                )
            )
            or (
                attempt.candidate_state_hash is not None
                and (
                    type(attempt.candidate_state_hash) is not str
                    or not _is_sha256(attempt.candidate_state_hash)
                )
            )
            or (
                attempt.candidate_payload_hash is not None
                and (
                    type(attempt.candidate_payload_hash) is not str
                    or not _is_sha256(attempt.candidate_payload_hash)
                )
            )
            for attempt in self.attempts
        ):
            return False
        if self.accepted_steps != sum(attempt.accepted for attempt in self.attempts):
            return False
        if any(
            attempt.accepted
            and (
                attempt.candidate_id is None
                or attempt.candidate_state_hash is None
                or attempt.candidate_payload_hash is None
            )
            for attempt in self.attempts
        ):
            return False
        candidate_attempts = tuple(
            attempt for attempt in self.attempts if attempt.candidate_id is not None
        )
        if len(candidate_attempts) != len(self.candidate_artifacts):
            return False
        for attempt, artifact in zip(candidate_attempts, self.candidate_artifacts):
            if type(artifact) is not CandidateArtifactV1:
                return False
            if (
                type(artifact.packet_id) is not str
                or type(artifact.producer_id) is not str
                or type(artifact.witness) is not str
                or (
                    artifact.claimed_terminal is not None
                    and type(artifact.claimed_terminal) is not str
                )
                or (
                    artifact.claimed_valid is not None
                    and type(artifact.claimed_valid) is not bool
                )
                or type(artifact.schema_version) is not str
                or type(artifact.authority_effect) is not str
            ):
                return False
            try:
                artifact_id = artifact.candidate_id
            except (TypeError, ValueError):
                return False
            if artifact_id != attempt.candidate_id:
                return False
            if not attempt.accepted:
                continue
            if (
                artifact.schema_version != CANDIDATE_SCHEMA
                or artifact.authority_effect != "None"
                or artifact.packet_id != self.packet_id
                or artifact.producer_id != attempt.solver_id
                or not artifact.witness
            ):
                return False
            try:
                payload_hash = domain_digest(
                    "omega.oesos.candidate-payload.v1",
                    artifact.payload,
                )
            except (TypeError, ValueError):
                return False
            if payload_hash != attempt.candidate_payload_hash:
                return False

        decision_events = tuple(
            event
            for event in self.process_events
            if event.event_type
            in {"solver-refusal", "candidate-refusal", "verified-retraction"}
        )
        if len(decision_events) != len(self.attempts):
            return False
        for attempt, event in zip(self.attempts, decision_events):
            if attempt.accepted:
                if (
                    event.event_type != "verified-retraction"
                    or event.dda_letter != "E"
                    or event.output_state_hash != attempt.candidate_state_hash
                    or attempt.after_measure is None
                    or event.details
                    != freeze(
                        {
                            "solver_id": attempt.solver_id,
                            "candidate_id": attempt.candidate_id,
                            "raw_mass": attempt.after_raw_mass,
                            "phi1": attempt.after_measure[1],
                            "gamma2": attempt.after_measure[0],
                            "obstruction_mass": (
                                attempt.after_measure[1] + attempt.after_measure[0]
                            ),
                            "claimed_terminal_ignored": attempt.claimed_terminal,
                        }
                    )
                ):
                    return False
            elif event.event_type == "solver-refusal":
                if (
                    attempt.candidate_id is not None
                    or event.dda_letter != "M"
                    or event.details
                    != freeze(
                        {
                            "solver_id": attempt.solver_id,
                            "reason": attempt.reason,
                        }
                    )
                ):
                    return False
            elif (
                event.event_type != "candidate-refusal"
                or event.dda_letter != "M"
                or event.details
                != freeze(
                    {
                        "solver_id": attempt.solver_id,
                        "candidate_id": attempt.candidate_id,
                        "candidate_state_hash": attempt.candidate_state_hash,
                        "reason": attempt.reason,
                        "claimed_terminal": attempt.claimed_terminal,
                    }
                )
            ):
                return False

        active: dict[str, float] = {}
        ever_seen: set[str] = set()
        last_step = -1
        for event in self.obstruction_events:
            if (
                type(event.step) is not int
                or type(event.obstruction_id) is not str
                or type(event.disposition) is not str
                or type(event.magnitude) is not float
                or type(event.witness) is not str
                or event.step < last_step
                or event.step > self.accepted_steps
                or not event.obstruction_id
                or not event.witness
                or not math.isfinite(event.magnitude)
                or event.magnitude <= 0.0
            ):
                return False
            last_step = event.step
            if event.disposition == "OPENED":
                if event.obstruction_id in ever_seen:
                    return False
                ever_seen.add(event.obstruction_id)
                active[event.obstruction_id] = event.magnitude
            elif event.disposition == "REOPENED":
                if (
                    event.obstruction_id not in ever_seen
                    or event.obstruction_id in active
                ):
                    return False
                active[event.obstruction_id] = event.magnitude
            elif event.disposition == "UPDATED":
                previous = active.get(event.obstruction_id)
                if previous is None or event.magnitude >= previous:
                    return False
                active[event.obstruction_id] = event.magnitude
            elif event.disposition == "DISCHARGED":
                previous = active.get(event.obstruction_id)
                if previous is None or event.magnitude != previous:
                    return False
                del active[event.obstruction_id]
            else:
                return False
        if tuple(sorted(active)) != self.active_obstructions:
            return False
        accepted_attempts = tuple(
            attempt for attempt in self.attempts if attempt.accepted
        )
        if accepted_attempts and (
            self.final_projection is None
            or accepted_attempts[-1].candidate_state_hash != self.output_state_hash
        ):
            return False
        try:
            evidence_digest = _run_evidence_digest(
                packet_id=self.packet_id,
                runtime_id=self.runtime_id,
                solver_registry_hash=self.solver_registry_hash,
                parent_event_id=self.parent_event_id,
                prime000=self.prime000,
                adapter=self.adapter,
                detector=self.detector,
                terminal_status=self.terminal_status,
                stop_reasons=self.stop_reasons,
                input_state_hash=self.input_state_hash,
                output_state_hash=self.output_state_hash,
                final_native_state=self.final_native_state,
                final_projection=self.final_projection,
                attempts=self.attempts,
                candidate_artifacts=self.candidate_artifacts,
                accepted_steps=self.accepted_steps,
                obstruction_events=self.obstruction_events,
                active_obstructions=self.active_obstructions,
                process_events=self.process_events[:-1],
                authority_effect=self.authority_effect,
            )
        except (AttributeError, TypeError, ValueError):
            return False
        expected_terminal_details = freeze(
            {
                "terminal_status": self.terminal_status.value,
                "stop_reasons": self.stop_reasons,
                "active_obstructions": self.active_obstructions,
                "evidence_digest": evidence_digest,
            }
        )
        return terminal_event.details == expected_terminal_details

    @property
    def locally_resolved(self) -> bool:
        return (
            self.evidence_valid()
            and type(self.terminal_status) is TerminalStatus
            and self.terminal_status is TerminalStatus.LAB_EXACT_CANDIDATE
            and type(self.final_projection) is ProjectionReceipt
            and self.final_projection.is_exact
            and type(self.active_obstructions) is tuple
            and not self.active_obstructions
            and self.final_native_state is not None
            and type(self.prime000) is Prime000ShapeReceipt
            and self.prime000.accepted
            and type(self.adapter) is Prime001ShapeReceipt
            and self.adapter.sound
            and type(self.detector) is DetectorAdequacyReceipt
            and self.detector.adequate
        )

    def to_wire_receipt(self) -> EvaluationReceiptV1:
        if not self.evidence_valid():
            raise ValueError("run receipt does not match its committed evidence")
        return EvaluationReceiptV1(
            packet_id=self.packet_id,
            input_state_hash=self.input_state_hash,
            output_state_hash=self.output_state_hash,
            terminal_status=self.terminal_status.value,
            runtime_id=self.runtime_id,
            solver_registry_hash=self.solver_registry_hash,
            attempts=tuple(
                AttemptEvidenceV1(
                    solver_id=attempt.solver_id,
                    candidate_id=attempt.candidate_id,
                    candidate_state_hash=attempt.candidate_state_hash,
                    accepted=attempt.accepted,
                    reason=attempt.reason,
                )
                for attempt in self.attempts
            ),
            parent_event_id=self.parent_event_id,
            event_root=self.event_root,
            active_obstructions=self.active_obstructions,
            authority_effect=self.authority_effect,
        )


def _empty_adapter_receipt(
    problem: RuntimeProblem, detail: str
) -> Prime001ShapeReceipt:
    return Prime001ShapeReceipt(
        adapter_id=problem.adapter.adapter_id,
        source_carrier_id=problem.adapter.source_carrier_id,
        target_carrier_id=problem.adapter.target_carrier_id,
        sound=False,
        loss_ledger=(),
        detail=detail,
    )


def _empty_detector_receipt(
    problem: RuntimeProblem, failure: str
) -> DetectorAdequacyReceipt:
    return DetectorAdequacyReceipt(
        projector_id=problem.projector.projector_id,
        adequate=False,
        cases_checked=0,
        failures=(failure,),
    )


class OesosLab:
    """Bounded, deterministic proposal router with independent projection.

    The object is intentionally a laboratory evaluator.  Its local continuation
    predicate controls only in-memory experiment state and cannot substitute for
    the sealed Rust Prime 002 ``StepPermit``.
    """

    def __init__(
        self,
        solvers: Iterable[CandidateSolver],
        policy: tuple[str, ...] | None = None,
    ) -> None:
        try:
            solver_list = [copy.deepcopy(solver) for solver in solvers]
        except Exception as exc:
            raise ValueError(
                "registered solvers must support isolated snapshots"
            ) from exc
        self._solvers = {solver.manifest.solver_id: solver for solver in solver_list}
        if len(self._solvers) != len(solver_list):
            raise ValueError("solver ids must be unique")
        self._solver_factories = {
            solver_id: SolverFactoryV1.from_solver(solver)
            for solver_id, solver in self._solvers.items()
        }
        default_policy = tuple(solver.manifest.solver_id for solver in solver_list)
        self.policy = policy or default_policy
        self._validate_policy(self.policy)
        self._solver_registry_hash = domain_digest(
            "omega.oesos.solver-registry.v1",
            tuple(
                sorted(
                    (solver_id, factory.factory_id)
                    for solver_id, factory in self._solver_factories.items()
                )
            ),
        )

    @property
    def solvers(self) -> tuple[CandidateSolver, ...]:
        return tuple(
            self._solver_factories[solver_id].construct() for solver_id in self.policy
        )

    @property
    def solver_registry_hash(self) -> str:
        return self._solver_registry_hash

    @property
    def promotion_isolation_attested(self) -> bool:
        return all(
            factory.promotion_isolation_attested
            for factory in self._solver_factories.values()
        )

    @property
    def promotion_isolation_findings(self) -> tuple[str, ...]:
        return tuple(
            finding
            for solver_id in sorted(self._solver_factories)
            for finding in self._solver_factories[solver_id].isolation_findings
        )

    def solver_registry_identity_valid(self) -> bool:
        return all(
            factory.current_identity_matches()
            for factory in self._solver_factories.values()
        )

    def _apply_verified_local_policy(
        self,
        policy: tuple[str, ...],
        *,
        expected_registry_hash: str,
    ) -> None:
        if (
            expected_registry_hash != self.solver_registry_hash
            or not self.promotion_isolation_attested
            or not self.solver_registry_identity_valid()
        ):
            raise ValueError("verified local policy admission preconditions failed")
        self._validate_policy(policy)
        self.policy = policy

    def _validate_policy(self, policy: tuple[str, ...]) -> None:
        if len(policy) != len(self._solvers) or set(policy) != set(self._solvers):
            raise ValueError("policy must be a permutation of the registered solvers")

    def _prime000(self, problem: RuntimeProblem) -> Prime000ShapeReceipt:
        eligible = tuple(
            solver_id
            for solver_id in self.policy
            if self._solvers[solver_id].manifest.supports(
                problem.envelope.packet_family
            )
        )
        declarations = (
            f"01:carrier:{problem.envelope.carrier_id}",
            f"02:primitive_difference:{problem.primitive_difference}",
            f"03:zero_relation:{problem.zero_relation}",
            "04:cochains:"
            + ("declared" if problem.cochain_declared else "not-applicable"),
            f"05:quotient_residual:{problem.projector.projector_id}",
            "06:phi1-gamma2:separate",
            f"07:observer:{problem.observer_id}",
            f"08:witness:{problem.witness_certificate}",
            "09:eligible_candidate_producers:" + ",".join(eligible),
            "10:routing_policy:" + ",".join(self.policy),
            f"11:terminalizer:{TERMINALIZER_ID}",
            "12:literature:deferred-until-terminal",
        )
        blockers: list[str] = []
        envelope = problem.envelope
        if envelope.schema_version != PACKET_SCHEMA:
            blockers.append("UNSUPPORTED_PACKET_SCHEMA")
        if envelope.authority_effect != "None":
            blockers.append("AUTHORITY_EXPANSION")
        if envelope.packet_kind != "problem" or envelope.framing_mode != "strict":
            blockers.append("UNSUPPORTED_PACKET_FRAMING")
        if envelope.terminal_target != "ExactOrTypedObstruction":
            blockers.append("UNSUPPORTED_TERMINAL_TARGET")
        if envelope.evidence_ceiling != "ReplayableLabEvidence":
            blockers.append("UNSUPPORTED_EVIDENCE_CEILING")
        if envelope.oracle_policy != "ExternalVerifierRequired":
            blockers.append("UNSAFE_ORACLE_POLICY")
        if envelope.allowed_transforms != ("same_carrier_retraction",):
            blockers.append("UNSUPPORTED_TRANSFORM_SET")
        if (
            not envelope.constraints
            or any(not item for item in envelope.constraints)
            or len(envelope.constraints) != len(set(envelope.constraints))
        ):
            blockers.append("INVALID_CONSTRAINT_SET")
        if any(not item for item in envelope.protected_boundaries) or len(
            envelope.protected_boundaries
        ) != len(set(envelope.protected_boundaries)):
            blockers.append("INVALID_PROTECTED_BOUNDARIES")
        if not _is_sha256(envelope.initial_state_hash):
            blockers.append("INVALID_INITIAL_STATE_HASH")
        elif envelope.initial_state_hash != domain_digest(
            "omega.oesos.native-state.v1", problem.native_initial_state
        ):
            blockers.append("INITIAL_STATE_PACKET_MISMATCH")
        if not _is_sha256(envelope.source_digest):
            blockers.append("MISSING_SOURCE_DIGEST")
        if envelope.parent_event_id is not None and not _is_sha256(
            envelope.parent_event_id
        ):
            blockers.append("INVALID_PARENT_EVENT")
        for value, reason in (
            (envelope.task_id, "MISSING_TASK"),
            (envelope.packet_family, "MISSING_FAMILY"),
            (envelope.carrier_id, "MISSING_CARRIER"),
            (problem.primitive_difference, "MISSING_PRIMITIVE_DIFFERENCE"),
            (problem.zero_relation, "MISSING_ZERO_RELATION"),
            (problem.observer_id, "MISSING_OBSERVER"),
            (problem.witness_certificate, "MISSING_WITNESS"),
        ):
            if not value:
                blockers.append(reason)
        if envelope.step_budget <= 0:
            blockers.append("BUDGET_EXHAUSTED")
        if problem.adapter.source_carrier_id != envelope.carrier_id:
            blockers.append("ADAPTER_SOURCE_MISMATCH")
        if problem.adapter.target_carrier_id != envelope.carrier_id:
            blockers.append("CARRIER_LIFT_UNLICENSED")
        if not _is_sha256(getattr(problem.projector, "config_digest", "")):
            blockers.append("MISSING_PROJECTOR_CONFIG")
        if not _is_sha256(getattr(problem.adapter, "config_digest", "")):
            blockers.append("MISSING_ADAPTER_CONFIG")
        try:
            packet_semantics_valid = problem.projector.validate_packet(
                envelope,
                problem.native_initial_state,
            )
        except Exception:
            packet_semantics_valid = False
        if not packet_semantics_valid:
            blockers.append("PACKET_RUNTIME_SEMANTICS_MISMATCH")
        if problem.observer_id != problem.projector.projector_id:
            blockers.append("OBSERVER_PROJECTOR_MISMATCH")
        if set(envelope.protected_boundaries) != set(problem.protected_obstruction_ids):
            blockers.append("PROTECTED_BOUNDARY_MISMATCH")
        for solver_id in eligible:
            manifest = self._solvers[solver_id].manifest
            if not solver_id or manifest.authority_effect != "None":
                blockers.append(f"SOLVER_AUTHORITY_EXPANSION:{solver_id}")
            if not manifest.deterministic:
                blockers.append(f"NONDETERMINISTIC_SOLVER:{solver_id}")
            if not self._solver_factories[solver_id].current_identity_matches():
                blockers.append(f"SOLVER_IMPLEMENTATION_DRIFT:{solver_id}")
            if solver_id == problem.projector.projector_id:
                blockers.append(f"PRODUCER_EVALUATOR_COLLISION:{solver_id}")
        if not eligible:
            blockers.append("NO_CAPABLE_SOLVER")
        return Prime000ShapeReceipt(declarations=declarations, blockers=tuple(blockers))

    def _adapter_receipt(
        self,
        problem: RuntimeProblem,
        native_state: Any,
    ) -> tuple[Prime001ShapeReceipt, Any | None]:
        adapter = problem.adapter
        try:
            packet_state = adapter.adapt(native_state)
            roundtrip = adapter.descend(packet_state)
            native_meaning = freeze(adapter.native_meaning(native_state))
            packet_meaning = freeze(adapter.packet_meaning(packet_state))
            roundtrip_meaning = freeze(adapter.native_meaning(roundtrip))
            projector_meaning = freeze(problem.projector.meaning(packet_state))
            loss = tuple(adapter.loss_ledger(native_state))
            sound = (
                native_meaning == packet_meaning
                and native_meaning == roundtrip_meaning
                and packet_meaning == projector_meaning
                and not loss
                and getattr(adapter, "authority_effect", "None") == "None"
            )
            detail = (
                "adapter square commutes"
                if sound
                else "adapter square or protected view failed"
            )
            return (
                Prime001ShapeReceipt(
                    adapter_id=adapter.adapter_id,
                    source_carrier_id=adapter.source_carrier_id,
                    target_carrier_id=adapter.target_carrier_id,
                    sound=sound,
                    loss_ledger=loss,
                    detail=detail,
                ),
                packet_state,
            )
        except Exception as exc:
            return _empty_adapter_receipt(
                problem, f"adapter exception: {type(exc).__name__}"
            ), None

    def _project(self, problem: RuntimeProblem, packet_state: Any) -> ProjectionReceipt:
        receipt = problem.projector.project(packet_state)
        expected_hash = domain_digest(
            "omega.oesos.state.v1", problem.projector.meaning(packet_state)
        )
        if receipt.projector_id != problem.projector.projector_id:
            raise ValueError("projection receipt names the wrong projector")
        if receipt.authority_effect != "None":
            raise ValueError("projection receipt expands authority")
        if not receipt.witness:
            raise ValueError("projection receipt has no witness")
        if receipt.state_hash != expected_hash:
            raise ValueError("projection state hash does not bind projector meaning")
        if len(receipt.active_ids) != len(set(receipt.active_ids)):
            raise ValueError("projection returned duplicate obstruction ids")
        if not math.isfinite(receipt.phi1) or not math.isfinite(receipt.gamma2):
            raise ValueError("projection aggregates must be finite")
        return receipt

    def _detector_adequacy(self, problem: RuntimeProblem) -> DetectorAdequacyReceipt:
        failures: list[str] = []
        saw_green = False
        saw_red = False
        for case in problem.detector_cases:
            try:
                packet_state = problem.adapter.adapt(case.native_state)
                projection = self._project(problem, packet_state)
                expected = tuple(sorted(case.expected_active_ids))
                if projection.active_ids != expected:
                    failures.append(
                        f"{case.case_id}:expected={expected}:observed={projection.active_ids}"
                    )
                if projection.control_digest != case.expected_projection_digest:
                    failures.append(f"{case.case_id}:projection-control-mismatch")
                saw_green = saw_green or not expected
                saw_red = saw_red or bool(expected)
            except Exception as exc:
                failures.append(f"{case.case_id}:exception={type(exc).__name__}")
        if not problem.detector_cases:
            failures.append("NO_ADEQUACY_CASES")
        if not saw_green:
            failures.append("NO_NEGATIVE_CONTROL")
        if not saw_red:
            failures.append("NO_POSITIVE_CONTROL")
        return DetectorAdequacyReceipt(
            projector_id=problem.projector.projector_id,
            adequate=not failures,
            cases_checked=len(problem.detector_cases),
            failures=tuple(failures),
        )

    @staticmethod
    def _strict_descent(before: ProjectionReceipt, after: ProjectionReceipt) -> bool:
        before_map = {item.obstruction_id: item for item in before.obstructions}
        after_map = {item.obstruction_id: item for item in after.obstructions}
        if set(after_map) - set(before_map):
            return False
        strict = bool(set(before_map) - set(after_map))
        for obstruction_id, item in after_map.items():
            previous = before_map[obstruction_id]
            if item.closure_failure != previous.closure_failure:
                return False
            if item.magnitude > previous.magnitude:
                return False
            strict = strict or item.magnitude < previous.magnitude
        return strict

    @staticmethod
    def _residual_terminal(projection: ProjectionReceipt) -> TerminalStatus:
        if projection.is_exact:
            return TerminalStatus.LAB_EXACT_CANDIDATE
        if projection.gamma2 > 0.0:
            return TerminalStatus.LAB_ACTIVE_CLOSURE_FAILURE_CANDIDATE
        return TerminalStatus.LAB_CLOSED_RESIDUAL_CANDIDATE

    def _terminal_receipt(
        self,
        *,
        problem: RuntimeProblem,
        prime000: Prime000ShapeReceipt,
        adapter: Prime001ShapeReceipt,
        detector: DetectorAdequacyReceipt,
        terminal_status: TerminalStatus,
        stop_reasons: tuple[str, ...],
        input_state_hash: str,
        packet_state: Any,
        final_projection: ProjectionReceipt | None,
        attempts: list[SolverAttempt],
        candidate_artifacts: list[CandidateArtifactV1],
        accepted_steps: int,
        ledger: ObstructionLedger,
        events: ProcessEventLog,
        packet_state_adapted: bool = True,
    ) -> RunReceipt:
        current_hash = (
            events.events[-1].output_state_hash if events.events else input_state_hash
        )
        output_hash = (
            final_projection.state_hash
            if final_projection is not None
            else current_hash
        )
        if output_hash != current_hash:
            terminal_status = TerminalStatus.INVALID_PACKET
            stop_reasons = (*stop_reasons, "EVENT_STATE_DIVERGENCE")
            output_hash = current_hash
        if not packet_state_adapted:
            try:
                final_native_state = copy.deepcopy(problem.native_initial_state)
                freeze(final_native_state)
            except Exception as exc:
                final_native_state = None
                stop_reasons = (
                    *stop_reasons,
                    f"FINAL_STATE_SNAPSHOT_FAILURE:{type(exc).__name__}",
                )
        else:
            try:
                descended_state = problem.adapter.descend(packet_state)
                final_roundtrip = problem.adapter.adapt(descended_state)
                if freeze(problem.adapter.packet_meaning(final_roundtrip)) != freeze(
                    problem.adapter.packet_meaning(packet_state)
                ):
                    raise ValueError("final adapter round-trip changed packet meaning")
                final_native_state = copy.deepcopy(descended_state)
                freeze(final_native_state)
            except Exception as exc:
                final_native_state = None
                terminal_status = TerminalStatus.ADAPTER_FAILURE
                stop_reasons = (
                    *stop_reasons,
                    f"FINAL_DESCENT_FAILURE:{type(exc).__name__}",
                )
        evidence_digest = _run_evidence_digest(
            packet_id=problem.envelope.packet_id,
            runtime_id=problem.runtime_id,
            solver_registry_hash=self.solver_registry_hash,
            parent_event_id=problem.envelope.parent_event_id,
            prime000=prime000,
            adapter=adapter,
            detector=detector,
            terminal_status=terminal_status,
            stop_reasons=stop_reasons,
            input_state_hash=input_state_hash,
            output_state_hash=output_hash,
            final_native_state=final_native_state,
            final_projection=final_projection,
            attempts=attempts,
            candidate_artifacts=candidate_artifacts,
            accepted_steps=accepted_steps,
            obstruction_events=ledger.events,
            active_obstructions=ledger.active_ids,
            process_events=events.events,
            authority_effect="None",
        )
        events.append(
            "terminal",
            DdaLetter.T,
            output_hash,
            output_hash,
            {
                "terminal_status": terminal_status.value,
                "stop_reasons": stop_reasons,
                "active_obstructions": ledger.active_ids,
                "evidence_digest": evidence_digest,
            },
        )
        return RunReceipt(
            packet_id=problem.envelope.packet_id,
            runtime_id=problem.runtime_id,
            solver_registry_hash=self.solver_registry_hash,
            parent_event_id=problem.envelope.parent_event_id,
            prime000=prime000,
            adapter=adapter,
            detector=detector,
            terminal_status=terminal_status,
            stop_reasons=stop_reasons,
            input_state_hash=input_state_hash,
            output_state_hash=output_hash,
            final_native_state=final_native_state,
            final_projection=final_projection,
            attempts=tuple(attempts),
            candidate_artifacts=tuple(candidate_artifacts),
            accepted_steps=accepted_steps,
            obstruction_events=ledger.events,
            active_obstructions=ledger.active_ids,
            process_events=events.events,
            event_root=events.root,
        )

    def solve(self, problem: RuntimeProblem) -> RunReceipt:
        run_solvers = {
            solver_id: factory.construct()
            for solver_id, factory in self._solver_factories.items()
        }
        events = ProcessEventLog(problem.envelope.parent_event_id)
        ledger = ObstructionLedger()
        attempts: list[SolverAttempt] = []
        candidate_artifacts: list[CandidateArtifactV1] = []
        accepted_steps = 0
        input_hash = domain_digest(
            "omega.oesos.native-state.v1", problem.native_initial_state
        )
        events.append(
            "declare-carrier",
            DdaLetter.C,
            input_hash,
            input_hash,
            {"packet_id": problem.envelope.packet_id, "runtime_id": problem.runtime_id},
        )

        prime000 = self._prime000(problem)
        if not prime000.accepted:
            return self._terminal_receipt(
                problem=problem,
                prime000=prime000,
                adapter=_empty_adapter_receipt(problem, "Prime 000 shape refused"),
                detector=_empty_detector_receipt(problem, "Prime 000 shape refused"),
                terminal_status=TerminalStatus.INVALID_PACKET,
                stop_reasons=prime000.blockers,
                input_state_hash=input_hash,
                packet_state=problem.native_initial_state,
                final_projection=None,
                attempts=attempts,
                candidate_artifacts=candidate_artifacts,
                accepted_steps=accepted_steps,
                ledger=ledger,
                events=events,
                packet_state_adapted=False,
            )

        adapter, packet_state = self._adapter_receipt(
            problem, problem.native_initial_state
        )
        if not adapter.sound or packet_state is None:
            events.append(
                "adapter-refusal",
                DdaLetter.M,
                input_hash,
                input_hash,
                {"detail": adapter.detail, "loss_ledger": adapter.loss_ledger},
            )
            return self._terminal_receipt(
                problem=problem,
                prime000=prime000,
                adapter=adapter,
                detector=_empty_detector_receipt(problem, "adapter failed"),
                terminal_status=TerminalStatus.ADAPTER_FAILURE,
                stop_reasons=("ADAPTER_FAILURE",),
                input_state_hash=input_hash,
                packet_state=problem.native_initial_state,
                final_projection=None,
                attempts=attempts,
                candidate_artifacts=candidate_artifacts,
                accepted_steps=accepted_steps,
                ledger=ledger,
                events=events,
                packet_state_adapted=False,
            )
        packet_hash = domain_digest(
            "omega.oesos.state.v1", problem.projector.meaning(packet_state)
        )
        events.append(
            "adapter-descent",
            DdaLetter.D,
            input_hash,
            packet_hash,
            {"adapter_id": adapter.adapter_id, "loss_ledger": adapter.loss_ledger},
        )

        detector = self._detector_adequacy(problem)
        if not detector.adequate:
            events.append(
                "detector-refusal",
                DdaLetter.M,
                packet_hash,
                packet_hash,
                {"failures": detector.failures},
            )
            return self._terminal_receipt(
                problem=problem,
                prime000=prime000,
                adapter=adapter,
                detector=detector,
                terminal_status=TerminalStatus.DETECTOR_INADEQUATE,
                stop_reasons=("MISSING_DETECTOR",),
                input_state_hash=input_hash,
                packet_state=packet_state,
                final_projection=None,
                attempts=attempts,
                candidate_artifacts=candidate_artifacts,
                accepted_steps=accepted_steps,
                ledger=ledger,
                events=events,
            )

        try:
            projection = self._project(problem, packet_state)
        except Exception as exc:
            events.append(
                "projection-refusal",
                DdaLetter.M,
                packet_hash,
                packet_hash,
                {"exception": type(exc).__name__},
            )
            return self._terminal_receipt(
                problem=problem,
                prime000=prime000,
                adapter=adapter,
                detector=detector,
                terminal_status=TerminalStatus.DETECTOR_INADEQUATE,
                stop_reasons=("PROJECTION_FAILURE",),
                input_state_hash=input_hash,
                packet_state=packet_state,
                final_projection=None,
                attempts=attempts,
                candidate_artifacts=candidate_artifacts,
                accepted_steps=accepted_steps,
                ledger=ledger,
                events=events,
            )
        ledger.reconcile(projection, step=0, witness=projection.witness)
        events.append(
            "residual-projection",
            DdaLetter.R,
            projection.state_hash,
            projection.state_hash,
            {
                "raw_mass": projection.raw_mass,
                "phi1": projection.phi1,
                "gamma2": projection.gamma2,
                "obstruction_mass": projection.obstruction_mass,
                "obstructions": projection.active_ids,
            },
        )
        seen_states = {projection.state_hash}

        if projection.is_exact:
            return self._terminal_receipt(
                problem=problem,
                prime000=prime000,
                adapter=adapter,
                detector=detector,
                terminal_status=TerminalStatus.LAB_EXACT_CANDIDATE,
                stop_reasons=("ZERO_RELATION_REACHED",),
                input_state_hash=input_hash,
                packet_state=packet_state,
                final_projection=projection,
                attempts=attempts,
                candidate_artifacts=candidate_artifacts,
                accepted_steps=accepted_steps,
                ledger=ledger,
                events=events,
            )

        while True:
            if accepted_steps >= problem.envelope.step_budget:
                return self._terminal_receipt(
                    problem=problem,
                    prime000=prime000,
                    adapter=adapter,
                    detector=detector,
                    terminal_status=TerminalStatus.BUDGET_EXHAUSTED,
                    stop_reasons=("BUDGET_EXHAUSTED",),
                    input_state_hash=input_hash,
                    packet_state=packet_state,
                    final_projection=projection,
                    attempts=attempts,
                    candidate_artifacts=candidate_artifacts,
                    accepted_steps=accepted_steps,
                    ledger=ledger,
                    events=events,
                )

            accepted = False
            for solver_id in self.policy:
                solver = run_solvers[solver_id]
                if not solver.manifest.supports(problem.envelope.packet_family):
                    continue
                before_measure = projection.measure
                try:
                    proposal = solver.propose(problem, packet_state, projection)
                except Exception as exc:
                    proposal = None
                    reason = f"solver-exception:{type(exc).__name__}"
                else:
                    reason = "no-proposal" if proposal is None else "candidate-rejected"
                manifest_drift = solver.manifest != self._solvers[solver_id].manifest
                environment_drift = not self._solver_factories[
                    solver_id
                ].current_identity_matches()
                if manifest_drift and proposal is None:
                    reason = "solver-manifest-drift"
                elif environment_drift and proposal is None:
                    reason = "solver-execution-environment-drift"
                if proposal is None:
                    attempts.append(
                        SolverAttempt(
                            solver_id=solver_id,
                            candidate_id=None,
                            candidate_state_hash=None,
                            accepted=False,
                            reason=reason,
                            before_measure=before_measure,
                            after_measure=None,
                            before_raw_mass=projection.raw_mass,
                            after_raw_mass=None,
                        )
                    )
                    events.append(
                        "solver-refusal",
                        DdaLetter.M,
                        projection.state_hash,
                        projection.state_hash,
                        {"solver_id": solver_id, "reason": reason},
                    )
                    continue

                rejection: str | None = None
                candidate_projection: ProjectionReceipt | None = None
                candidate_state_hash: str | None = None
                candidate_payload_hash: str | None = None
                raw_candidate = proposal.candidate
                if isinstance(raw_candidate, CandidateArtifactV1):
                    candidate = CandidateArtifactV1(
                        packet_id=raw_candidate.packet_id,
                        producer_id=raw_candidate.producer_id,
                        payload=raw_candidate.payload,
                        witness=raw_candidate.witness,
                        claimed_terminal=raw_candidate.claimed_terminal,
                        claimed_valid=raw_candidate.claimed_valid,
                        metadata=raw_candidate.metadata,
                        schema_version=raw_candidate.schema_version,
                        authority_effect=raw_candidate.authority_effect,
                    )
                    candidate_id = candidate.candidate_id
                    candidate_artifacts.append(candidate)
                    claimed_terminal = candidate.claimed_terminal
                else:
                    candidate = None
                    candidate_id = None
                    claimed_terminal = None
                try:
                    frozen_proposed_state = freeze(proposal.state)
                    proposed_state_canonical = True
                except (TypeError, ValueError):
                    frozen_proposed_state = None
                    proposed_state_canonical = False
                if candidate_id is not None and proposed_state_canonical:
                    candidate_payload_hash = domain_digest(
                        "omega.oesos.candidate-payload.v1",
                        frozen_proposed_state,
                    )
                if manifest_drift:
                    rejection = "solver-manifest-drift"
                elif environment_drift:
                    rejection = "solver-execution-environment-drift"
                elif candidate is None:
                    rejection = "candidate-type-invalid"
                if rejection is not None:
                    pass
                elif candidate.schema_version != CANDIDATE_SCHEMA:
                    rejection = "candidate-schema-mismatch"
                elif candidate.authority_effect != "None":
                    rejection = "candidate-authority-expansion"
                elif candidate.producer_id != solver_id:
                    rejection = "candidate-producer-mismatch"
                elif not candidate.witness:
                    rejection = "candidate-witness-missing"
                elif candidate.packet_id != problem.envelope.packet_id:
                    rejection = "candidate-packet-mismatch"
                elif not proposed_state_canonical:
                    rejection = "candidate-state-not-canonical"
                elif candidate.payload != frozen_proposed_state:
                    rejection = "candidate-payload-state-mismatch"
                elif proposal.next_carrier_id != problem.adapter.target_carrier_id:
                    rejection = "next-carrier-undeclared"
                elif not proposal.candidate_declares_minimal_move:
                    rejection = "candidate-minimal-move-declaration-missing"
                elif proposal.candidate_loss_claims:
                    rejection = "candidate-loss-claims-unsupported"
                else:
                    try:
                        candidate_projection = self._project(problem, proposal.state)
                        candidate_state_hash = candidate_projection.state_hash
                        descended = problem.adapter.descend(proposal.state)
                        readapted = problem.adapter.adapt(descended)
                        if freeze(problem.adapter.packet_meaning(readapted)) != freeze(
                            problem.adapter.packet_meaning(proposal.state)
                        ):
                            rejection = "candidate-adapter-square-failed"
                        elif freeze(
                            problem.projector.skeleton(proposal.state)
                        ) != freeze(problem.projector.skeleton(packet_state)):
                            rejection = "skeleton-not-preserved"
                        elif candidate_projection.state_hash in seen_states:
                            rejection = "repeated-state"
                        elif not self._strict_descent(projection, candidate_projection):
                            rejection = "no-strict-residual-descent"
                        elif not problem.projector.verify_retraction(
                            solver_id,
                            packet_state,
                            proposal.state,
                        ):
                            rejection = "host-retraction-law-failed"
                    except Exception as exc:
                        rejection = f"verification-exception:{type(exc).__name__}"

                if rejection is not None or candidate_projection is None:
                    rejection_reason = rejection or "candidate-rejected"
                    attempts.append(
                        SolverAttempt(
                            solver_id=solver_id,
                            candidate_id=candidate_id,
                            candidate_state_hash=candidate_state_hash,
                            accepted=False,
                            reason=rejection_reason,
                            before_measure=before_measure,
                            after_measure=(
                                candidate_projection.measure
                                if candidate_projection is not None
                                else None
                            ),
                            before_raw_mass=projection.raw_mass,
                            after_raw_mass=(
                                candidate_projection.raw_mass
                                if candidate_projection is not None
                                else None
                            ),
                            claimed_terminal=claimed_terminal,
                            candidate_payload_hash=candidate_payload_hash,
                        )
                    )
                    events.append(
                        "candidate-refusal",
                        DdaLetter.M,
                        projection.state_hash,
                        projection.state_hash,
                        {
                            "solver_id": solver_id,
                            "candidate_id": candidate_id,
                            "candidate_state_hash": candidate_state_hash,
                            "reason": rejection_reason,
                            "claimed_terminal": claimed_terminal,
                        },
                    )
                    continue

                attempts.append(
                    SolverAttempt(
                        solver_id=solver_id,
                        candidate_id=candidate_id,
                        candidate_state_hash=candidate_state_hash,
                        accepted=True,
                        reason="independently-verified-strict-descent",
                        before_measure=before_measure,
                        after_measure=candidate_projection.measure,
                        before_raw_mass=projection.raw_mass,
                        after_raw_mass=candidate_projection.raw_mass,
                        claimed_terminal=claimed_terminal,
                        candidate_payload_hash=candidate_payload_hash,
                    )
                )
                prior_hash = projection.state_hash
                packet_state = proposal.state
                projection = candidate_projection
                accepted_steps += 1
                seen_states.add(projection.state_hash)
                ledger.reconcile(
                    projection,
                    step=accepted_steps,
                    witness=candidate_id,
                )
                events.append(
                    "verified-retraction",
                    DdaLetter.E,
                    prior_hash,
                    projection.state_hash,
                    {
                        "solver_id": solver_id,
                        "candidate_id": candidate_id,
                        "raw_mass": projection.raw_mass,
                        "phi1": projection.phi1,
                        "gamma2": projection.gamma2,
                        "obstruction_mass": projection.obstruction_mass,
                        "claimed_terminal_ignored": claimed_terminal,
                    },
                )
                accepted = True

                if projection.is_exact:
                    return self._terminal_receipt(
                        problem=problem,
                        prime000=prime000,
                        adapter=adapter,
                        detector=detector,
                        terminal_status=TerminalStatus.LAB_EXACT_CANDIDATE,
                        stop_reasons=("ZERO_RELATION_REACHED",),
                        input_state_hash=input_hash,
                        packet_state=packet_state,
                        final_projection=projection,
                        attempts=attempts,
                        candidate_artifacts=candidate_artifacts,
                        accepted_steps=accepted_steps,
                        ledger=ledger,
                        events=events,
                    )

                blockers: list[str] = []
                if proposal.next_carrier_id != problem.adapter.target_carrier_id:
                    blockers.append("MISSING_CARRIER")
                if not adapter.sound:
                    blockers.append("ADAPTER_FAILURE")
                if not detector.adequate:
                    blockers.append("MISSING_DETECTOR")
                if not proposal.candidate_declares_minimal_move:
                    blockers.append("UNAUTHORIZED_CONTINUATION")
                if accepted_steps >= problem.envelope.step_budget:
                    blockers.append("BUDGET_EXHAUSTED")
                prime002 = LocalContinuationCheck(
                    may_continue_locally=not blockers,
                    blockers=tuple(blockers),
                )
                if blockers:
                    status = (
                        TerminalStatus.BUDGET_EXHAUSTED
                        if "BUDGET_EXHAUSTED" in blockers
                        else TerminalStatus.UNAUTHORIZED_CONTINUATION
                    )
                    return self._terminal_receipt(
                        problem=problem,
                        prime000=prime000,
                        adapter=adapter,
                        detector=detector,
                        terminal_status=status,
                        stop_reasons=prime002.blockers,
                        input_state_hash=input_hash,
                        packet_state=packet_state,
                        final_projection=projection,
                        attempts=attempts,
                        candidate_artifacts=candidate_artifacts,
                        accepted_steps=accepted_steps,
                        ledger=ledger,
                        events=events,
                    )
                events.append(
                    "repacketize-same-carrier",
                    DdaLetter.I,
                    projection.state_hash,
                    projection.state_hash,
                    {
                        "local_continuation_check": "proposal-only",
                        "step": accepted_steps,
                    },
                )
                break

            if not accepted:
                status = self._residual_terminal(projection)
                return self._terminal_receipt(
                    problem=problem,
                    prime000=prime000,
                    adapter=adapter,
                    detector=detector,
                    terminal_status=status,
                    stop_reasons=("STUCK_CORPUS",),
                    input_state_hash=input_hash,
                    packet_state=packet_state,
                    final_projection=projection,
                    attempts=attempts,
                    candidate_artifacts=candidate_artifacts,
                    accepted_steps=accepted_steps,
                    ledger=ledger,
                    events=events,
                )

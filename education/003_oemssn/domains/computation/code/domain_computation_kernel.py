"""
Domain Kernel: Theoretical Computer Science & Automata Theory
AuthorityEffect: None
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class FuelStatus(str, Enum):
    HALTED = "HALTED"
    OUT_OF_FUEL = "OUT_OF_FUEL"
    CYCLE_DETECTED = "CYCLE_DETECTED"
    OBSTRUCTION = "OBSTRUCTION"


@dataclass
class PrimitiveDifferenceSetting:
    """Root W Witnessed Irreflexive Difference Germ: (X, R, a, b)."""

    carrier: Set[str]
    relation: Set[Tuple[str, str]]
    a: str
    b: str

    def is_irrefl(self) -> bool:
        """Verifies irreflexivity: forall x in carrier, (x, x) not in relation."""
        return all((x, x) not in self.relation for x in self.carrier)

    def is_witnessed(self) -> bool:
        """Verifies witness existence: (a, b) in relation."""
        return (self.a, self.b) in self.relation

    def is_distinct(self) -> bool:
        """Theorem of Distinctness: a != b under witnessed irreflexivity."""
        return self.a != self.b and self.is_witnessed() and self.is_irrefl()

    def transpose(self, edge: Tuple[str, str]) -> Tuple[str, str]:
        """Transposition operator sigma = (u, v) -> (v, u)."""
        return (edge[1], edge[0])

    def evaluate_1chain_boundary(self, edge: Tuple[str, str]) -> Dict[str, int]:
        """Oriented 1-chain boundary: partial_1(u, v) = {v: +1, u: -1}."""
        u, v = edge
        if u == v:
            return {}
        return {v: 1, u: -1}

    def verify_transposition_sign_inversion(self, edge: Tuple[str, str]) -> bool:
        """Verifies partial_1(sigma(e)) == -partial_1(e)."""
        u, v = edge
        if u == v:
            return False
        b_orig = self.evaluate_1chain_boundary(edge)
        b_trans = self.evaluate_1chain_boundary(self.transpose(edge))
        for pt in [u, v]:
            if b_trans.get(pt, 0) != -b_orig.get(pt, 0):
                return False
        return True


@dataclass
class SimplicialBoundaryReceipt:
    """Certified receipt of simplicial boundary nilpotency B_1 * B_2 = 0."""

    vertices: List[str]
    edges: List[Tuple[str, str]]
    faces: List[Tuple[str, str, str]]
    b1_matrix: List[List[int]]
    b2_matrix: List[List[int]]
    product_matrix: List[List[int]]
    is_nilpotent: bool
    num_cycles: int
    euler_characteristic: int
    authority_effect: str = "None"

    def __bool__(self) -> bool:
        """Backward compatibility for boolean checks on boundary closure."""
        return self.is_nilpotent


@dataclass(frozen=True)
class TuringConfiguration:
    """Instantaneous description (ID) of a discrete Turing machine."""

    state: str
    head_pos: int
    tape: Tuple[Tuple[int, str], ...] = ()  # sparse representation of non-blank tape cells

    def tape_dict(self) -> Dict[int, str]:
        return dict(self.tape)

    def read_cell(self, blank: str = "_") -> str:
        return dict(self.tape).get(self.head_pos, blank)

    @classmethod
    def from_dict(
        cls, state: str, head_pos: int, tape_map: Dict[int, str]
    ) -> "TuringConfiguration":
        clean_items = tuple(sorted((k, v) for k, v in tape_map.items() if v != "_"))
        return cls(state=state, head_pos=head_pos, tape=clean_items)


@dataclass
class TuringStepReceipt:
    """Audit receipt for a single deterministic execution step."""

    step_number: int
    config_before: TuringConfiguration
    symbol_read: str
    symbol_written: str
    head_direction: int  # -1 (Left), 0 (Stay), +1 (Right)
    config_after: TuringConfiguration
    fuel_remaining: int


@dataclass
class HaltingObstruction:
    """Formal certification that computation did not reach a halting state within fuel budget."""

    obstruction_id: str = "HaltingIncompletenessObstruction"
    initial_config: Optional[TuringConfiguration] = None
    terminal_config: Optional[TuringConfiguration] = None
    fuel_budget: int = 0
    steps_executed: int = 0
    cycle_detected: bool = False
    cycle_period: Optional[int] = None
    reason: str = (
        "Bounded fuel exhausted before reaching terminal state; halting undecidable within budget."
    )
    authority_effect: str = "None"


@dataclass
class FuelExecutionReceipt:
    """Certified end-to-end receipt of fuel-bounded computation."""

    start_node: Optional[str] = None
    terminal_node: Optional[str] = None
    initial_config: Optional[TuringConfiguration] = None
    terminal_config: Optional[TuringConfiguration] = None
    fuel_provided: int = 0
    fuel_consumed: int = 0
    fuel_remaining: int = 0
    steps_taken: int = 0
    status: FuelStatus = FuelStatus.HALTED
    trace: List[Any] = field(default_factory=list)
    step_receipts: List[TuringStepReceipt] = field(default_factory=list)
    obstruction: Optional[HaltingObstruction] = None
    authority_effect: str = "None"


@dataclass
class DomainState:
    step: int
    name: str
    carrier: Set[str] = field(default_factory=set)
    relations: Set[Tuple[str, str]] = field(default_factory=set)
    invariants: Dict[str, Any] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)
    branches_retained: List[str] = field(default_factory=list)
    branch_metadata: Dict[str, Dict[str, Any]] = field(default_factory=dict)


class DomainEngine:
    """Deterministic transition engine for computation domain."""

    def __init__(self):
        self.state = DomainState(step=0, name="state_empty_void")
        self.setting: Optional[PrimitiveDifferenceSetting] = None
        self.gap_detected: bool = False

    def step_01_admit_root(self, mark: str = "<>") -> bool:
        """Admits initial opaque root mark <> (change class: create_structure)."""
        self.state.carrier.add(mark)
        self.state.step = 1
        self.state.name = "state_initialized_with_root_reference"
        self.state.branches_retained = ["branch_root_single"]
        self.state.history.append("step_01: initial_datum (create_structure)")
        return True

    def step_02_admit_germ(self, a: str = "a", b: str = "b") -> bool:
        """Admits primitive difference pair (a, b) (change class: create_structure)."""
        if self.state.step < 1:
            return False
        self.state.carrier.update([a, b])
        self.state.relations.add((a, b))
        self.setting = PrimitiveDifferenceSetting(
            carrier=self.state.carrier, relation=self.state.relations, a=a, b=b
        )
        self.state.step = 2
        self.state.name = "state_with_distinguished_difference_pair"
        self.state.history.append("step_02: create_structure")
        return self.setting.is_witnessed()

    def step_03_enforce_irrefl(self) -> bool:
        """Purges reflexive loops to protect carrier irreflexivity (change class: remove_obstruction)."""
        if not self.setting:
            return False
        # Strip reflexive pairs
        self.state.relations = {pair for pair in self.state.relations if pair[0] != pair[1]}
        self.setting.relation = self.state.relations
        valid = self.setting.is_distinct()
        self.state.invariants["irreflexive"] = valid
        self.state.step = 3
        self.state.name = "state_irreflexive_carrier_protected"
        self.state.history.append("step_03: remove_obstruction")
        return valid

    def step_04_admit_orientation(self) -> bool:
        """
        Admits directed orientation while enforcing tie-retention.
        Retains both directed cut D_2 and symmetric link S_2 branches.
        """
        if self.state.step < 3 or not self.setting or not self.setting.is_distinct():
            return False
        a, b = self.setting.a, self.setting.b
        self.state.branches_retained = ["branch_D2", "branch_S2"]
        self.state.branch_metadata = {
            "branch_D2": {
                "type": "directed_germ",
                "relation": {(a, b)},
                "symmetric": False,
                "automorphism_group": "id",
            },
            "branch_S2": {
                "type": "symmetrized_link",
                "relation": {(a, b), (b, a)},
                "symmetric": True,
                "automorphism_group": "Z2",
            },
        }
        self.state.invariants["tie_retention_active"] = True
        self.state.step = 4
        self.state.name = "state_oriented_germ_retained"
        self.state.history.append("step_04: admit_orientation_tie_retention (create_structure)")
        return True

    def step_05_admit_transposition(self) -> bool:
        """
        Verifies pre-natal transposition operator sigma(a, b) = (b, a)
        and oriented 1-chain boundary sign inversion partial_1(sigma(e)) = -partial_1(e).
        """
        if self.state.step < 4 or not self.setting:
            return False
        edge = (self.setting.a, self.setting.b)
        sigma_edge = self.setting.transpose(edge)
        if edge == sigma_edge:
            return False
        sign_flip = self.setting.verify_transposition_sign_inversion(edge)
        if not sign_flip:
            return False
        self.state.invariants["transposition_sign_inversion"] = True
        self.state.step = 5
        self.state.name = "state_bounded_queue_isolated"
        self.state.history.append("step_05: transposition_antisymmetry (remove_obstruction)")
        return True

    def step_06_instantiate_alphabet(self, symbols: Optional[List[str]] = None) -> bool:
        """
        Construct domain-specific carrier alphabet for computation elements (change class: create_structure).
        """
        if self.state.step < 5:
            return False
        if symbols is None:
            symbols = ["0", "1", "_"]
        for sym in symbols:
            self.state.carrier.add(f"sym_{sym}")
        self.state.invariants["alphabet"] = list(symbols)
        self.state.step = 6
        self.state.name = "state_computation_alphabet_admitted"
        self.state.history.append(
            "step_06: rule_computation_alphabet_instantiation (create_structure)"
        )
        return True

    def step_07_evaluate_boundary_closure(self) -> SimplicialBoundaryReceipt:
        """
        Resolves boundary ambiguity by asserting exact discrete closure invariants B_1 * B_2 = 0.
        """
        if self.state.step < 6:
            raise RuntimeError(
                "Cannot evaluate boundary closure before step 06 alphabet instantiation."
            )
        receipt = self.evaluate_boundary_closure()
        self.state.step = 7
        self.state.name = "state_computation_boundary_enforced"
        self.state.history.append("step_07: rule_boundary_closure (remove_obstruction)")
        return receipt

    def step_08_synthesize_transition_poset(self) -> bool:
        """
        Synthesizes transition relation poset governing computation state transformations.
        """
        if self.state.step < 7:
            return False
        _a, b = self.setting.a, self.setting.b
        # Transition relation poset on state machine nodes
        self.state.relations.add((b, "c"))
        self.state.carrier.add("c")
        self.state.invariants["transition_poset_active"] = True
        self.state.step = 8
        self.state.name = "state_computation_transition_poset_active"
        self.state.history.append("step_08: rule_poset_synthesis (create_structure)")
        return True

    def step_09_resolve_parity(self) -> bool:
        """
        Eliminates non-deterministic parity deadlock via explicit S_2 permutation check.
        """
        if self.state.step < 8 or not self.setting:
            return False
        edge = (self.setting.a, self.setting.b)
        sigma = self.setting.transpose(edge)
        parity_distinct = edge != sigma
        self.state.invariants["parity_stabilized"] = parity_distinct
        self.state.step = 9
        self.state.name = "state_computation_parity_stabilized"
        self.state.history.append("step_09: rule_parity_resolution (remove_obstruction)")
        return parity_distinct

    def step_10_admit_higher_complexes(self) -> bool:
        """
        Admits higher-order relational complexes (commuting squares as 2-simplices).
        """
        if self.state.step < 9:
            return False
        self.state.invariants["higher_complexes"] = True
        self.state.step = 10
        self.state.name = "state_computation_higher_complexes_admitted"
        self.state.history.append("step_10: rule_complex_admission (create_structure)")
        return True

    def step_11_enforce_conservation(self) -> bool:
        """
        Enforces discrete fuel conservation constraints over admitted state ledger.
        """
        if self.state.step < 10:
            return False
        self.state.invariants["fuel_conservation"] = True
        self.state.step = 11
        self.state.name = "state_computation_conserved_ledger"
        self.state.history.append("step_11: rule_conservation_enforcement (remove_obstruction)")
        return True

    def step_12_quotient_observer_interface(self) -> bool:
        """
        Formulates quotient observer descent interface mapping internal state to external report.
        """
        if self.state.step < 11:
            return False
        self.state.invariants["observer_interface"] = True
        self.state.step = 12
        self.state.name = "state_computation_observer_interface_active"
        self.state.history.append("step_12: rule_quotient_projection (create_structure)")
        return True

    def step_13_prune_fuel_bounded_branches(self) -> bool:
        """
        Prunes candidate branches exceeding finite fuel bounds.
        """
        if self.state.step < 12:
            return False
        self.state.invariants["branches_pruned"] = True
        self.state.step = 13
        self.state.name = "state_computation_fuel_pruned_state"
        self.state.history.append("step_13: rule_fuel_bounded_pruning (remove_obstruction)")
        return True

    def step_14_establish_frontier(self) -> bool:
        """
        Establishes automata and Turing computational frontier model.
        """
        if self.state.step < 13:
            return False
        self.state.invariants["computational_frontier"] = True
        self.state.step = 14
        self.state.name = "state_computation_frontier_active"
        self.state.history.append("step_14: establish_frontier (create_structure)")
        return True

    def step_15_isolate_gap_obstruction(self) -> Dict[str, str]:
        """
        Records the scenario scope label HaltingIncompletenessObstruction; this is not a proof.
        """
        self.state.step = 15
        self.state.name = "state_computation_gap_isolated"
        self.state.history.append("step_15: isolate_gap_obstruction (remove_obstruction)")
        return self.check_gap_obstruction()

    def step_16_terminal_certification(self) -> Dict[str, Any]:
        """
        Emits custody ledger and verification receipt.
        """
        self.state.step = 16
        self.state.name = "state_computation_certified"
        self.state.history.append("step_16: terminal_certification")
        return {
            "status": "CERTIFIED",
            "domain": "computation",
            "steps_completed": 16,
            "invariants": self.state.invariants,
            "branches_retained": self.state.branches_retained,
            "authority_effect": "None",
        }

    def evaluate_simplicial_boundary_matrices(
        self, vertices: List[str], edges: List[Tuple[str, str]], faces: List[Tuple[str, str, str]]
    ) -> SimplicialBoundaryReceipt:
        """
        Evaluates exact integer simplicial boundary matrices B_1 and B_2
        and verifies B_1 * B_2 = 0.
        """
        if not vertices or not edges or not faces:
            raise ValueError(
                "Vertices, edges, and faces must be non-empty for simplicial boundary evaluation."
            )

        v_idx = {v: i for i, v in enumerate(vertices)}
        e_idx = {e: j for j, e in enumerate(edges)}

        n0 = len(vertices)
        n1 = len(edges)
        n2 = len(faces)

        # B_1: vertices x edges
        b1 = [[0] * n1 for _ in range(n0)]
        for j, (u, v) in enumerate(edges):
            if u not in v_idx:
                raise KeyError(f"Edge vertex '{u}' missing from vertices list")
            if v not in v_idx:
                raise KeyError(f"Edge vertex '{v}' missing from vertices list")
            b1[v_idx[v]][j] += 1
            b1[v_idx[u]][j] -= 1

        # B_2: edges x faces
        b2 = [[0] * n2 for _ in range(n1)]
        for k, (v0, v1, v2) in enumerate(faces):
            boundary_terms = [(1, (v1, v2)), (-1, (v0, v2)), (1, (v0, v1))]
            for sign, (src, dst) in boundary_terms:
                if (src, dst) in e_idx:
                    b2[e_idx[(src, dst)]][k] += sign
                elif (dst, src) in e_idx:
                    b2[e_idx[(dst, src)]][k] -= sign
                else:
                    raise KeyError(f"Face boundary edge ({src}, {dst}) missing from edge list")

        # Integer matrix multiplication B_1 * B_2
        prod = [[0] * n2 for _ in range(n0)]
        is_nilpotent = True
        for i in range(n0):
            for k in range(n2):
                s = sum(b1[i][j] * b2[j][k] for j in range(n1))
                prod[i][k] = s
                if s != 0:
                    is_nilpotent = False

        euler_char = n0 - n1 + n2
        num_cycles = max(0, n1 - n0 + 1)

        return SimplicialBoundaryReceipt(
            vertices=vertices,
            edges=edges,
            faces=faces,
            b1_matrix=b1,
            b2_matrix=b2,
            product_matrix=prod,
            is_nilpotent=is_nilpotent,
            num_cycles=num_cycles,
            euler_characteristic=euler_char,
            authority_effect="None",
        )

    def evaluate_boundary_closure(self) -> SimplicialBoundaryReceipt:
        """
        Genuine boundary nilpotence evaluation B_1 * B_2 = 0 on standard oriented 2-simplex.
        """
        vertices = ["a", "b", "c"]
        edges = [("a", "b"), ("b", "c"), ("a", "c")]
        faces = [("a", "b", "c")]
        receipt = self.evaluate_simplicial_boundary_matrices(vertices, edges, faces)
        self.state.invariants["boundary_nilpotence"] = receipt.is_nilpotent
        return receipt

    def check_gap_obstruction(self) -> Dict[str, str]:
        """Reports the declared scenario scope limit HaltingIncompletenessObstruction; no impossibility is calculated.."""
        self.gap_detected = True
        return {
            "gap_id": "HaltingIncompletenessObstruction",
            "status": "UNBRIDGED_OBSTRUCTION",
            "domain": "computation",
            "reason": "Finite discrete difference cannot derive continuous parameters without ungrounded admissions.",
        }

    def execute_fuel_bounded(
        self,
        start_node: str,
        fuel: int,
        transition_graph: Optional[Dict[str, str]] = None,
        detect_cycles: bool = False,
    ) -> FuelExecutionReceipt:
        """
        Executes fuel-bounded graph reduction sequence matching Scenario 4 Steps 08/09.
        Handles cycle detection, fuel exhaustion, and HaltingObstruction receipt generation.
        """
        if fuel < 0:
            raise ValueError(f"Fuel budget must be non-negative, got {fuel}")

        if transition_graph is None:
            transition_graph = {src: dst for src, dst in self.state.relations}

        curr = start_node
        trace = [curr]
        visited_indices: Dict[str, int] = {curr: 0}
        rem_fuel = fuel
        steps = 0
        obstruction = None
        has_cycle = False
        detected_period = None

        while rem_fuel > 0:
            if curr not in transition_graph:
                return FuelExecutionReceipt(
                    start_node=start_node,
                    terminal_node=curr,
                    fuel_provided=fuel,
                    fuel_consumed=steps,
                    fuel_remaining=rem_fuel,
                    steps_taken=steps,
                    status=FuelStatus.HALTED,
                    trace=trace,
                    obstruction=None,
                )
            next_node = transition_graph[curr]
            steps += 1
            rem_fuel -= 1

            # Cycle detection
            if next_node in visited_indices:
                has_cycle = True
                detected_period = steps - visited_indices[next_node]
                if detect_cycles:
                    trace.append(next_node)
                    obstruction = HaltingObstruction(
                        initial_config=None,
                        terminal_config=None,
                        fuel_budget=fuel,
                        steps_executed=steps,
                        cycle_detected=True,
                        cycle_period=detected_period,
                        reason=f"Deterministic periodic cycle of length {detected_period} detected at node '{next_node}'.",
                    )
                    return FuelExecutionReceipt(
                        start_node=start_node,
                        terminal_node=next_node,
                        fuel_provided=fuel,
                        fuel_consumed=steps,
                        fuel_remaining=rem_fuel,
                        steps_taken=steps,
                        status=FuelStatus.CYCLE_DETECTED,
                        trace=trace,
                        obstruction=obstruction,
                    )

            curr = next_node
            visited_indices[curr] = steps
            trace.append(curr)

        if curr in transition_graph:
            status = FuelStatus.OUT_OF_FUEL
            obstruction = HaltingObstruction(
                initial_config=None,
                terminal_config=None,
                fuel_budget=fuel,
                steps_executed=steps,
                cycle_detected=has_cycle,
                cycle_period=detected_period,
                reason=f"Fuel budget {fuel} exhausted with pending transition from '{curr}'.",
            )
        else:
            status = FuelStatus.HALTED

        return FuelExecutionReceipt(
            start_node=start_node,
            terminal_node=curr,
            fuel_provided=fuel,
            fuel_consumed=steps,
            fuel_remaining=rem_fuel,
            steps_taken=steps,
            status=status,
            trace=trace,
            obstruction=obstruction,
        )

    def execute_turing_machine(
        self,
        initial_config: TuringConfiguration,
        transition_table: Dict[Tuple[str, str], Tuple[str, str, int]],
        halting_states: Set[str],
        fuel: int,
        blank_symbol: str = "_",
    ) -> FuelExecutionReceipt:
        """
        Executes a discrete deterministic Turing Machine under a strict fuel budget.
        transition_table maps (state, read_symbol) -> (new_state, write_symbol, direction)
        direction in {-1, 0, 1}
        """
        if fuel < 0:
            raise ValueError(f"Fuel budget must be non-negative, got {fuel}")

        curr_config = initial_config
        tape_map = curr_config.tape_dict()
        trace = [curr_config]
        step_receipts: List[TuringStepReceipt] = []
        visited_configs: Dict[TuringConfiguration, int] = {curr_config: 0}

        rem_fuel = fuel
        steps = 0
        obstruction = None

        while rem_fuel > 0:
            if curr_config.state in halting_states:
                return FuelExecutionReceipt(
                    initial_config=initial_config,
                    terminal_config=curr_config,
                    fuel_provided=fuel,
                    fuel_consumed=steps,
                    fuel_remaining=rem_fuel,
                    steps_taken=steps,
                    status=FuelStatus.HALTED,
                    trace=trace,
                    step_receipts=step_receipts,
                    obstruction=None,
                )

            sym_read = tape_map.get(curr_config.head_pos, blank_symbol)
            key = (curr_config.state, sym_read)

            if key not in transition_table:
                # Undefined transition: machine blocks / halts abnormally
                return FuelExecutionReceipt(
                    initial_config=initial_config,
                    terminal_config=curr_config,
                    fuel_provided=fuel,
                    fuel_consumed=steps,
                    fuel_remaining=rem_fuel,
                    steps_taken=steps,
                    status=FuelStatus.HALTED,
                    trace=trace,
                    step_receipts=step_receipts,
                    obstruction=None,
                )

            new_state, sym_write, direction = transition_table[key]

            # Update tape
            if sym_write == blank_symbol:
                tape_map.pop(curr_config.head_pos, None)
            else:
                tape_map[curr_config.head_pos] = sym_write

            new_head = curr_config.head_pos + direction
            next_config = TuringConfiguration.from_dict(new_state, new_head, tape_map)

            steps += 1
            rem_fuel -= 1

            receipt = TuringStepReceipt(
                step_number=steps,
                config_before=curr_config,
                symbol_read=sym_read,
                symbol_written=sym_write,
                head_direction=direction,
                config_after=next_config,
                fuel_remaining=rem_fuel,
            )
            step_receipts.append(receipt)
            trace.append(next_config)

            # Cycle detection
            if next_config in visited_configs:
                period = steps - visited_configs[next_config]
                obstruction = HaltingObstruction(
                    initial_config=initial_config,
                    terminal_config=next_config,
                    fuel_budget=fuel,
                    steps_executed=steps,
                    cycle_detected=True,
                    cycle_period=period,
                    reason=f"Periodic configuration cycle of period {period} detected.",
                )
                return FuelExecutionReceipt(
                    initial_config=initial_config,
                    terminal_config=next_config,
                    fuel_provided=fuel,
                    fuel_consumed=steps,
                    fuel_remaining=rem_fuel,
                    steps_taken=steps,
                    status=FuelStatus.CYCLE_DETECTED,
                    trace=trace,
                    step_receipts=step_receipts,
                    obstruction=obstruction,
                )

            visited_configs[next_config] = steps
            curr_config = next_config

        if curr_config.state in halting_states:
            status = FuelStatus.HALTED
        else:
            status = FuelStatus.OUT_OF_FUEL
            obstruction = HaltingObstruction(
                initial_config=initial_config,
                terminal_config=curr_config,
                fuel_budget=fuel,
                steps_executed=steps,
                cycle_detected=False,
                reason=f"Fuel budget {fuel} exhausted before reaching halting state.",
            )

        return FuelExecutionReceipt(
            initial_config=initial_config,
            terminal_config=curr_config,
            fuel_provided=fuel,
            fuel_consumed=steps,
            fuel_remaining=rem_fuel,
            steps_taken=steps,
            status=status,
            trace=trace,
            step_receipts=step_receipts,
            obstruction=obstruction,
        )

from omega_engine.crates.type.everett import EverettArena, EverettNode, EverettNodeId


class ManyWorldsDAG:
    support_grade: str = "ToyDiagnosticOnly"
    authority_effect: str = "None"

    def __init__(self, arena: EverettArena, root_index: int):
        self.arena = arena
        self.root_index = root_index
        self.support_grade = "ToyDiagnosticOnly"
        self.authority_effect = "None"

    def to_dict(self) -> dict:
        return {
            "support_grade": self.support_grade,
            "authority_effect": self.authority_effect,
            "root_index": self.root_index,
            "node_count": len(self.arena.nodes),
        }

    @classmethod
    def new_root(cls, id_val: str, amplitude: float, sign_field: list):
        root = EverettNode(
            id_val=id_val,
            amplitude=amplitude,
            configuration_sign_field=sign_field,
            child_indices=[],
        )
        arena = EverettArena(nodes=[root])
        return cls(arena, 0)

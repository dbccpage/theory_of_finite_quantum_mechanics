"""Decisive curvature and path faults tied to independent integration cases."""
from scalar_port_faults import block


def recipes(root):
    entries = []
    def add(identity, name, prefix, before, after):
        path = root / name
        original = block(path.read_bytes().decode("utf8"), prefix)
        if original.count(before) != 1:
            raise RuntimeError("Ambiguous curvature fault: " + identity)
        entries.append({"id": identity, "source": "holonomy/" + name,
            "before": original, "after": original.replace(before, after, 1),
            "filter": "", "target": "curvature", "outcome": "unrun"})
    add("CU01-path-transport-shape", "holonomy.rs", "pub fn compute_path_holonomy", 
        "if step.rows() != connection.dim || step.cols() != connection.dim {", "if false {")
    add("CU02-subtraction", "curvature.rs", "fn matrix_difference", 
        ".sub(right.get_scalar(row, col)?)", ".add(right.get_scalar(row, col)?)")
    add("CU03-product-order", "curvature.rs", "pub fn curvature_commutator<", 
        "let p2 = m2.matmul_with_limits(m1, limits)?;", "let p2 = m1.matmul_with_limits(m2, limits)?;")
    add("CU04-both-product-costs", "curvature.rs", "pub fn curvature_commutator<", 
        ".checked_mul(4)", ".checked_mul(2)")
    add("CU05-subtraction-cost", "curvature.rs", "pub fn curvature_commutator<", 
        ".checked_add(cells)", ".checked_add(0)")
    add("CU06-inclusive-work", "curvature.rs", "fn admit_curvature_work", 
        "if requested > limits.max_operations {", "if requested >= limits.max_operations {")
    add("CU07-plaquette-direction", "curvature.rs", "pub fn plaquette_curvature<", 
        "matrix_difference(&hol, &id, &connection.limits)", "matrix_difference(&id, &hol, &connection.limits)")
    add("CU08-path-work-policy", "holonomy.rs", "pub fn compute_path_holonomy", 
        "step_mat.matmul_with_limits(&current, &connection.limits)?", "step_mat.matmul(&current)?")
    return entries

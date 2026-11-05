from witnessed_difference.proved_rows import replay_proved_rows


def test_replay_calls_the_shipped_finite_checks() -> None:
    report = replay_proved_rows()
    assert report["ok"] is True
    pointed = report["WDP-CH01-P02"]
    assert pointed["total"] == 4674
    assert pointed["related"] == 2337
    assert pointed["related_and_irreflexive"] == 196
    assert pointed["distinct"] == 3104
    assert pointed["matches_enumeration"] is True
    assert pointed["related_loop_not_distinct"] == [True, False]
    assert pointed["distinct_empty_not_related"] == [False, True]
    assert pointed["irreflexive_related_not_distinct"] == 0
    assert report["WDP-CH03-P01"] == {
        "fixed_points_at_least_two": [],
        "fixed_point_of_singleton": [0],
    }
    assert report["WDP-CH07-P01"] == {"left": "3/2", "right": "3/2", "joined": "3"}
    path = report["WDP-CH07-P02"]
    assert path["reconstructed"] == {"a-b": "1", "b-c": "1", "a-c": "2"}
    assert path["direct"] == path["long_path"] == "2"
    pairs = report["WDP-CH10-P02"]["pairs"]
    assert ("identity", "zero") in pairs
    assert ("zero", "identity") not in pairs
    assert ("identity", "identity") in pairs
    grammar = report["WDP-CH10-P03"]
    assert (grammar["core_classes"], grammar["capacity"], grammar["visible_classes"]) == (4, 3, 3)
    assert grammar["collision"] == ["q1", "q3"]
    assert grammar["pigeonhole_forced"] is True
    assert report["WDP-CH14-P01"] == {"same_output": True, "points_distinct": True}
    descent = report["WDP-CH16-P01"]
    assert descent["forgotten_obstruction"] > 0
    assert descent["remembered_unique"] is True
    assert descent["remembered_factor"] == [[0, 0], [1, 1]]
    assert report["WDP-CH16-P02"]["forgotten_obstruction"] > 0
    corner = report["WDP-CH18-P02"]
    assert corner["identity_stochastic"] == corner["identity_permutation"] == 1
    assert corner["average_stochastic"] == 1
    assert corner["average_permutation"] == 0
    shear = report["WDP-CH18-P03"]
    assert shear["inverse_product"] == ((1, 0), (0, 1))
    assert shear["image_of_basis"] == ["2", "-1"]
    assert shear["column_sums"] == ["1", "1"]
    assert shear["permutation"] == 0
    census = report["WDP-CH18-P04"]
    assert census["carrier"] == 2
    assert census["unitary_matrices"] == census["monomial_unitaries"] > 0
    corner_end = report["WDP-CH18-P05"]
    assert corner_end["hadamard_gram"] == [["2", "0"], ["0", "2"]]
    assert corner_end["hadamard_readouts_differ"] is True
    assert corner_end["pythagorean_gram"] == [["1", "0"], ["0", "1"]]
    assert corner_end["half_gram"] == [["1", "0"], ["0", "1"]]
    assert corner_end["half_square"] == [["0", "1"], ["1", "0"]]
    mixture = report["WDP-CH18-P07"]
    assert mixture["average_mixture"] == [["1/2", "1/2"], ["1/2", "1/2"]]
    assert mixture["average_weight_sum"] == "1"
    assert mixture["average_weights_nonnegative"] == 1
    assert mixture["identity_mixture"] == [["1", "0"], ["0", "1"]]
    assert mixture["identity_weight_sum"] == "1"
    assert mixture["product_stochastic"] == 1
    povm = report["WDP-CH19-P14"]
    assert povm["effects_equal"] is True
    assert povm["luders_complete"] is True
    assert povm["prepare_complete"] is True
    assert povm["luders_post"] == ["1", "0"]
    assert povm["prepare_post"] == ["3/5", "4/5"]
    assert povm["posts_parallel"] is False

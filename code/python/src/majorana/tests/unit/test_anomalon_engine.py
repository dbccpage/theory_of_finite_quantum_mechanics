from omega_engine.crates.runtime.rt_anomalon_review import (
    calculate_basic_metrics,
    calculate_signal_metrics,
    build_text_density_matrix,
    run_anomalon_review,
)


def test_anomalon_basic_metrics():
    text = "Write a clear prompt. Write it now!"
    metrics = calculate_basic_metrics(text)

    assert metrics["charCount"] == len(text)
    assert metrics["wordCount"] == 7
    assert metrics["sentenceCount"] == 2
    assert metrics["uniqueWordRatio"] > 0.5
    assert metrics["avgWordLength"] > 0.0


def test_anomalon_signal_metrics():
    text = "Write a clear prompt. Write it now! Maybe it seems uncertain."
    metrics = calculate_signal_metrics(text)

    assert metrics["questionCount"] == 0
    assert (
        metrics["imperativeCount"] == 2
    )  # "Write" starts both the first and second sentences
    assert metrics["hedgeCount"] >= 2  # "maybe", "seems", "uncertain"
    assert metrics["charEntropy"] > 0.0
    assert metrics["wordEntropy"] > 0.0


def test_anomalon_density_matrix():
    basic = calculate_basic_metrics("Test document.")
    signal = calculate_signal_metrics("Test document.")
    density = build_text_density_matrix(basic, signal)

    assert "purity" in density
    assert "vonNeumannEntropy" in density
    assert "l1Coherence" in density
    assert len(density["eigenvalues"]) == 4


def test_anomalon_review_run():
    text = "Write a clear prompt. Write it now! Maybe it seems uncertain."
    result = run_anomalon_review("prompt", text)

    assert "terminalStatus" in result
    assert "metrics" in result
    assert "density" in result
    assert "obstruction" in result
    assert "certificate" in result
    assert "advice" in result




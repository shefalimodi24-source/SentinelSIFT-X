from graph.state import SentinelState


def _score_benchmark(state: SentinelState):
    expected = set(state.get("ground_truth", []))

    if not expected:
        state["benchmark_results"] = {}
        return

    verified = {
        item["finding"]
        for item in state["verified_findings"]
    }

    matched = expected.intersection(verified)
    scored_detected = verified.intersection(expected)

    precision = (
        len(matched) / len(scored_detected)
        if scored_detected
        else 0
    )

    recall = len(matched) / len(expected)
    detection_rate = recall

    state["benchmark_results"] = {
        "precision": precision,
        "recall": recall,
        "detection_rate": detection_rate
    }


def _format_percent(value):
    return f"{value * 100:.0f}%"


def report_agent(state: SentinelState):
    _score_benchmark(state)

    for item in state["verified_findings"]:

        print("Finding:", item["finding"])

        print("Evidence:")

        for e in item["evidence"]:
            print(" -", e)

        print(
            "Confidence:",
            state["confidence_scores"][item["finding"]]
        )

        print()
    print("\nRecommended Tools:")

    print("\nRecommended Tools:")

    for tool in state["tool_recommendations"]:
        print(" -", tool)

    print("\nTool Execution Results:")

    for item in state.get("new_evidence", []):
        print(" -", item)
    print("Reasoning Log:")

    for log in state["reasoning_log"]:
        print("-", log)

    if state["benchmark_results"]:
        print("\nBenchmark Results:")
        print(
            "Detection Rate:",
            _format_percent(
                state["benchmark_results"]["detection_rate"]
            )
        )
        print(
            "Precision:",
            _format_percent(
                state["benchmark_results"]["precision"]
            )
        )
        print(
            "Recall:",
            _format_percent(
                state["benchmark_results"]["recall"]
            )
        )

    return state
    
    

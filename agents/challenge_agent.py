from graph.state import SentinelState


def challenge_agent(state: SentinelState):
    results = []

    confidence_scores = {}

    for finding in state["findings"]:

        source_count = len(
            finding.get("sources", [])
        )

        confidence = 0.90

        issues = []

        if source_count <= 1:

            confidence = 0.60

            issues.append(
                "Single-source evidence"
            )

        results.append({
            "finding": finding["finding"],
            "confidence": confidence,
            "issues": issues
        })

        confidence_scores[
            finding["finding"]
        ] = confidence

    state["challenge_results"] = results

    state["confidence_scores"] = confidence_scores

    state["reasoning_log"].append(
        "Challenge Agent reviewed findings"
    )

    return state
    
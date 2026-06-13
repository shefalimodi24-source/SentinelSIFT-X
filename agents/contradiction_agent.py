from graph.state import SentinelState


def contradiction_agent(state: SentinelState):
    contradictions = []

    for finding in state["findings"]:

        sources = finding.get("sources", [])

        if len(sources) == 1:

            contradictions.append(
                f"Weakly supported finding: {finding['finding']}"
            )

    if contradictions:

        state["reasoning_log"].append(
            "Contradiction Agent detected weak findings"
        )

    else:

        state["reasoning_log"].append(
            "Contradiction Agent found no issues"
        )
    state["contradictions"] = contradictions

    return state

from graph.state import SentinelState


def correlation_agent(state: SentinelState):
    merged = {}

    for item in state["findings"]:

        finding = item["finding"]

        if finding not in merged:

            merged[finding] = {
                "finding": finding,
                "evidence": [],
                "sources": []
            }

        merged[finding]["evidence"].extend(
            item["evidence"]
        )

        merged[finding]["sources"].append(
            item.get("source", "unknown")
        )

    state["findings"] = list(merged.values())

    state["reasoning_log"].append(
        "Correlation Agent merged findings"
    )

    return state
    

from graph.state import SentinelState


def tool_selection_agent(state: SentinelState):

    recommendations = set()

    for finding in state["verified_findings"]:

        name = finding["finding"].lower()

        if "powershell" in name:

            recommendations.add("EvtxECmd")
            recommendations.add("PECmd")

        if "persistence" in name:

            recommendations.add("AmcacheParser")
            recommendations.add("AppCompatCacheParser")

    state["tool_recommendations"] = list(recommendations)

    state["reasoning_log"].append(
        f"Tool Selector chose {len(recommendations)} tools"
    )

    return state
    
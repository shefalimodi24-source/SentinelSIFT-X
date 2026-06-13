from graph.state import SentinelState


def verifier_agent(state: SentinelState):
    verified = []
    confidence = {}

    for item in state["findings"]:

        if item["sources"] == ["tool_executor"]:

            verified.append(item)

            confidence[item["finding"]] = 0.95
            continue


        evidence = item["evidence"]

        if len(evidence) > 0:

            verified.append(item)

            confidence[item["finding"]] = 0.90

    state["verified_findings"] = verified
    state["confidence_scores"] = confidence

    state["reasoning_log"].append(
        f"Verifier approved {len(verified)} findings"
    )

    return state
    
    
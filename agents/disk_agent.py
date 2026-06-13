from graph.state import SentinelState


def disk_agent(state: SentinelState):
    findings = state["findings"]

    case_data = state["case_data"].lower()

    if "autorun" in case_data:

        findings.append(
            {
                "finding": "Persistence mechanism detected",
                "source": "disk",
                "evidence": [
                    "autorun registry entry"
                ]
            }
        )

    state["findings"] = findings

    state["reasoning_log"].append(
        "Disk Agent completed analysis"
    )

    return state
    
from graph.state import SentinelState


def log_agent(state: SentinelState):
    findings = state["findings"]

    case_data = state["case_data"].lower()

    if "powershell" in case_data:

        findings.append(
            {
                "finding": "PowerShell execution detected",
                "source": "logs",
                "evidence": [
                    "event id 4688"
                ]
            }
        )

    state["findings"] = findings

    state["reasoning_log"].append(
        "Log Agent completed analysis"
    )

    return state
    
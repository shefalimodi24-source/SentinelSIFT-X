from graph.state import SentinelState


def memory_agent(state: SentinelState):
    findings = state["findings"]

    case_data = state["case_data"].lower()

    if "powershell" in case_data:

        findings.append(
            {
                "finding": "PowerShell execution detected",
                "source": "memory",
                "evidence": [
                    "powershell.exe process"
                ]
            }
        )

    state["findings"] = findings

    state["reasoning_log"].append(
        "Memory Agent completed analysis"
    )

    return state
    
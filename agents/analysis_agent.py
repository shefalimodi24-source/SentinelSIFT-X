from graph.state import SentinelState


def analysis_agent(state: SentinelState):

    case_data = state["case_data"]

    findings = []

    if "powershell" in case_data.lower():

        findings.append(
            {
                "finding": "Suspicious PowerShell activity detected",
                "evidence": [
                    "powershell.exe process",
                    "event id 4688"

                ]
            }
        )

    if "autorun" in case_data.lower():

        findings.append(
            {
                "finding": "Potential persistence mechanism found",
                "evidence": [
                    "autorun registry entry"
                ]
            }
        )

    state["findings"] = findings

    state["reasoning_log"].append(
        f"Analysis Agent identified {len(findings)} findings"
    )

    return state

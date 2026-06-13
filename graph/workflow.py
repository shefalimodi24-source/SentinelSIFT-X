from graph.state import SentinelState

from agents.analysis_agent import analysis_agent
from agents.verifier_agent import verifier_agent
from agents.report_agent import report_agent


def run_workflow():

    state: SentinelState = {
        "case_data": """
        powershell.exe launched
        suspicious autorun entry detected
        """,
        "findings": [],
        "verified_findings": [],
        "confidence_scores": {},
        "reasoning_log": [],
        "retry_count": 0
    }

    state = analysis_agent(state)

    for _ in range(3):

        state = verifier_agent(state)

        if len(state["verified_findings"]) == len(state["findings"]):
            break

        state["retry_count"] += 1

        state["reasoning_log"].append(
            "Verifier rejected findings. Re-analysis triggered."
        )

    state = report_agent(state)


if __name__ == "__main__":
    run_workflow()
    
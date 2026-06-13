import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT))

from data.case_loader import load_case

from agents.memory_agent import memory_agent
from agents.disk_agent import disk_agent
from agents.log_agent import log_agent
from agents.correlation_agent import correlation_agent
from agents.verifier_agent import verifier_agent
from agents.report_agent import report_agent
from agents.protocol_sift_agent import protocol_sift_agent
from agents.windows_artifact_agent import windows_artifact_agent
from graph.langgraph_workflow import workflow

def analyze_case(case_file):

    case = load_case(case_file)

    case_data = " ".join(
        item.value
        for item in case["evidence"]
    )

    state = {
        "case_data": case_data,
        "evidence": case["evidence"],
        "findings": [],
        "verified_findings": [],
        "confidence_scores": {},
        "reasoning_log": [],
        "retry_count": 0,
        "contradictions": [],
        "challenge_results": [],
        "tool_recommendations": [],
        "benchmark_results": {},
        "new_evidence": [],
        "ground_truth": case["ground_truth"]
    }

    final_state = workflow.invoke(state)

    return final_state

if __name__ == "__main__":

    analyze_case("data/case3.json")


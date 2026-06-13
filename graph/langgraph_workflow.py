from typing import Literal
from langgraph.graph import StateGraph, END
from graph.state import SentinelState
from agents.memory_agent import memory_agent
from agents.disk_agent import disk_agent
from agents.log_agent import log_agent
from agents.correlation_agent import correlation_agent
from agents.challenge_agent import challenge_agent
from agents.contradiction_agent import contradiction_agent
from agents.verifier_agent import verifier_agent
from agents.report_agent import report_agent
from agents.protocol_sift_agent import protocol_sift_agent
from agents.windows_artifact_agent import windows_artifact_agent
from agents.tool_selection_agent import tool_selection_agent
from agents.tool_executor_agent import tool_executor_agent


def _debug_node(name, node):
    def wrapped(state: SentinelState):
        print(
            f"[debug] ENTER {name}: "
            f"findings={len(state.get('findings', []))}, "
            f"verified={len(state.get('verified_findings', []))}, "
            f"retry_count={state.get('retry_count')}",
            flush=True
        )

        result = node(state)

        print(
            f"[debug] EXIT {name}: "
            f"findings={len(result.get('findings', []))}, "
            f"verified={len(result.get('verified_findings', []))}, "
            f"retry_count={result.get('retry_count')}",
            flush=True
        )

        return result

    return wrapped


def verification_router(
    state: SentinelState
) -> Literal["tool_selector", "memory"]:

    print(
        f"[debug] ROUTER verifier: "
        f"findings={len(state['findings'])}, "
        f"verified={len(state['verified_findings'])}, "
        f"retry_count={state['retry_count']}",
        flush=True
    )

    if len(state["verified_findings"]) == len(state["findings"]):
        print("[debug] ROUTER verifier -> tool_selector", flush=True)
        return "tool_selector"

    if state["retry_count"] >= 3:
        print("[debug] ROUTER verifier -> tool_selector", flush=True)
        return "tool_selector"

    state["retry_count"] += 1

    state["reasoning_log"].append(
        "Verifier rejected findings. Re-analysis triggered."
    )

    print("[debug] ROUTER verifier -> memory", flush=True)
    return "memory"


graph = StateGraph(SentinelState)

graph.add_node("memory", _debug_node("memory", memory_agent))
graph.add_node("disk", _debug_node("disk", disk_agent))
graph.add_node("logs", _debug_node("logs", log_agent))
graph.add_node("correlation", _debug_node("correlation", correlation_agent))
graph.add_node("challenge", _debug_node("challenge", challenge_agent))
graph.add_node("contradiction", _debug_node("contradiction", contradiction_agent))
graph.add_node("verifier", _debug_node("verifier", verifier_agent))
graph.add_node("post_tool_verifier", _debug_node("post_tool_verifier", verifier_agent))
graph.add_node("report", _debug_node("report", report_agent))
graph.add_node(
    "protocol_sift",
    _debug_node("protocol_sift", protocol_sift_agent)
)
graph.add_node(
    "tool_selector",
    _debug_node("tool_selector", tool_selection_agent)
)
graph.add_node(
    "windows_artifacts",
    _debug_node("windows_artifacts", windows_artifact_agent)
)
graph.add_node(
    "tool_executor",
    _debug_node("tool_executor", tool_executor_agent)
)
graph.set_entry_point("memory")

graph.add_edge("memory", "disk")
graph.add_edge("disk", "logs")
graph.add_edge("logs", "protocol_sift")


graph.add_edge(
    "protocol_sift",
    "windows_artifacts"
)

graph.add_edge(
    "windows_artifacts",
    "correlation"
)


graph.add_edge("correlation", "challenge")
graph.add_edge("challenge", "contradiction")
graph.add_edge("contradiction", "verifier")

graph.add_conditional_edges(
    "verifier",
    verification_router,
    {
        "memory": "memory",
        "tool_selector": "tool_selector"
    }
)
graph.add_edge(
    "tool_selector",
    "tool_executor"
)

graph.add_edge(
    "tool_executor",
    "post_tool_verifier"
)

graph.add_edge(
    "post_tool_verifier",
    "report"
)

graph.add_edge(
    "report",
    END
)


workflow = graph.compile()


if __name__ == "__main__":

    state = {
        "case_data": """
        powershell.exe launched
        suspicious autorun entry detected
        """,

        "findings": [],
        "verified_findings": [],
        "confidence_scores": {},
        "reasoning_log": [],
        "retry_count": 0,
        "contradictions": [],

        "challenge_results": [],
        "tool_recommendations": [],
        "executed_tools": [],
        "new_evidence": [],
        "benchmark_results": {},
        "ground_truth": [],
        "new_evidence": []
    }

    print("[debug] INVOKE workflow", flush=True)
    workflow.invoke(state)
    print("[debug] WORKFLOW completed", flush=True)

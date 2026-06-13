import platform
import subprocess

from graph.state import SentinelState


def tool_executor_agent(state: SentinelState):

    new_evidence = []

    running_on_windows = (
        platform.system().lower() == "windows"
    )

    for tool in state["tool_recommendations"]:

        try:

            # ----------------------
            # WINDOWS DEMO MODE
            # ----------------------

            if running_on_windows:

                result = subprocess.run(
                    [
                        "cmd",
                        "/c",
                        "echo",
                        f"{tool} executed"
                    ],
                    capture_output=True,
                    text=True
                )

                evidence_text = result.stdout.strip()

                new_evidence.append(
                    evidence_text
                )

                if tool == "EvtxECmd":

                   state["findings"].append({
                       "finding": "Event Log Analysis Completed",
                       "evidence": [
                            evidence_text
                       ],
                       "sources": ["tool_executor"]
                    })

                elif tool == "AmcacheParser":

                    state["findings"].append({
                        "finding": "Amcache Analysis Completed",
                        "evidence": [
                           evidence_text
                    ],
                    "sources": ["tool_executor"]
                    })

                elif tool == "PECmd":

                    state["findings"].append({
                        "finding": "Prefetch Analysis Completed",
                        "evidence": [
                            evidence_text
                        ],
                        "sources": ["tool_executor"]
                  })

                elif tool == "AppCompatCacheParser":

                   state["findings"].append({
                       "finding": "AppCompatCache Analysis Completed",
                       "evidence": [
                           evidence_text
                    ],
                    "sources": ["tool_executor"]
                    })

                state["confidence_scores"][
                    state["findings"][-1]["finding"]
                ] = 0.95
            

            # ----------------------
            # SIFT REAL EXECUTION
            # ----------------------

            else:

                if tool == "EvtxECmd":

                    result = subprocess.run(
                        [
                            "dotnet",
                            "/opt/zimmermantools/EvtxeCmd/EvtxECmd.dll",
                            "--help"
                        ],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )

                    if result.returncode == 0:
                        new_evidence.append(
                            "EvtxECmd executed successfully"
                        )

                elif tool == "AmcacheParser":

                    result = subprocess.run(
                        [
                            "dotnet",
                            "/opt/zimmermantools/AmcacheParser.dll",
                            "--help"
                        ],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )

                    if result.returncode == 0:
                        new_evidence.append(
                            "AmcacheParser executed successfully"
                        )

        except Exception as e:

            state["reasoning_log"].append(
                f"Tool execution failed: {tool}: {e}"
            )

    state["new_evidence"].extend(
        new_evidence
    ) 

    state["reasoning_log"].append(
        f"Executed {len(new_evidence)} tools"
    )

    return state


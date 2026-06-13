def windows_artifact_agent(state):
    recommendations = set()


    for finding in state["findings"]:

        name = finding["finding"].lower()

        if "powershell" in name:

            recommendations.add(
                "Run EvtxECmd.dll against Security.evtx"
            )

            recommendations.add(
                "Run PECmd.dll against Prefetch artifacts"
            )

        if "persistence" in name:

            recommendations.add(
                "Run AmcacheParser.dll"
            )

            recommendations.add(
                "Run AppCompatCacheParser.dll"
            )

    if recommendations:

        state["findings"].append({
            "finding": "Protocol SIFT Investigation Plan",
            "evidence": list(recommendations),
            "sources": ["protocol_sift"]
        })

    state["reasoning_log"].append(
        "Windows Artifact Agent generated investigation plan"
    )

    return state

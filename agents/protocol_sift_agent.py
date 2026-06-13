import json


def protocol_sift_agent(state):
    with open("data/protocol_sift_skills.json") as f:
        data = json.load(f)

    findings = []

    for skill in data["skills"]:

        findings.append({
            "finding": f"Protocol SIFT Skill Available: {skill}",
            "evidence": [skill],
            "source": "protocol_sift"
        })

    state["findings"].extend(findings)

    state["reasoning_log"].append(
        f"Protocol SIFT loaded {len(findings)} skills"
    )

    return state
    
from data.evidence import Evidence


def parse_case(case_json):

    evidence = []

    for artifact in case_json["artifacts"]:

        if "powershell" in artifact.lower():

            evidence.append(
                Evidence(
                    source="memory",
                    artifact_type="process",
                    value=artifact
                )
            )

        elif "event id" in artifact.lower():

            evidence.append(
                Evidence(
                    source="logs",
                    artifact_type="event",
                    value=artifact
                )
            )

        elif "autorun" in artifact.lower():

            evidence.append(
                Evidence(
                    source="disk",
                    artifact_type="registry",
                    value=artifact
                )
            )

    return evidence
    
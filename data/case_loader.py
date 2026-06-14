import json
import csv
from pathlib import Path
from data.artifact_parser import parse_case
from data.evidence import Evidence


ARTIFACT_SOURCE = {
    "evtx": "logs",
    "prefetch": "disk",
    "amcache": "disk",
}


ARTIFACT_TYPE = {
    "evtx": "event",
    "prefetch": "prefetch",
    "amcache": "amcache",
}


def _record_value(artifact_type, record):
    values = [
        value.strip()
        for value in record.values()
        if value and value.strip()
    ]

    return f"{artifact_type.upper()} CSV record: " + " | ".join(values)


def _load_artifact_csv(case_dir, artifact_file):
    artifact_type = artifact_file["type"].lower()

    if artifact_type not in ARTIFACT_SOURCE:
        raise ValueError(f"Unsupported artifact type: {artifact_type}")

    # For the hackathon demo, artifact files are always loaded from the repository's data/artifacts folder.
    # The path in artifact_file["path"] is relative to the 'data' directory.
    path = Path("data") / artifact_file["path"]

    evidence = []

    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)

        for record in reader:
            evidence.append(
                Evidence(
                    source=ARTIFACT_SOURCE[artifact_type],
                    artifact_type=ARTIFACT_TYPE[artifact_type],
                    value=_record_value(artifact_type, record)
                )
            )

    return evidence


def _load_ground_truth(case_path):
    # The ground truth JSON is expected to be in a 'ground_truth' subdirectory
    # sibling to the 'data' directory, with a name derived from the case file.
    # For uploaded cases, we assume they are temporary and will not have an associated ground truth.
    # Therefore, we return an empty list for ground truth.
    return []


def load_case(path):

    case_path = Path(path)

    with open(case_path, "r") as f:
        data = json.load(f)

    evidence = parse_case(data)

    for artifact_file in data.get("artifact_files", []):
        evidence.extend(
            _load_artifact_csv(
                case_path.parent,
                artifact_file
            )
        )

    return {
        "case_id": data["case_id"],
        "hostname": data["hostname"],
        "evidence": evidence,
        "ground_truth": _load_ground_truth(case_path)
    }


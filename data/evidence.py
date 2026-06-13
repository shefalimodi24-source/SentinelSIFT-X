from dataclasses import dataclass


@dataclass
class Evidence:

    source: str

    artifact_type: str

    value: str
    
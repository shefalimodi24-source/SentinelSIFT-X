from typing import TypedDict, List, Dict


class SentinelState(TypedDict):

    case_data: str

    findings: List[Dict]

    verified_findings: List[Dict]

    confidence_scores: Dict[str, float]

    reasoning_log: List[str]

    retry_count: int

    contradictions: List[str]

    challenge_results: List[Dict]

    tool_recommendations: List[str]

    new_evidence: List[str]

    benchmark_results: Dict[str, float]

    ground_truth: List[str]
    
    


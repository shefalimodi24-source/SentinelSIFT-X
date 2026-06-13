import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from agents.memory_agent import memory_agent
from agents.disk_agent import disk_agent
from agents.log_agent import log_agent
from agents.correlation_agent import correlation_agent
from agents.verifier_agent import verifier_agent


def run_case(case_data):

    state = {
        "case_data": case_data,
        "findings": [],
        "verified_findings": [],
        "confidence_scores": {},
        "reasoning_log": [],
        "retry_count": 0,
        "contradictions": []
    }

    state = memory_agent(state)
    state = disk_agent(state)
    state = log_agent(state)
    state = correlation_agent(state)
    state = verifier_agent(state)

    return [
        item["finding"]
        for item in state["verified_findings"]
    ]


def benchmark():

    with open(
        ROOT / "benchmarks" / "test_cases.json",
        "r"
    ) as f:

        tests = json.load(f)

    total = len(tests)
    passed = 0

    print("\n===== BENCHMARK RESULTS =====\n")

    for test in tests:

        predicted = run_case(
            test["case_data"]
        )

        expected = test["expected_findings"]

        success = set(predicted) == set(expected)

        if success:
            passed += 1

        print(f"Test: {test['name']}")
        print("Expected:", expected)
        print("Predicted:", predicted)
        print("PASS" if success else "FAIL")
        print()

    accuracy = (passed / total) * 100

    print(f"Overall Accuracy: {accuracy:.2f}%")
    print(f"Passed: {passed}/{total}")


if __name__ == "__main__":
    benchmark()
    
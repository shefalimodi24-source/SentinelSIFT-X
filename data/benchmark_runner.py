import contextlib
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT))

from data.run_case import analyze_case


METRICS = [
    ("detection_rate", "Detection Rate"),
    ("precision", "Precision"),
    ("recall", "Recall"),
]


def _format_percent(value):
    return f"{value * 100:g}%"


def _run_case(case_path):
    with contextlib.redirect_stdout(io.StringIO()):
        state = analyze_case(str(case_path))

    return state["benchmark_results"]


def _case_label(case_path):
    case_number = case_path.stem.replace("case", "")

    if case_number.isdigit():
        return f"Case {int(case_number)}"

    return case_path.stem


def _average(results, metric):
    if not results:
        return 0

    return sum(result.get(metric, 0) for result in results) / len(results)


def main():
    case_paths = sorted((ROOT / "data").glob("case*.json"))
    results = []

    for case_path in case_paths:
        benchmark_results = _run_case(case_path)
        results.append(benchmark_results)

        print(f"{_case_label(case_path)}:")

        for metric, label in METRICS:
            print(
                f"{label}: "
                f"{_format_percent(benchmark_results.get(metric, 0))}"
            )

        print()

    print("Overall:")

    for metric, label in METRICS:
        print(
            f"{label}: "
            f"{_format_percent(_average(results, metric))}"
        )


if __name__ == "__main__":
    main()

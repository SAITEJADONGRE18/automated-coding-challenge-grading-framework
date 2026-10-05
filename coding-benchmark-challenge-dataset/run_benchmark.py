import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROBLEMS_PATH = ROOT / "dataset" / "problems.json"
TESTS_PATH = ROOT / "tests" / "test_cases.json"

REFERENCE_MODULES = {
    "P001": ("reference_solutions/p001_two_sum_sorted.py", "two_sum_sorted"),
    "P002": ("reference_solutions/p002_longest_unique_substring.py", "longest_unique_substring"),
    "P003": ("reference_solutions/p003_merge_intervals.py", "merge_intervals"),
    "P004": ("reference_solutions/p004_shortest_path_grid.py", "shortest_path_grid"),
    "P005": ("reference_solutions/p005_range_sum_query.py", "range_sum_queries"),
}

def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    parser = argparse.ArgumentParser(description="Run the coding challenge benchmark.")
    parser.add_argument("--submission", help="Path to a Python file implementing all five required functions.")
    parser.add_argument("--public-only", action="store_true", help="Run only tests marked public.")
    args = parser.parse_args()

    problems = json.loads(PROBLEMS_PATH.read_text(encoding="utf-8"))
    cases_by_problem = json.loads(TESTS_PATH.read_text(encoding="utf-8"))
    if args.submission:
        candidate_path = Path(args.submission).resolve()
        if not candidate_path.is_file():
            print(f"Submission file not found: {candidate_path}", file=sys.stderr)
            return 2
        module = load_module(candidate_path, "candidate_submission")
        source = "submission"
    else:
        module = None
        source = "reference"

    report = {"source": source, "total": 0, "passed": 0, "failed": 0, "problems": []}
    all_ok = True

    for problem in problems:
        pid = problem["id"]
        rel_path, function_name = REFERENCE_MODULES[pid]
        if module is None:
            solution_module = load_module(ROOT / rel_path, f"ref_{pid.lower()}")
            function = getattr(solution_module, function_name)
        else:
            function = getattr(module, function_name, None)
            if function is None:
                print(f"ERROR: submission is missing function {function_name} for {pid}", file=sys.stderr)
                return 2

        p_report = {"id": pid, "title": problem["title"], "passed": 0, "failed": 0, "cases": []}
        for idx, case in enumerate(cases_by_problem[pid], start=1):
            if args.public_only and case.get("visibility") != "public":
                continue
            report["total"] += 1
            started = time.perf_counter()
            try:
                actual = function(**case["input"])
                expected = case["expected"]
                ok = actual == expected
                error = None
                if not ok:
                    error = f"Expected {expected!r}, got {actual!r}"
            except Exception as exc:
                ok = False
                error = f"{type(exc).__name__}: {exc}"
            elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
            case_result = {"case": idx, "visibility": case.get("visibility", "unspecified"),
                           "passed": ok, "elapsed_ms": elapsed_ms}
            if error:
                case_result["error"] = error
            p_report["cases"].append(case_result)
            if ok:
                report["passed"] += 1
                p_report["passed"] += 1
            else:
                report["failed"] += 1
                p_report["failed"] += 1
                all_ok = False
        report["problems"].append(p_report)
        print(f"{pid} | {problem['title']}: {p_report['passed']}/{p_report['passed'] + p_report['failed']} passed")

    report["pass_rate"] = round(report["passed"] / report["total"], 4) if report["total"] else 0
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / "latest_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nOverall: {report['passed']}/{report['total']} passed ({report['pass_rate'] * 100:.1f}%)")
    print(f"Report written to: {reports_dir / 'latest_report.json'}")
    return 0 if all_ok else 1

if __name__ == "__main__":
    raise SystemExit(main())

# Coding Benchmark & Challenge Dataset

A GitHub-ready starter benchmark for evaluating programming problem-solving quality. It includes problem statements, constraints, examples, reference implementations, public and hidden-style edge cases, complexity targets, common incorrect approaches, and an automated grading harness.

## What's included

- **5 programming challenges** spanning arrays, strings, intervals, graphs, and data structures.
- Structured problem metadata in `dataset/problems.json`.
- Reference solutions in `reference_solutions/`.
- Public and additional tests in `tests/`.
- A local grader that checks function signatures and compares results against expected outputs.
- A small benchmark report showing pass rate and per-problem results.

## Requirements

- Python 3.10+
- No third-party packages required.

## Run the reference solutions

From the project root:

```bash
python run_benchmark.py
```

This runs the bundled reference implementations against all bundled tests. It should pass all tests.

## Grade your own solution

1. Open `submissions/solution_template.py`.
2. Implement the required functions using the exact function names and signatures.
3. Run:

```bash
python run_benchmark.py --submission submissions/solution_template.py
```

The grader prints per-problem results and a JSON report at `reports/latest_report.json`.

**Important:** This is a local educational grader, not a secure online judge. It imports Python submissions in-process. Only run code you trust. For a production service, run untrusted submissions in an isolated container with CPU, memory, filesystem, and network restrictions.

## Dataset design

Each problem record includes:
- `id`, `title`, `difficulty`, `tags`
- `statement`, `input_format`, `output_format`
- `constraints`, `examples`
- `function_name`, `signature`
- `target_complexity`
- `common_wrong_approaches`
- `grading_notes`

Tests use direct function calls and expected return values. This makes the dataset easy to adapt to other languages or an API-based evaluation pipeline.

## Project structure

```text
coding-benchmark-challenge-dataset/
├── dataset/
│   └── problems.json
├── reference_solutions/
│   ├── p001_two_sum_sorted.py
│   ├── p002_longest_unique_substring.py
│   ├── p003_merge_intervals.py
│   ├── p004_shortest_path_grid.py
│   └── p005_range_sum_query.py
├── tests/
│   └── test_cases.json
├── submissions/
│   └── solution_template.py
├── reports/
│   └── .gitkeep
├── run_benchmark.py
├── requirements.txt
├── LICENSE
└── .gitignore
```

## Adding a problem

1. Add its specification to `dataset/problems.json`.
2. Add a reference implementation under `reference_solutions/`.
3. Add cases to `tests/test_cases.json`.
4. Add the function to `submissions/solution_template.py`.
5. Run the benchmark and verify that the reference solution passes.

## Scope and limitations

This release is a complete **baseline dataset and grading framework**, not a statistically validated benchmark. It does not claim calibrated difficulty, broad language coverage, adversarial security, or independent expert review. Before using it to rank models or candidates, add more problems, independently review expected outputs, and test against deliberately incorrect submissions.

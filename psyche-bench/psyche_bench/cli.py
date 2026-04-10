"""
psyche-bench CLI — Benchmark suite for music recommendation systems.

Usage:
    psyche-bench download-data --dataset fma-small
    psyche-bench evaluate --model my_model.py --dataset fma-small --output results.json
    psyche-bench show-results --input results.json
"""

import argparse
import json
import sys
from pathlib import Path


def main():
    """CLI entry point for psyche-bench."""
    parser = argparse.ArgumentParser(
        prog="psyche-bench",
        description="PSYCHE Benchmark Suite — Evaluate music recommendation systems",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # download-data
    dl_parser = subparsers.add_parser("download-data", help="Download benchmark datasets")
    dl_parser.add_argument(
        "--dataset",
        choices=["fma-small", "fma-medium"],
        default="fma-small",
        help="Dataset to download",
    )

    # evaluate
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate a recommender model")
    eval_parser.add_argument("--model", required=True, help="Path to model Python file")
    eval_parser.add_argument("--dataset", default="fma-small", help="Dataset to evaluate against")
    eval_parser.add_argument(
        "--baselines",
        default="random,popularity",
        help="Comma-separated baselines to compare against",
    )
    eval_parser.add_argument(
        "--metrics",
        default="serendipity,diversity,coherence",
        help="Comma-separated metrics to compute",
    )
    eval_parser.add_argument("--output", default="results.json", help="Output file path")
    eval_parser.add_argument("--wandb", action="store_true", help="Log results to W&B")

    # show-results
    show_parser = subparsers.add_parser("show-results", help="Display benchmark results")
    show_parser.add_argument("--input", required=True, help="Path to results JSON file")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "download-data":
        _cmd_download(args)
    elif args.command == "evaluate":
        _cmd_evaluate(args)
    elif args.command == "show-results":
        _cmd_show_results(args)


def _cmd_download(args):
    """Download benchmark dataset."""
    print(f"Downloading {args.dataset}...")
    # TODO: Actual download implementation — Week 13
    print(f"Dataset would be saved to ~/.psyche-bench/data/{args.dataset}/")
    print("Download not yet implemented — use scripts/download_fma.sh for now.")


def _cmd_evaluate(args):
    """Run evaluation."""
    print(f"Evaluating model: {args.model}")
    print(f"Dataset: {args.dataset}")
    print(f"Baselines: {args.baselines}")
    print(f"Metrics: {args.metrics}")
    # TODO: Full evaluation implementation — Week 13
    results = {
        "model": args.model,
        "dataset": args.dataset,
        "metrics": {},
        "baselines": {},
        "status": "not_yet_implemented",
    }
    Path(args.output).write_text(json.dumps(results, indent=2))
    print(f"Results saved to {args.output}")


def _cmd_show_results(args):
    """Display results."""
    results = json.loads(Path(args.input).read_text())
    print("\n=== PSYCHE Benchmark Results ===")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

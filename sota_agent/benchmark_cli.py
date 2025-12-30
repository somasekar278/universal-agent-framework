"""Command-line interface for agent benchmarking."""

import argparse
import sys
from pathlib import Path


def main():
    """Main CLI entry point for benchmarking."""
    parser = argparse.ArgumentParser(
        description="SOTA Agent Benchmark Runner - Comprehensive agent evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sota-benchmark run --suite fraud --agents all --report md
  sota-benchmark run --suite all --agents myagent --parallel
  sota-benchmark run --suite customer_support --agents all --report md,json,html
  sota-benchmark create --suite fraud_detection --output benchmarks/

For more information, visit: https://github.com/somasekar278/universal-agent-template
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run benchmarks")
    run_parser.add_argument(
        "--suite",
        nargs="+",
        default=["all"],
        help="Benchmark suite(s) to run (default: all)"
    )
    run_parser.add_argument(
        "--agents",
        nargs="+",
        default=["all"],
        help="Agent(s) to evaluate (default: all)"
    )
    run_parser.add_argument(
        "--metrics",
        type=str,
        help="Comma-separated list of metrics (default: all standard metrics)"
    )
    run_parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel"
    )
    run_parser.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="Max parallel workers (default: 4)"
    )
    run_parser.add_argument(
        "--output-dir",
        default="benchmark_results",
        help="Output directory (default: benchmark_results)"
    )
    run_parser.add_argument(
        "--report",
        default="md",
        help="Report format(s): md,json,html (default: md)"
    )
    run_parser.add_argument(
        "--no-leaderboard",
        action="store_true",
        help="Skip leaderboard generation"
    )
    run_parser.add_argument(
        "--benchmark-dir",
        default="benchmarks",
        help="Directory containing benchmark suites (default: benchmarks)"
    )
    run_parser.add_argument(
        "--agents-dir",
        default="benchmark_agents",
        help="Directory containing agent modules (default: benchmark_agents)"
    )
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create benchmark suite template")
    create_parser.add_argument(
        "--suite",
        required=True,
        help="Suite name (e.g., fraud_detection)"
    )
    create_parser.add_argument(
        "--output",
        default="benchmarks",
        help="Output directory (default: benchmarks)"
    )
    create_parser.add_argument(
        "--num-tests",
        type=int,
        default=5,
        help="Number of test cases to generate (default: 5)"
    )
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available suites and agents")
    list_parser.add_argument(
        "--benchmark-dir",
        default="benchmarks",
        help="Benchmark directory (default: benchmarks)"
    )
    list_parser.add_argument(
        "--agents-dir",
        default="benchmark_agents",
        help="Agents directory (default: benchmark_agents)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="SOTA Agent Framework 0.2.0"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == "run":
            run_benchmarks(args)
        elif args.command == "create":
            create_suite(args)
        elif args.command == "list":
            list_items(args)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_benchmarks(args):
    """Run benchmark evaluation."""
    from evaluation.runner import BenchmarkRunner, BenchmarkConfig
    
    # Create config
    config = BenchmarkConfig.from_cli_args(args)
    
    # Create runner
    runner = BenchmarkRunner(
        config=config,
        benchmark_dir=Path(args.benchmark_dir),
        agents_dir=Path(args.agents_dir)
    )
    
    # Run benchmarks
    results = runner.run_sync()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📈 Benchmark Summary")
    print("=" * 60)
    
    for agent_name, agent_results in results.items():
        if not agent_results:
            continue
        
        passed = sum(1 for r in agent_results if r.passed)
        total = len(agent_results)
        avg_score = sum(r.overall_score for r in agent_results) / total
        
        print(f"\n{agent_name}:")
        print(f"  ✓ Pass Rate: {passed}/{total} ({passed/total*100:.1f}%)")
        print(f"  ✓ Avg Score: {avg_score:.3f}")


def create_suite(args):
    """Create a benchmark suite template."""
    from evaluation.harness import BenchmarkSuite, TestCase
    
    print(f"📝 Creating benchmark suite: {args.suite}")
    
    # Create suite
    suite = BenchmarkSuite(
        name=args.suite,
        description=f"Benchmark suite for {args.suite} domain",
        default_metrics=[
            "tool_call_success",
            "plan_correctness",
            "hallucination_rate",
            "latency",
            "coherence",
            "accuracy"
        ]
    )
    
    # Add template test cases
    for i in range(args.num_tests):
        test_case = TestCase(
            id=f"{args.suite}_test_{i+1}",
            name=f"Test Case {i+1}",
            input_data={
                "query": f"Sample query for test case {i+1}",
                "context": {}
            },
            expected_output={
                "ground_truth": {},
                "expected_tools": [],
                "expected_plan": {},
                "latency_budget_ms": 1000,
                "required_fields": [],
                "numeric_ranges": {},
                "structure": {}
            },
            tags=["generated", "template"]
        )
        suite.add_test_case(test_case)
    
    # Save to file
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{args.suite}.yaml"
    
    suite.to_yaml(output_path)
    
    print(f"✅ Created benchmark suite: {output_path}")
    print(f"   Test cases: {len(suite.test_cases)}")
    print(f"\n💡 Edit {output_path} to customize test cases and expectations")


def list_items(args):
    """List available suites and agents."""
    print("📦 Available Benchmark Suites:")
    
    benchmark_dir = Path(args.benchmark_dir)
    if benchmark_dir.exists():
        suites = list(benchmark_dir.glob("*.yaml"))
        if suites:
            for suite_file in suites:
                print(f"  - {suite_file.stem}")
        else:
            print("  (none found)")
    else:
        print(f"  Directory not found: {benchmark_dir}")
    
    print("\n🤖 Available Agents:")
    
    agents_dir = Path(args.agents_dir)
    if agents_dir.exists():
        agents = [f for f in agents_dir.glob("*.py") if not f.name.startswith("_")]
        if agents:
            for agent_file in agents:
                print(f"  - {agent_file.stem}")
        else:
            print("  (none found)")
    else:
        print(f"  Directory not found: {agents_dir}")


if __name__ == "__main__":
    main()


import argparse
import os
import sys
import tempfile

from .compiler import compile_cpp
from .reporter import run_stress_test

def check_file_exists(path: str, name: str) -> None:
    if not os.path.exists(path):
        print(f"Error: {name} file '{path}' does not exist.", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(description="CP Stress-Testing CLI Tool")
    parser.add_argument("command", choices=["run"], help="Command to run")
    parser.add_argument("--sol", required=True, help="Path to the solution .cpp file")
    parser.add_argument("--gen", required=True, help="Path to the test case generator .cpp file")
    parser.add_argument("--brute", help="Path to brute-force reference .cpp file")
    parser.add_argument("--checker", help="Path to a checker .cpp or .py for special-judge problems")
    parser.add_argument("--iters", type=int, default=100, help="Number of random test cases to run (default: 100)")
    parser.add_argument("--timeout", type=float, default=2.0, help="Seconds allowed for sol before declaring TLE (default: 2)")
    parser.add_argument("--seed-start", type=int, default=1, help="First seed value (default: 1)")
    
    args = parser.parse_args()
    
    if not args.brute and not args.checker:
        print("Error: You must provide either --brute or --checker.", file=sys.stderr)
        sys.exit(1)
        
    # Pre-flight checks
    check_file_exists(args.sol, "--sol")
    check_file_exists(args.gen, "--gen")
    if args.brute:
        check_file_exists(args.brute, "--brute")
    if args.checker:
        check_file_exists(args.checker, "--checker")
        
    print("Compiling files...")
    
    with tempfile.TemporaryDirectory() as tempdir:
        sol_bin = os.path.join(tempdir, "sol_bin")
        gen_bin = os.path.join(tempdir, "gen_bin")
        brute_bin = os.path.join(tempdir, "brute_bin") if args.brute else None
        
        compile_cpp(args.sol, sol_bin)
        compile_cpp(args.gen, gen_bin)
        
        if args.brute:
            compile_cpp(args.brute, brute_bin)
            
        checker_path = None
        if args.checker:
            if args.checker.endswith(".cpp"):
                checker_path = os.path.join(tempdir, "checker_bin")
                compile_cpp(args.checker, checker_path)
            else:
                checker_path = args.checker # E.g., a python script
                
        print("Compilation successful! Starting stress test...\n")
        
        run_stress_test(
            gen_bin=gen_bin,
            sol_bin=sol_bin,
            brute_bin=brute_bin,
            checker_path=checker_path,
            iters=args.iters,
            timeout=args.timeout,
            seed_start=args.seed_start
        )

if __name__ == "__main__":
    main()

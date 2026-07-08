import os
import sys
import tempfile
from typing import Optional
from .runner import run_generator, run_solution, TimeLimitExceeded, RuntimeException
from .compare import compare_exact, run_checker

def report_failure(seed: int, test_input: str, fail_type: str, sol_output: str, expected_output: str) -> None:
    """Prints diagnostic information upon a failure and saves the failing input."""
    print(f"\n[FAILED] on seed {seed} - {fail_type}")
    
    os.makedirs("fails", exist_ok=True)
    fail_path = f"fails/seed_{seed}.txt"
    with open(fail_path, "w", encoding="utf-8") as f:
        f.write(test_input)
        
    print(f"Test case saved to: {os.path.abspath(fail_path)}")
    print("\n--- Input ---")
    print(test_input.strip())
    print("\n--- Solution Output / Error ---")
    print(sol_output.strip())
    print("\n--- Brute Force / Checker Output ---")
    print(expected_output.strip())
    print()
    sys.exit(1)

def run_stress_test(gen_bin: str, sol_bin: str, brute_bin: Optional[str], checker_path: Optional[str], 
                    iters: int, timeout: float, seed_start: int) -> None:
    
    for i in range(iters):
        seed = seed_start + i
        
        # 1. Generate test case
        try:
            test_input = run_generator(gen_bin, seed)
        except Exception as e:
            print(f"\nGenerator failed on seed {seed}:\n{e}")
            sys.exit(1)
            
        # 2. Run Solution
        try:
            sol_output = run_solution(sol_bin, test_input, timeout)
        except TimeLimitExceeded:
            report_failure(seed, test_input, "Time Limit Exceeded", "<Took too long>", "<N/A>")
        except RuntimeException as e:
            report_failure(seed, test_input, "Runtime Error", e.stderr, "<N/A>")
            
        # 3. Check Correctness
        if brute_bin:
            try:
                # Brute force gets a generous 10 second timeout
                brute_output = run_solution(brute_bin, test_input, timeout=10.0)
            except TimeLimitExceeded:
                report_failure(seed, test_input, "Brute Force TLE (Internal Error)", "<N/A>", "Brute force took > 10 seconds.")
            except RuntimeException as e:
                report_failure(seed, test_input, "Brute Force RE (Internal Error)", "<N/A>", e.stderr)
                
            if not compare_exact(sol_output, brute_output):
                report_failure(seed, test_input, "Wrong Answer", sol_output, brute_output)
                
        elif checker_path:
            # We need to write input and sol_output to temp files for the checker
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as fin:
                fin.write(test_input)
                in_path = fin.name
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as fsol:
                fsol.write(sol_output)
                sol_path = fsol.name
                
            is_correct, checker_msg = run_checker(checker_path, in_path, sol_path)
            
            # Clean up temp files
            os.remove(in_path)
            os.remove(sol_path)
            
            if not is_correct:
                report_failure(seed, test_input, "Wrong Answer (Checker)", sol_output, checker_msg)

        # Print live progress updating the same line
        progress = f"[{i+1}/{iters}] seed={seed} ... PASS"
        sys.stdout.write(f"\r{progress}")
        sys.stdout.flush()
        
    print(f"\n\n[SUCCESS] All {iters} iterations passed!")

import subprocess
from typing import Tuple, Optional

def normalize_output(text: str) -> str:
    """
    Strips trailing whitespace per line and removes trailing blank lines.
    This ensures exact string match works even if there are carriage returns 
    or extra spaces at the end of lines.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    # Strip trailing whitespace from each line
    lines = [line.rstrip() for line in lines]
    
    # Remove trailing empty lines
    while lines and not lines[-1]:
        lines.pop()
        
    return "\n".join(lines)

def compare_exact(sol_output: str, brute_output: str) -> bool:
    """
    Compares two outputs using exact string match, ignoring trailing whitespace 
    per line and trailing blank lines.
    (Note: floating-point tolerance is not supported in v1).
    """
    return normalize_output(sol_output) == normalize_output(brute_output)

def run_checker(checker_path: str, input_file: str, sol_output_file: str, brute_output_file: Optional[str] = None) -> Tuple[bool, str]:
    """
    Runs a special-judge checker.
    The checker receives file paths as CLI args: <input_file> <sol_output_file> [<brute_output_file>].
    Returns (True, "") if checker exits with 0.
    Returns (False, checker_output) if checker exits with non-zero.
    """
    cmd = [checker_path, input_file, sol_output_file]
    if brute_output_file:
        cmd.append(brute_output_file)
        
    # We allow the checker to be a python script as well
    if checker_path.endswith(".py"):
        cmd.insert(0, "python")
        
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        is_correct = (result.returncode == 0)
        
        # Capture whatever the checker printed as the explanation (stdout or stderr)
        output_msg = result.stdout.strip()
        if result.stderr.strip():
            output_msg += "\n" + result.stderr.strip()
            
        return is_correct, output_msg.strip()
    except Exception as e:
        return False, f"Failed to execute checker: {e}"

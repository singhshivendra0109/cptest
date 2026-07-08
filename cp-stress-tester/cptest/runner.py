import subprocess

class TimeLimitExceeded(Exception):
    """Raised when a solution exceeds the given timeout."""
    pass

class RuntimeException(Exception):
    """Raised when a solution exits with a non-zero return code."""
    def __init__(self, stderr: str):
        self.stderr = stderr
        super().__init__(f"Runtime Error:\n{stderr}")

def run_generator(gen_binary_path: str, seed: int) -> str:
    """
    Runs the compiled generator binary with the given seed as argv[1].
    Captures and returns stdout as the test input string.
    """
    cmd = [gen_binary_path, str(seed)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout

def run_solution(binary_path: str, input_data: str, timeout: float) -> str:
    """
    Runs the compiled solution/brute binary, feeding input_data via stdin.
    
    Raises TimeLimitExceeded if it takes longer than `timeout` seconds.
    Raises RuntimeException if it crashes or exits with a non-zero code.
    Returns the captured stdout as a string.
    """
    cmd = [binary_path]
    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode != 0:
            raise RuntimeException(result.stderr)
        return result.stdout
    except subprocess.TimeoutExpired:
        raise TimeLimitExceeded()

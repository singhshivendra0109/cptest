import subprocess
import sys
import os

def compile_cpp(source_path: str, output_path: str) -> None:
    """
    Compiles a C++ source file using g++ -O2.
    If it fails, prints the exact g++ stderr output and exits immediately.
    """
    if not os.path.exists(source_path):
        print(f"Error: Source file '{source_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    cmd = ["g++", "-O2", "-o", output_path, source_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Compilation failed for {source_path}:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            sys.exit(1)
    except FileNotFoundError:
        print("Error: 'g++' not found. Please install a C++ compiler and ensure it is in your PATH.", file=sys.stderr)
        sys.exit(1)

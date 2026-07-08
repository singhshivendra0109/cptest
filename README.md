# CP Stress-Testing CLI Tool (`cptest`)

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A robust, system-level CLI tool designed for competitive programmers to automate the discovery of edge cases and failing tests in algorithmic solutions. 

By orchestrating isolated C++ compilation and inter-process communication (IPC) via standard I/O piping, `cptest` rapidly fires thousands of random test cases at a fast (but potentially buggy) solution, comparing its output against a slow, undeniably correct brute-force reference.

## ✨ Features

- **Automated Bug Discovery:** Instantly finds the exact small input that breaks your logic, saving hours of manual dry-running during live contests.
- **Process Isolation & Safety:** Uses Python's `subprocess` engine to enforce strict Time Limit Exceeded (TLE) constraints (default 2s) and intercept Runtime Errors (like segfaults) cleanly without crashing the tool.
- **Invisible File Handling:** Zero file I/O boilerplate required in your C++ code. The tool pipelines the generator's `stdout` directly into the `stdin` of your solutions in memory.
- **Smart Output Matching:** Automatically strips trailing whitespaces and trailing blank lines to prevent frustrating formatting-based false negatives.
- **Special-Judge Checker Protocol:** Write complex custom validation logic (e.g., graph traversal, floating-point validation) effortlessly in Python or C++.
- **Artifact Saving:** Upon finding a failure, the exact input array is instantly saved to a `fails/` directory for local debugging.

---

## 🚀 Installation

You can install `cptest` globally on your system using `pip`. Navigate to the project directory and run:

```bash
python -m pip install -e .
```

*Note: If your environment warns you that the installation script path is not on your Windows `PATH`, you can execute the tool anywhere using `python -m cptest.cli run` instead of just `cptest run`.*

---

## 📖 Usage Guide

To stress test a problem, you only need to write three standard C++ files. You can place these files anywhere on your computer.

### 1. File Setup
1. **`gen.cpp` (Generator):** Takes a random seed from `argv[1]` and prints a random test case to `cout`.
2. **`sol.cpp` (Your Solution):** Reads from `cin` and prints your fast, optimized answer to `cout`.
3. **`brute.cpp` (Reference):** Reads from `cin` and prints your slow, naive, 100% correct answer to `cout`.

### 2. Running the Tool
Open your terminal in the directory containing those three files and run:

```bash
python -m cptest.cli run --sol sol.cpp --brute brute.cpp --gen gen.cpp
```

---

## 🔄 Working Flow & Architecture

The tool abstracts away the pain of file management, compilation, and string comparison. Below is the complete lifecycle of a single stress-test command:

```mermaid
flowchart TD
    A([Start: cptest run]) --> B[Create Temporary Sandbox]
    B --> C[Compile sol.cpp, gen.cpp, brute.cpp]
    
    C --> D{Compilation Success?}
    D -- No --> E([Halt & Show Compile Error])
    D -- Yes --> F[Initialize test loop: seed = 1 to N]
    
    F --> G[Run gen_bin.exe with seed]
    G --> H[Capture test_input from stdout]
    
    H --> I(Run sol_bin.exe)
    H --> J(Run brute_bin.exe)
    
    I -. pipes test_input to stdin .-> K[Capture sol_output]
    J -. pipes test_input to stdin .-> L[Capture expected_output]
    
    K --> M{Execution Valid?}
    L --> M
    
    M -- TLE or Runtime Error --> N[Report Crash]
    M -- Success --> O{Compare Outputs}
    
    O -- Mismatch --> P[Write test_input to fails/seed_X.txt]
    P --> Q([Halt & Display Outputs])
    
    N --> P
    
    O -- Match --> R{More seeds?}
    R -- Yes --> F
    R -- No --> S([SUCCESS: All tests passed!])
```

### 🏗️ Under the Hood
1. **Compilation Sandbox:** Uses Python's `tempfile.TemporaryDirectory()` to compile `.exe` binaries. This ensures your workspace remains unpolluted by `.exe` files and `.obj` build artifacts.
2. **Execution Engine (`runner.py`):** Utilizes `subprocess.run(capture_output=True, timeout=X)` to launch the compiled C++ binaries. Standard streams (`stdin`/`stdout`) are safely and securely piped in RAM.
3. **Argparse CLI (`cli.py`):** Exposes customizable flags allowing you to dynamically adjust iterations (`--iters`), timeout limits (`--timeout`), and deterministic starting seeds (`--seed-start`).

---

## 🛠️ Advanced: Special-Judge Checkers

If a problem has multiple valid configurations (e.g., "output any valid path in a graph"), an exact string match against a brute force will fail. Instead of `--brute`, you can provide a custom `--checker` (written in `.cpp` or `.py`):

```bash
python -m cptest.cli run --sol sol.cpp --gen gen.cpp --checker checker.py
```

**Checker Protocol:** 
The tool passes temporary file paths to your checker via command line arguments in this exact order: 
`checker <input_file> <sol_output_file> [<brute_output_file>]`

Your checker script should parse these files. If the solution is correct, exit with code `0`. Any non-zero exit code triggers a failure, and `cptest` will forward whatever your checker printed to `stdout`/`stderr` directly to the user as the explanation.

---

## 💡 Why this exists (Related Tools)

While tools like `quicktest`, `CP Editor` built-ins, and bash scripts exist, `cptest` was designed with a specific angle: **a seamless Python-based checker plugin system**. Writing complex validation logic (like graph cycles or float tolerances) in C++ during a live contest is slow and error-prone. By allowing checkers to be written natively in Python, validation scripts can be built in a fraction of the time. It also features automatic `fails/` directory organization natively.

---

## ⚠️ Known Limitations (v1.0)
- **No Floating-Point Tolerance:** Exact output matching currently does not support dynamic floating-point tolerance (e.g., `1.000` != `1.0`). Use a custom Python checker for float problems.
- **Language Support:** v1 currently only officially supports C++ for the `sol`, `gen`, and `brute` files.
- **Single-Threaded:** The test loop is currently sequential, running one seed at a time.


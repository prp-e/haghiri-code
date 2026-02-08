Here is a comprehensive game plan to build a *Claude Code* style agentic assistant, adhering strictly to your functional programming rules and resource constraints.

# Project Blueprint: The "No-Class" Coding Agent

This document outlines the architecture for a serious, functional-style coding agent. The core philosophy here is **State-as-Data**: passing dictionaries of context between functions rather than encapsulating state in objects.

## Needs

### 1. Essential Libraries
Since we are avoiding OOP, we need libraries that support strong functional patterns and easy API switching.

*   **`litellm`**: The most critical library for your resource setup. It standardizes calls to OpenAI, Anthropic, OpenRouter, Ollama, and Nebius into a single format. It handles the "API shim" so you don't have to write logic for every provider.
*   **`tenacity`**: For retrying failed API calls or tool executions without writing complex `try/except` loops.
*   **`rich`**: To build a beautiful, terminal-based user interface (TUI). It handles Markdown rendering and spinners without needing class-based UI frameworks.
*   **`pydantic`** (specifically `TypeAdapter` or functional validators): Even without classes, you need to define the *schema* of your tools so the LLM knows how to call them.
*   **`fnmatch`** & **`glob`**: For file pattern matching (ignoring `.git`, `__pycache__`).
*   **`subprocess`**: To handle the actual execution of shell commands.

### 2. Required Methods (The Tool Calling Loop)
To achieve a "Tool Calling Approach" without objects, you need a recursive or `while` loop architecture composed of these pure functions:

*   **`orchestrate_agent_loop`**: The main entry point. It holds the conversation history list and calls the LLM.
*   **`extract_tool_calls`**: Parses the raw response from the LLM (OpenAI format or raw text) to identify if the model wants to run a function.
*   **`route_tool_execution`**: A mapping function (using a dictionary dispatch pattern) that takes a tool name string and arguments, then calls the actual Python function.
*   **`capture_command_output`**: Runs system commands and captures `stdout` and `stderr` safely to feed back to the model.
*   **`serialize_context`**: Reads the current file buffer or directory tree and converts it into a token-optimized string to be inserted into the System Prompt.

### 3. Path to "Serious" Engineering
To move from a hobby script to a production-grade engine:

*   **Implement Safe Sandboxing**: Currently, your agent likely runs on your laptop's OS. To be serious, you must implement an **Execution Environment**. Use your RunPod credits to spin up a Docker container that acts as the "Agent's Computer." The agent sends commands to the container, not your local shell. This prevents accidental deletion of your own files.
*   **Context Pruning (AST Parsing)**: Instead of reading whole files, use `tree-sitter` bindings. This allows the agent to read *just* the function signatures of a large file before deciding to read the implementation.
*   **Evaluation Pipeline**: You cannot improve what you don't measure. Run your agent against the **SWE-bench** (Software Engineering Benchmark) lite dataset to score its ability to solve GitHub issues.

---

## Tool Definitions

These are the pure functions exposed to the LLM. They are named comprehensively in snake_case as requested.

### File System Operations
*   **`read_file_content_from_path`**: Opens a file and returns its text. Must handle encoding errors gracefully.
*   **`write_content_to_file_path`**: Overwrites a file with new content. Crucial for creating new files.
*   **`apply_text_patch_to_file`**: Instead of rewriting the whole file (which is slow and token-heavy), this tool accepts a search block and a replace block to modify existing code.
*   **`list_recursive_directory_structure`**: Returns a tree view of the file system, respecting `.gitignore` rules.
*   **`search_codebase_using_regex`**: Runs a grep-like search to find where specific functions or variables are defined across the project.

### Execution & Analysis
*   **`execute_shell_command_in_terminal`**: Runs bash commands (e.g., `pip install`, `pytest`, `python main.py`).
*   **`fetch_documentation_from_url`**: Uses a headless browser or simple requests to scrape external library documentation when the agent gets stuck (uses your internet search capability).
*   **`analyze_python_syntax_validity`**: A fast check (using Python's `ast` module) to verify code written by the agent is syntactically correct before running it.

---

## Resource Game Plan

Based on your hardware and credits, here is the optimal architecture:

### 1. The "Brain" (Cloud APIs)
*   **Primary Logic (High Intelligence)**: Use **OpenRouter** to access **Claude 3.5 Sonnet** or **DeepSeek V3**. These are the best coding models currently. Use these for the *planning* phase and *writing* code.
*   **Fallback/Speed (Nebius/Novita)**: Use **Llama 3 70B** or **Qwen 2.5 Coder** via Nebius for faster, cheaper tasks like "explain this error" or "write a docstring".

### 2. The "Eyes" (Local GPU - RTX 3050)
*   Your 3050 has limited VRAM (4GB-6GB), so it cannot run the main logic.
*   **Embedding Engine**: Run a small embedding model locally (like `nomic-embed-text-v1.5`) using **Ollama**. This allows you to index your entire codebase locally for free. When the agent asks "Where is the `login` function?", you perform a local vector search rather than paying API fees to read every file.
*   **Summarizer**: Run a highly quantized 7B model (like `Mistral-Nemo` or `DeepSeek-R1-Distill-Qwen-7B`) locally. Use this to summarize long documentation pages before sending the summary to the smart cloud model.

### 3. The "Hands" (RunPod & Cloud)
*   **The Sandbox**: Use your **RunPod** credits to keep a "Development Pod" running. When your agent decides to `execute_shell_command_in_terminal`, do **not** run it on your laptop. Send the command via SSH or HTTP to the RunPod instance.
*   **Heavy Lifting**: If you need to compile a massive project or run heavy integration tests, offload this to the RunPod GPU pod.

### 4. Grants & Funding Strategy
*   **Modal**: Build your "Sandboxing" infrastructure on Modal. They love projects that use their platform for isolation. If you write a blog post about "Building a Safe Agent with Modal Sandboxes," you are highly likely to get credits.
*   **Nebius**: They are currently aggressive with grants for open-source AI agents. Position your project as an "Open Source, Functional-Style Coding Agent" to apply for their startup program.
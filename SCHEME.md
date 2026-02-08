Here is a schematic representation of the codebase. This design strictly follows the **Functional Programming** paradigm (no classes) and uses **Type Hinting** to maintain structure without object-oriented overhead.

### 1. The State Definition
Instead of an object holding variables, we define a dictionary structure that acts as the "Single Source of Truth" passed between functions.

```python
from typing import TypedDict, List, Dict, Any, Union

# The entire memory of the agent is contained here
class AgentState(TypedDict):
    messages: List[Dict[str, str]]       # Chat history (User, Assistant, Tool roles)
    working_directory: str               # Current folder context
    scratchpad: str                      # Place for the agent to store thoughts
    tool_outputs: Dict[str, Any]         # Cache for recent tool results
    iteration_count: int                 # Safety breaker to prevent infinite loops
```

### 2. The Tool Registry
A strictly typed dictionary mapping string names to pure functions. This allows dynamic dispatch without `if/else` chains.

```python
# Tool function signatures (Implementations omitted for brevity)
def read_file_content_from_path(file_path: str) -> str:
    """Reads a file and returns text."""
    ...

def execute_shell_command_in_terminal(command: str) -> str:
    """Runs a bash command and returns stdout/stderr."""
    ...

def search_codebase_using_regex(pattern: str) -> str:
    """Greps the codebase."""
    ...

# The Registry: Maps snake_case names to actual python callables
TOOL_REGISTRY = {
    "read_file": read_file_content_from_path,
    "run_shell": execute_shell_command_in_terminal,
    "search_code": search_codebase_using_regex,
}

# The Schema: JSON definitions sent to the LLM (e.g., OpenAI format)
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads file content...",
            "parameters": { ... } 
        }
    },
    # ... schemas for other tools
]
```

### 3. The Core Logic (The Brain)
Functions that handle the API communication and parsing.

```python
import litellm

def call_language_model(state: AgentState) -> Dict[str, Any]:
    """
    Pure function: Takes current state, returns raw model response.
    Uses 'litellm' to handle switching between OpenRouter/Ollama/Nebius.
    """
    response = litellm.completion(
        model="openrouter/anthropic/claude-3.5-sonnet",
        messages=state['messages'],
        tools=TOOL_SCHEMAS,
        tool_choice="auto"
    )
    return response.choices[0].message

def parse_model_response(raw_message: Any) -> Union[str, Dict]:
    """
    Determines if the model wants to talk (str) or act (Dict).
    """
    if raw_message.tool_calls:
        return {
            "action": "tool_call",
            "tool_name": raw_message.tool_calls[0].function.name,
            "tool_args": raw_message.tool_calls[0].function.arguments
        }
    else:
        return {
            "action": "reply",
            "content": raw_message.content
        }
```

### 4. The Execution Engine (The Main Loop)
This is where the magic happens. A `while` loop that orchestrates the flow.

```python
def run_agent_cycle(user_objective: str, initial_path: str):
    # 1. Initialize State
    current_state: AgentState = {
        "messages": [{"role": "user", "content": user_objective}],
        "working_directory": initial_path,
        "scratchpad": "",
        "tool_outputs": {},
        "iteration_count": 0
    }

    print(f"--- Starting Agent in {initial_path} ---")

    # 2. Main Loop
    while current_state['iteration_count'] < 50: # Hard limit for safety
        
        # A. Think
        raw_response = call_language_model(current_state)
        decision = parse_model_response(raw_response)
        
        # B. Route
        if decision['action'] == 'reply':
            print(f"Agent: {decision['content']}")
            # Update state history
            current_state['messages'].append(raw_response)
            # Break if task is done, or ask user for new input
            break 
            
        elif decision['action'] == 'tool_call':
            tool_name = decision['tool_name']
            tool_args = decision['tool_args']
            
            print(f"Action: Calling {tool_name} with {tool_args}...")
            
            # C. Act (Dynamic Dispatch)
            if tool_name in TOOL_REGISTRY:
                # Execute the specific function
                output = TOOL_REGISTRY[tool_name](**tool_args)
                
                # Update State with tool result
                tool_message = {
                    "role": "tool",
                    "name": tool_name,
                    "content": output
                }
                current_state['messages'].append(raw_response) # Add the call
                current_state['messages'].append(tool_message) # Add the result
            
        current_state['iteration_count'] += 1
```
# formal-methods-agent
An agent equipped with Formal Methods skills

## Overview

This project implements a single agent with multiple skills for formal methods tasks. The agent can process user requests and invoke the appropriate skills to perform operations.

## Architecture

The system consists of:
- **Agent**: Central coordinator that manages skills and processes user requests
- **Skills**: Pluggable modules that perform specific operations

### Available Skills

1. **DotnetSkill**: Performs .NET operations
   - `build`: Build .NET projects and solutions

2. **CoyoteSkill**: Performs operations with the [Coyote](https://github.com/microsoft/coyote) tool
   - `test`: Run systematic testing on .NET assemblies
   - `rewrite`: Rewrite assemblies for Coyote testing

## Installation

### Prerequisites

- Python 3.8 or higher
- .NET SDK (for DotnetSkill)
- Coyote tool (for CoyoteSkill) - Install from https://github.com/microsoft/coyote

### Setup

1. Clone the repository:
```bash
git clone https://github.com/suvamM/formal-methods-agent.git
cd formal-methods-agent
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Basic Example

```python
from formal_methods_agent.agent import Agent
from formal_methods_agent.skills import DotnetSkill, CoyoteSkill

# Create and configure the agent
agent = Agent()
agent.register_skill(DotnetSkill())
agent.register_skill(CoyoteSkill())

# Build a .NET project
result = agent.process_request(
    skill_name="dotnet",
    operation="build",
    project_path="./MyProject"
)

if result['success']:
    print("Build succeeded!")
else:
    print(f"Build failed: {result['error']}")

# Run Coyote testing
result = agent.process_request(
    skill_name="coyote",
    operation="test",
    assembly_path="./bin/Debug/net8.0/MyApp.dll",
    args="--iterations 100"
)

if result['success']:
    print("Testing completed!")
else:
    print(f"Testing failed: {result['error']}")
```

### Running the Example

```bash
python examples/basic_usage.py
```

## Extending the Agent

To add a new skill:

1. Create a new class that inherits from `Skill`
2. Implement the `execute` method
3. Register the skill with the agent

Example:

```python
from formal_methods_agent.skills.base_skill import Skill

class MyCustomSkill(Skill):
    def __init__(self):
        super().__init__("custom")
    
    def execute(self, operation: str, **kwargs):
        # Implement your skill logic here
        return {"success": True, "output": "Operation completed"}

# Register with agent
agent.register_skill(MyCustomSkill())
```

## License

MIT License - See LICENSE file for details

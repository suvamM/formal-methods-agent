"""Example usage of the Formal Methods Agent."""

from formal_methods_agent.agent import Agent
from formal_methods_agent.skills import DotnetSkill, CoyoteSkill


def main():
    """Demonstrate the agent usage."""
    # Create the agent
    agent = Agent()
    
    # Register skills
    agent.register_skill(DotnetSkill())
    agent.register_skill(CoyoteSkill())
    
    print("Formal Methods Agent initialized")
    print(f"Agent: {agent}")
    print(f"Available skills: {', '.join(agent.list_skills())}\n")
    
    # Example 1: Build a .NET project
    print("=" * 60)
    print("Example 1: Building a .NET project")
    print("=" * 60)
    result = agent.process_request(
        skill_name="dotnet",
        operation="build",
        project_path=".",
        args=""
    )
    print(f"Success: {result.get('success')}")
    if result.get('success'):
        print(f"Output: {result.get('output', '')[:200]}...")
    else:
        print(f"Error: {result.get('error')}")
    print()
    
    # Example 2: Run Coyote test (this will fail if no assembly is present)
    print("=" * 60)
    print("Example 2: Running Coyote test")
    print("=" * 60)
    # Note: Replace the path below with an actual .NET assembly path
    # For example: "./bin/Debug/net8.0/MyApp.dll"
    result = agent.process_request(
        skill_name="coyote",
        operation="test",
        assembly_path="./bin/Debug/net8.0/MyApp.dll",
        args="--iterations 100"
    )
    print(f"Success: {result.get('success')}")
    if result.get('success'):
        print(f"Output: {result.get('output', '')[:200]}...")
    else:
        print(f"Error: {result.get('error')}")
    print()
    
    # Example 3: Invalid skill
    print("=" * 60)
    print("Example 3: Invalid skill request")
    print("=" * 60)
    result = agent.process_request(
        skill_name="invalid_skill",
        operation="do_something"
    )
    print(f"Success: {result.get('success')}")
    print(f"Error: {result.get('error')}")
    print()


if __name__ == "__main__":
    main()

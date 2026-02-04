"""Dotnet skill for the Formal Methods Agent."""

import subprocess
from typing import Any, Dict
from .base_skill import Skill


class DotnetSkill(Skill):
    """Skill for performing .NET operations."""

    def __init__(self):
        """Initialize the Dotnet skill."""
        super().__init__("dotnet")

    def execute(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Execute a dotnet operation.
        
        Args:
            operation: The dotnet operation to execute (e.g., 'build', 'test', 'run').
            **kwargs: Additional arguments for the operation.
                - project_path: Path to the project/solution file (optional).
                - args: Additional command-line arguments (optional).
            
        Returns:
            A dictionary containing:
                - success (bool): Whether the operation succeeded.
                - output (str): The command output.
                - error (str): Error message if any.
        """
        if operation == "build":
            return self._build(**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown operation: {operation}. Supported operations: build"
            }

    def _build(self, project_path: str = ".", args: str = "") -> Dict[str, Any]:
        """Build a .NET project.
        
        Args:
            project_path: Path to the project or solution file.
            args: Additional build arguments.
            
        Returns:
            A dictionary with the build result.
        """
        try:
            cmd = ["dotnet", "build", project_path]
            if args:
                cmd.extend(args.split())
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": (result.stderr or result.stdout).strip() if result.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Build operation timed out after 5 minutes"
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "dotnet command not found. Please ensure .NET SDK is installed."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"An error occurred: {str(e)}"
            }

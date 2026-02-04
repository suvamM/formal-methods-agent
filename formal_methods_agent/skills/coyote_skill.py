"""Coyote skill for the Formal Methods Agent."""

import subprocess
from typing import Any, Dict
from .base_skill import Skill


class CoyoteSkill(Skill):
    """Skill for performing Coyote operations.
    
    Coyote is a tool for systematic testing of concurrent C# code.
    See: https://github.com/microsoft/coyote
    """

    def __init__(self):
        """Initialize the Coyote skill."""
        super().__init__("coyote")

    def execute(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Execute a Coyote operation.
        
        Args:
            operation: The Coyote operation to execute (e.g., 'test', 'rewrite').
            **kwargs: Additional arguments for the operation.
                - assembly_path: Path to the assembly to test (required for most operations).
                - args: Additional command-line arguments (optional).
            
        Returns:
            A dictionary containing:
                - success (bool): Whether the operation succeeded.
                - output (str): The command output.
                - error (str): Error message if any.
        """
        if operation == "test":
            return self._test(**kwargs)
        elif operation == "rewrite":
            return self._rewrite(**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown operation: {operation}. Supported operations: test, rewrite"
            }

    def _test(self, assembly_path: str, args: str = "") -> Dict[str, Any]:
        """Run Coyote testing on an assembly.
        
        Args:
            assembly_path: Path to the .NET assembly to test.
            args: Additional test arguments (e.g., '--iterations 100').
            
        Returns:
            A dictionary with the test result.
        """
        if not assembly_path:
            return {
                "success": False,
                "error": "assembly_path is required for Coyote test operation"
            }
        
        try:
            cmd = ["coyote", "test", assembly_path]
            if args:
                cmd.extend(args.split())
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for testing
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": (result.stderr or result.stdout).strip() if result.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Coyote test operation timed out after 10 minutes"
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "coyote command not found. Please ensure Coyote is installed."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"An error occurred: {str(e)}"
            }

    def _rewrite(self, assembly_path: str, args: str = "") -> Dict[str, Any]:
        """Rewrite an assembly for Coyote testing.
        
        Args:
            assembly_path: Path to the .NET assembly to rewrite.
            args: Additional rewrite arguments.
            
        Returns:
            A dictionary with the rewrite result.
        """
        if not assembly_path:
            return {
                "success": False,
                "error": "assembly_path is required for Coyote rewrite operation"
            }
        
        try:
            cmd = ["coyote", "rewrite", assembly_path]
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
                "error": "Coyote rewrite operation timed out after 5 minutes"
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "coyote command not found. Please ensure Coyote is installed."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"An error occurred: {str(e)}"
            }

"""Base skill class for the Formal Methods Agent."""

from abc import ABC, abstractmethod
from typing import Any, Dict
import subprocess


class Skill(ABC):
    """Abstract base class for all skills."""

    def __init__(self, name: str):
        """Initialize the skill.
        
        Args:
            name: The name of the skill.
        """
        self.name = name

    @abstractmethod
    def execute(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Execute a skill operation.
        
        Args:
            operation: The operation to execute.
            **kwargs: Additional arguments for the operation.
            
        Returns:
            A dictionary containing the result of the operation.
            Should include 'success' (bool) and 'message' or 'output' keys.
        """
        pass

    def _extract_error_message(self, result: subprocess.CompletedProcess) -> str:
        """Extract error message from subprocess result.
        
        Args:
            result: The completed process result.
            
        Returns:
            Error message from stderr or stdout, stripped of whitespace.
        """
        return (result.stderr or result.stdout).strip()

    def __str__(self) -> str:
        """String representation of the skill."""
        return f"{self.__class__.__name__}(name='{self.name}')"

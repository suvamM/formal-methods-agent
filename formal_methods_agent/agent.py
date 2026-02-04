"""Agent for the Formal Methods Agent."""

from typing import Any, Dict, List, Optional
from .skills.base_skill import Skill


class Agent:
    """Agent that processes user requests and invokes skills."""

    def __init__(self):
        """Initialize the agent."""
        self.skills: Dict[str, Skill] = {}

    def register_skill(self, skill: Skill) -> None:
        """Register a skill with the agent.
        
        Args:
            skill: The skill to register.
        """
        self.skills[skill.name] = skill

    def list_skills(self) -> List[str]:
        """List all registered skills.
        
        Returns:
            A list of skill names.
        """
        return list(self.skills.keys())

    def process_request(self, skill_name: str, operation: str, **kwargs) -> Dict[str, Any]:
        """Process a user request by invoking the appropriate skill.
        
        Args:
            skill_name: The name of the skill to invoke.
            operation: The operation to perform.
            **kwargs: Additional arguments for the operation.
            
        Returns:
            A dictionary containing the result of the operation.
        """
        if skill_name not in self.skills:
            return {
                "success": False,
                "error": f"Skill '{skill_name}' not found. Available skills: {', '.join(self.list_skills())}"
            }
        
        skill = self.skills[skill_name]
        
        try:
            result = skill.execute(operation, **kwargs)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Error executing {skill_name}.{operation}: {str(e)}"
            }

    def __str__(self) -> str:
        """String representation of the agent."""
        skills_str = ", ".join(self.list_skills())
        return f"Agent(skills=[{skills_str}])"

"""Tests for the Formal Methods Agent."""

import unittest
from formal_methods_agent.agent import Agent
from formal_methods_agent.skills import DotnetSkill, CoyoteSkill, Skill


class TestAgent(unittest.TestCase):
    """Test cases for the Agent class."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = Agent()

    def test_agent_initialization(self):
        """Test that agent initializes correctly."""
        self.assertIsInstance(self.agent, Agent)
        self.assertEqual(len(self.agent.list_skills()), 0)

    def test_register_skill(self):
        """Test skill registration."""
        skill = DotnetSkill()
        self.agent.register_skill(skill)
        self.assertEqual(len(self.agent.list_skills()), 1)
        self.assertIn("dotnet", self.agent.list_skills())

    def test_register_multiple_skills(self):
        """Test registering multiple skills."""
        self.agent.register_skill(DotnetSkill())
        self.agent.register_skill(CoyoteSkill())
        self.assertEqual(len(self.agent.list_skills()), 2)
        self.assertIn("dotnet", self.agent.list_skills())
        self.assertIn("coyote", self.agent.list_skills())

    def test_invalid_skill_request(self):
        """Test that requesting an invalid skill returns an error."""
        result = self.agent.process_request("invalid", "test")
        self.assertFalse(result["success"])
        self.assertIn("error", result)
        self.assertIn("not found", result["error"])

    def test_process_request_with_registered_skill(self):
        """Test processing a request with a registered skill."""
        self.agent.register_skill(DotnetSkill())
        # This will fail because dotnet is not installed, but should return proper error
        result = self.agent.process_request("dotnet", "build", project_path=".")
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)

    def test_agent_string_representation(self):
        """Test string representation of agent."""
        self.agent.register_skill(DotnetSkill())
        self.agent.register_skill(CoyoteSkill())
        agent_str = str(self.agent)
        self.assertIn("Agent", agent_str)
        self.assertIn("dotnet", agent_str)
        self.assertIn("coyote", agent_str)


class TestDotnetSkill(unittest.TestCase):
    """Test cases for the DotnetSkill class."""

    def setUp(self):
        """Set up test fixtures."""
        self.skill = DotnetSkill()

    def test_skill_initialization(self):
        """Test that skill initializes correctly."""
        self.assertEqual(self.skill.name, "dotnet")

    def test_unknown_operation(self):
        """Test that unknown operations return an error."""
        result = self.skill.execute("unknown_op")
        self.assertFalse(result["success"])
        self.assertIn("error", result)
        self.assertIn("Unknown operation", result["error"])

    def test_skill_string_representation(self):
        """Test string representation of skill."""
        skill_str = str(self.skill)
        self.assertIn("DotnetSkill", skill_str)
        self.assertIn("dotnet", skill_str)


class TestCoyoteSkill(unittest.TestCase):
    """Test cases for the CoyoteSkill class."""

    def setUp(self):
        """Set up test fixtures."""
        self.skill = CoyoteSkill()

    def test_skill_initialization(self):
        """Test that skill initializes correctly."""
        self.assertEqual(self.skill.name, "coyote")

    def test_unknown_operation(self):
        """Test that unknown operations return an error."""
        result = self.skill.execute("unknown_op")
        self.assertFalse(result["success"])
        self.assertIn("error", result)
        self.assertIn("Unknown operation", result["error"])

    def test_test_operation_without_assembly(self):
        """Test that test operation requires assembly_path."""
        result = self.skill.execute("test", assembly_path="")
        self.assertFalse(result["success"])
        self.assertIn("error", result)
        self.assertIn("required", result["error"])

    def test_rewrite_operation_without_assembly(self):
        """Test that rewrite operation requires assembly_path."""
        result = self.skill.execute("rewrite", assembly_path="")
        self.assertFalse(result["success"])
        self.assertIn("error", result)
        self.assertIn("required", result["error"])

    def test_skill_string_representation(self):
        """Test string representation of skill."""
        skill_str = str(self.skill)
        self.assertIn("CoyoteSkill", skill_str)
        self.assertIn("coyote", skill_str)


if __name__ == "__main__":
    unittest.main()

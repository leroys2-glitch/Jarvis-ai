"""
Test suite for Jarvis AI Core functionality
"""

import unittest
from jarvis.core.assistant import JarvisAI
from jarvis.core.agent_manager import AgentRole, AgentStatus


class TestJarvisCore(unittest.TestCase):
    """Test Jarvis core functionality"""

    def setUp(self):
        """Initialize Jarvis for testing"""
        self.jarvis = JarvisAI(name="TestJarvis")

    def test_jarvis_initialization(self):
        """Test Jarvis initializes correctly"""
        self.assertEqual(self.jarvis.name, "TestJarvis")
        self.assertIsNotNone(self.jarvis.agent_manager)

    def test_basic_conversation(self):
        """Test basic conversation"""
        response = self.jarvis.process("Hello")
        self.assertIsNotNone(response)
        self.assertIn("Hello", response)

    def test_create_agent(self):
        """Test agent creation"""
        agent_id = self.jarvis.create_agent("TestAgent", "scheduler")
        self.assertIsNotNone(agent_id)
        agent = self.jarvis.agent_manager.get_agent(agent_id)
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "TestAgent")

    def test_agent_by_role(self):
        """Test getting agents by role"""
        self.jarvis.create_agent("Scheduler1", "scheduler")
        self.jarvis.create_agent("Scheduler2", "scheduler")
        schedulers = self.jarvis.get_agents_by_role("scheduler")
        self.assertEqual(len(schedulers), 2)

    def test_system_status(self):
        """Test system status"""
        self.jarvis.create_agent("Agent1", "general")
        status = self.jarvis.get_system_status()
        self.assertEqual(status['total_agents'], 1)
        self.assertGreaterEqual(status['active_agents'], 0)


class TestAgentManager(unittest.TestCase):
    """Test Agent Manager functionality"""

    def setUp(self):
        """Initialize Agent Manager for testing"""
        from jarvis.core.agent_manager import AgentManager
        self.manager = AgentManager()

    def test_create_agent(self):
        """Test agent creation"""
        agent = self.manager.create_agent("TestAgent", "scheduler")
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "TestAgent")

    def test_find_best_agent(self):
        """Test finding best agent for capability"""
        self.manager.create_agent("Scheduler", "scheduler")
        agent = self.manager.find_best_agent("schedule_meeting")
        self.assertIsNotNone(agent)

    def test_delegate_task(self):
        """Test task delegation"""
        self.manager.create_agent("Worker", "general")
        task = {
            "id": "test_task",
            "description": "Test task",
            "priority": "normal"
        }
        success = self.manager.delegate_task("any_capability", task)
        self.assertTrue(success)

    def test_agent_communication(self):
        """Test inter-agent communication"""
        agent1 = self.manager.create_agent("Agent1", "scheduler")
        agent2 = self.manager.create_agent("Agent2", "email_handler")
        
        success = self.manager.send_message(
            agent1.id,
            agent2.id,
            "Test message"
        )
        self.assertTrue(success)

    def test_broadcast_message(self):
        """Test message broadcasting"""
        agent1 = self.manager.create_agent("Agent1", "scheduler")
        self.manager.create_agent("Agent2", "scheduler")
        self.manager.create_agent("Agent3", "email_handler")
        
        count = self.manager.broadcast_message(
            agent1.id,
            "Test broadcast",
            target_role="scheduler"
        )
        self.assertEqual(count, 2)  # Should broadcast to 2 schedulers


if __name__ == '__main__':
    unittest.main()

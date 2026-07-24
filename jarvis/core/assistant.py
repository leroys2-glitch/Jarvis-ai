"""
Main Jarvis AI Assistant Class with Multi-Agent Support
"""

import yaml
import logging
import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime
from jarvis.core.agent_manager import AgentManager, AgentRole

logger = logging.getLogger(__name__)


class JarvisAI:
    """Main Jarvis Assistant Class with Agent Management"""

    def __init__(self, name: str = "Jarvis", config_path: str = "config.yaml"):
        """
        Initialize Jarvis AI Assistant

        Args:
            name: Name of the assistant
            config_path: Path to configuration file
        """
        self.name = name
        self.config = self._load_config(config_path)
        self.conversation_history = []
        self.tasks = []
        self.voice_enabled = False
        
        # Initialize Agent Manager
        self.agent_manager = AgentManager()
        self.controlled_agents: List[str] = []

        logger.info(f"Initializing {self.name} AI Assistant with Multi-Agent Support")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}")
            return {}

    # ===== Agent Management Methods =====
    
    def create_agent(self, name: str, role: str, custom_capabilities: Optional[List[str]] = None) -> str:
        """
        Create a new controlled AI agent

        Args:
            name: Name for the agent
            role: Role from AgentRole (scheduler, email_handler, data_analyst, code_assistant, researcher, monitor, general)
            custom_capabilities: Optional custom capabilities

        Returns:
            Agent ID
        """
        agent = self.agent_manager.create_agent(name, role, custom_capabilities)
        self.controlled_agents.append(agent.id)
        logger.info(f"{self.name} created agent: {name}")
        return agent.id

    def delegate_task(self, capability: str, task_description: str, priority: str = "normal") -> bool:
        """
        Delegate a task to an agent with the required capability

        Args:
            capability: Required capability
            task_description: Description of the task
            priority: Task priority (low, normal, high)

        Returns:
            True if task was delegated successfully
        """
        task = {
            "id": str(uuid.uuid4()),
            "description": task_description,
            "priority": priority,
            "created_at": datetime.now().isoformat()
        }
        
        success = self.agent_manager.delegate_task(capability, task)
        
        if success:
            self.conversation_history.append({
                "role": "system",
                "message": f"Task delegated: {task_description}",
                "timestamp": datetime.now().isoformat()
            })
        
        return success

    def send_agent_message(self, from_agent_id: str, to_agent_id: str, message: str) -> bool:
        """
        Send a message between agents

        Args:
            from_agent_id: Sender agent ID
            to_agent_id: Receiver agent ID
            message: Message content

        Returns:
            True if message was sent successfully
        """
        return self.agent_manager.send_message(from_agent_id, to_agent_id, message)

    def broadcast_to_agents(self, agent_id: str, message: str, target_role: Optional[str] = None) -> int:
        """
        Broadcast a message to multiple agents

        Args:
            agent_id: Sending agent ID
            message: Message content
            target_role: Optional role to target

        Returns:
            Number of agents that received the message
        """
        return self.agent_manager.broadcast_message(agent_id, message, target_role)

    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific agent"""
        agent = self.agent_manager.get_agent(agent_id)
        return agent.get_info() if agent else None

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status including all agents"""
        return self.agent_manager.get_system_status()

    def list_all_agents(self) -> List[Dict[str, Any]]:
        """List information about all controlled agents"""
        return self.agent_manager.list_agents()

    def get_agents_by_role(self, role: str) -> List[str]:
        """Get agent IDs by role"""
        agents = self.agent_manager.get_agents_by_role(role)
        return [agent.id for agent in agents]

    def get_agents_by_capability(self, capability: str) -> List[str]:
        """Get agent IDs that can handle a specific capability"""
        agents = self.agent_manager.get_agents_by_capability(capability)
        return [agent.id for agent in agents]

    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the system"""
        if self.agent_manager.remove_agent(agent_id):
            if agent_id in self.controlled_agents:
                self.controlled_agents.remove(agent_id)
            return True
        return False

    # ===== Original Jarvis Methods =====

    def process(self, user_input: str) -> str:
        """
        Process user input and generate response

        Args:
            user_input: User's message or command

        Returns:
            Jarvis's response
        """
        self.conversation_history.append({
            "role": "user",
            "message": user_input,
            "timestamp": datetime.now().isoformat()
        })

        # Enhanced response logic with agent awareness
        response = self._generate_response(user_input)

        self.conversation_history.append({
            "role": "assistant",
            "message": response,
            "timestamp": datetime.now().isoformat()
        })

        logger.info(f"User: {user_input}")
        logger.info(f"Jarvis: {response}")

        return response

    def _generate_response(self, user_input: str) -> str:
        """Generate response based on user input"""
        lower_input = user_input.lower()

        if "hello" in lower_input:
            return f"Hello! I'm {self.name}. I now have {len(self.controlled_agents)} agents at my disposal. How can I assist you today?"
        elif "create agent" in lower_input or "spawn agent" in lower_input:
            return "I can create specialized agents. Specify the role: scheduler, email_handler, data_analyst, code_assistant, researcher, or monitor."
        elif "agents" in lower_input or "robots" in lower_input:
            status = self.get_system_status()
            return f"I currently control {status['total_agents']} agents. {status['active_agents']} are active, {status['busy_agents']} are busy, {status['idle_agents']} are idle."
        elif "delegate" in lower_input or "task" in lower_input:
            return "I can delegate tasks to my agents. Specify the capability needed and I'll assign it to the best available agent."
        elif "time" in lower_input:
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
        else:
            return "I understand. How can I help you further? I can manage tasks, control agents, or assist with various capabilities."

    def enable_voice(self) -> None:
        """Enable voice interaction mode"""
        self.voice_enabled = True
        logger.info("Voice mode enabled")

    def disable_voice(self) -> None:
        """Disable voice interaction mode"""
        self.voice_enabled = False
        logger.info("Voice mode disabled")

    def create_task(self, task: str, priority: str = "normal", assign_to_agent: bool = False) -> None:
        """
        Create a new task

        Args:
            task: Task description
            priority: Task priority (low, normal, high)
            assign_to_agent: Whether to assign to an agent automatically
        """
        task_record = {
            "id": len(self.tasks) + 1,
            "task": task,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task_record)
        logger.info(f"Task created: {task}")

    def list_tasks(self) -> list:
        """List all tasks"""
        return self.tasks

    def complete_task(self, task_id: int) -> bool:
        """
        Mark a task as complete

        Args:
            task_id: ID of the task to complete

        Returns:
            True if successful, False otherwise
        """
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                logger.info(f"Task completed: {task['task']}")
                return True
        return False

    def get_conversation_history(self) -> list:
        """Get conversation history"""
        return self.conversation_history

    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

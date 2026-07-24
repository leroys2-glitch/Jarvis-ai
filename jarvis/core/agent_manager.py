"""
Agent Manager - Controls creation, lifecycle, and coordination of AI agents
"""

import logging
import uuid
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Define different agent roles and specializations"""
    SCHEDULER = "scheduler"
    EMAIL_HANDLER = "email_handler"
    DATA_ANALYST = "data_analyst"
    CODE_ASSISTANT = "code_assistant"
    RESEARCHER = "researcher"
    MONITOR = "monitor"
    GENERAL = "general"


class AgentStatus(Enum):
    """Agent operational status"""
    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class Agent:
    """Individual AI Agent instance"""

    def __init__(self, agent_id: str, name: str, role: AgentRole, capabilities: List[str]):
        """
        Initialize an AI Agent

        Args:
            agent_id: Unique identifier for the agent
            name: Human-readable name
            role: Role/specialization of the agent
            capabilities: List of capabilities this agent can handle
        """
        self.id = agent_id
        self.name = name
        self.role = role
        self.capabilities = capabilities
        self.status = AgentStatus.IDLE
        self.current_task = None
        self.completed_tasks = []
        self.failed_tasks = []
        self.inbox = []  # Messages from other agents or Jarvis
        self.created_at = datetime.now().isoformat()
        self.last_active = datetime.now().isoformat()

        logger.info(f"Agent created: {self.name} (ID: {self.id}, Role: {self.role.value})")

    def assign_task(self, task: Dict[str, Any]) -> bool:
        """
        Assign a task to this agent

        Args:
            task: Task dictionary with 'id', 'description', 'priority', 'params'

        Returns:
            True if task was assigned, False if agent is busy
        """
        if self.status == AgentStatus.BUSY:
            return False

        self.current_task = task
        self.status = AgentStatus.BUSY
        self.last_active = datetime.now().isoformat()
        logger.info(f"Task assigned to {self.name}: {task.get('id')}")
        return True

    def complete_task(self, result: Any) -> None:
        """Mark current task as completed"""
        if self.current_task:
            task_record = {
                "task_id": self.current_task.get("id"),
                "completed_at": datetime.now().isoformat(),
                "result": result
            }
            self.completed_tasks.append(task_record)
            logger.info(f"Task completed by {self.name}: {self.current_task.get('id')}")

        self.current_task = None
        self.status = AgentStatus.IDLE
        self.last_active = datetime.now().isoformat()

    def fail_task(self, error: str) -> None:
        """Mark current task as failed"""
        if self.current_task:
            task_record = {
                "task_id": self.current_task.get("id"),
                "failed_at": datetime.now().isoformat(),
                "error": error
            }
            self.failed_tasks.append(task_record)
            logger.error(f"Task failed by {self.name}: {self.current_task.get('id')} - {error}")

        self.current_task = None
        self.status = AgentStatus.IDLE
        self.last_active = datetime.now().isoformat()

    def receive_message(self, message: Dict[str, Any]) -> None:
        """
        Receive a message from another agent or Jarvis

        Args:
            message: Message dictionary with 'from', 'content', 'type'
        """
        self.inbox.append({
            "message": message,
            "received_at": datetime.now().isoformat(),
            "read": False
        })
        logger.debug(f"Message received by {self.name} from {message.get('from')}")

    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value,
            "status": self.status.value,
            "capabilities": self.capabilities,
            "current_task": self.current_task,
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "messages_count": len(self.inbox),
            "created_at": self.created_at,
            "last_active": self.last_active
        }


class AgentManager:
    """Manages creation, coordination, and communication between agents"""

    def __init__(self):
        """Initialize the Agent Manager"""
        self.agents: Dict[str, Agent] = {}
        self.agent_registry: Dict[str, List[str]] = self._create_registry()
        self.message_queue: List[Dict[str, Any]] = []
        self.task_queue: List[Dict[str, Any]] = []

        logger.info("Agent Manager initialized")

    @staticmethod
    def _create_registry() -> Dict[str, List[str]]:
        """Create a registry of roles and their capabilities"""
        return {
            AgentRole.SCHEDULER.value: [
                "schedule_meeting",
                "manage_calendar",
                "set_reminder",
                "cancel_event"
            ],
            AgentRole.EMAIL_HANDLER.value: [
                "send_email",
                "read_email",
                "organize_inbox",
                "draft_response"
            ],
            AgentRole.DATA_ANALYST.value: [
                "analyze_data",
                "generate_report",
                "visualize_data",
                "query_database"
            ],
            AgentRole.CODE_ASSISTANT.value: [
                "debug_code",
                "generate_code",
                "review_code",
                "test_code"
            ],
            AgentRole.RESEARCHER.value: [
                "search_information",
                "summarize_content",
                "verify_facts",
                "compile_research"
            ],
            AgentRole.MONITOR.value: [
                "monitor_systems",
                "detect_anomalies",
                "alert_on_issues",
                "track_performance"
            ],
        }

    def create_agent(self, name: str, role: str, custom_capabilities: Optional[List[str]] = None) -> Agent:
        """
        Create a new AI agent

        Args:
            name: Name for the agent
            role: Role from AgentRole enum
            custom_capabilities: Optional custom capabilities list

        Returns:
            Created Agent instance
        """
        agent_id = str(uuid.uuid4())
        agent_role = AgentRole[role.upper()] if role.upper() in AgentRole.__members__ else AgentRole.GENERAL

        # Get default capabilities for role
        capabilities = self.agent_registry.get(agent_role.value, [])

        # Add custom capabilities if provided
        if custom_capabilities:
            capabilities.extend(custom_capabilities)

        agent = Agent(agent_id, name, agent_role, capabilities)
        self.agents[agent_id] = agent

        logger.info(f"Agent created and registered: {name} ({agent_id})")
        return agent

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID"""
        return self.agents.get(agent_id)

    def get_agents_by_role(self, role: str) -> List[Agent]:
        """Get all agents with a specific role"""
        agents = []
        for agent in self.agents.values():
            if agent.role.value == role:
                agents.append(agent)
        return agents

    def get_agents_by_capability(self, capability: str) -> List[Agent]:
        """Get all agents that can handle a specific capability"""
        agents = []
        for agent in self.agents.values():
            if capability in agent.capabilities:
                agents.append(agent)
        return agents

    def find_best_agent(self, required_capability: str) -> Optional[Agent]:
        """
        Find the best available agent for a task

        Prioritizes:
        1. Agents with matching capability
        2. Agents that are idle
        3. Agents with fewer tasks

        Args:
            required_capability: Capability needed

        Returns:
            Best available Agent or None
        """
        candidates = self.get_agents_by_capability(required_capability)

        if not candidates:
            logger.warning(f"No agents found with capability: {required_capability}")
            return None

        # Filter for idle agents
        idle_candidates = [a for a in candidates if a.status == AgentStatus.IDLE]

        if idle_candidates:
            # Return agent with fewest completed tasks (least experienced = fresher)
            return min(idle_candidates, key=lambda a: len(a.completed_tasks))

        # If no idle agents, return least busy
        return min(candidates, key=lambda a: len(a.completed_tasks))

    def delegate_task(self, capability: str, task: Dict[str, Any]) -> bool:
        """
        Delegate a task to the best available agent

        Args:
            capability: Required capability
            task: Task dictionary

        Returns:
            True if task was delegated, False otherwise
        """
        agent = self.find_best_agent(capability)

        if not agent:
            logger.warning(f"Could not find agent for task: {task.get('id')}")
            return False

        success = agent.assign_task(task)

        if success:
            logger.info(f"Task {task.get('id')} delegated to agent {agent.name}")
        else:
            logger.warning(f"Agent {agent.name} could not accept task {task.get('id')}")

        return success

    def send_message(self, from_agent_id: str, to_agent_id: str, content: str, message_type: str = "text") -> bool:
        """
        Send a message from one agent to another

        Args:
            from_agent_id: Sender agent ID
            to_agent_id: Receiver agent ID
            content: Message content
            message_type: Type of message (text, task_update, alert, etc.)

        Returns:
            True if message was sent successfully
        """
        sender = self.get_agent(from_agent_id)
        receiver = self.get_agent(to_agent_id)

        if not sender or not receiver:
            logger.error(f"Invalid agent IDs: from={from_agent_id}, to={to_agent_id}")
            return False

        message = {
            "from": sender.name,
            "from_id": from_agent_id,
            "to_id": to_agent_id,
            "content": content,
            "type": message_type,
            "timestamp": datetime.now().isoformat()
        }

        receiver.receive_message(message)
        logger.info(f"Message sent from {sender.name} to {receiver.name}")
        return True

    def broadcast_message(self, from_agent_id: str, content: str, target_role: Optional[str] = None) -> int:
        """
        Broadcast a message to multiple agents

        Args:
            from_agent_id: Sender agent ID
            content: Message content
            target_role: Optional role to target (broadcasts to all if None)

        Returns:
            Number of agents that received the message
        """
        sender = self.get_agent(from_agent_id)
        if not sender:
            logger.error(f"Invalid agent ID: {from_agent_id}")
            return 0

        if target_role:
            targets = self.get_agents_by_role(target_role)
        else:
            targets = [a for a in self.agents.values() if a.id != from_agent_id]

        message = {
            "from": sender.name,
            "from_id": from_agent_id,
            "content": content,
            "type": "broadcast",
            "timestamp": datetime.now().isoformat()
        }

        count = 0
        for agent in targets:
            agent.receive_message(message)
            count += 1

        logger.info(f"Broadcast message sent to {count} agents by {sender.name}")
        return count

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        total_agents = len(self.agents)
        active_agents = sum(1 for a in self.agents.values() if a.status != AgentStatus.OFFLINE)
        busy_agents = sum(1 for a in self.agents.values() if a.status == AgentStatus.BUSY)
        idle_agents = sum(1 for a in self.agents.values() if a.status == AgentStatus.IDLE)

        return {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "busy_agents": busy_agents,
            "idle_agents": idle_agents,
            "total_tasks": len(self.task_queue),
            "pending_messages": len(self.message_queue),
            "agents": [a.get_info() for a in self.agents.values()]
        }

    def list_agents(self) -> List[Dict[str, Any]]:
        """Get information about all agents"""
        return [agent.get_info() for agent in self.agents.values()]

    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the system"""
        if agent_id in self.agents:
            agent = self.agents.pop(agent_id)
            logger.info(f"Agent removed: {agent.name} ({agent_id})")
            return True
        return False

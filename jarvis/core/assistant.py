"""
Main Jarvis AI Assistant Class
"""

import yaml
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class JarvisAI:
    """Main Jarvis Assistant Class"""

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

        logger.info(f"Initializing {self.name} AI Assistant")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}")
            return {}

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

        # Simple response logic (can be expanded with NLP)
        if "hello" in user_input.lower():
            response = f"Hello! I'm {self.name}. How can I assist you today?"
        elif "task" in user_input.lower():
            response = "I can help you manage your tasks. What would you like to do?"
        elif "time" in user_input.lower():
            response = f"The current time is {datetime.now().strftime('%H:%M:%S')}"
        else:
            response = "I understand. How can I help you further?"

        self.conversation_history.append({
            "role": "assistant",
            "message": response,
            "timestamp": datetime.now().isoformat()
        })

        logger.info(f"User: {user_input}")
        logger.info(f"Jarvis: {response}")

        return response

    def enable_voice(self) -> None:
        """Enable voice interaction mode"""
        self.voice_enabled = True
        logger.info("Voice mode enabled")

    def disable_voice(self) -> None:
        """Disable voice interaction mode"""
        self.voice_enabled = False
        logger.info("Voice mode disabled")

    def create_task(self, task: str, priority: str = "normal") -> None:
        """
        Create a new task

        Args:
            task: Task description
            priority: Task priority (low, normal, high)
        """
        self.tasks.append({
            "id": len(self.tasks) + 1,
            "task": task,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().isoformat()
        })
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

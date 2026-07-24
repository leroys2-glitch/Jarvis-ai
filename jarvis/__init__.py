"""
Jarvis AI Assistant

An intelligent AI assistant inspired by the butler system from Iron Man.
Now with multi-agent system capabilities for delegating and coordinating tasks.
"""

__version__ = "0.2.0"
__author__ = "Leroy Moens"
__email__ = "leroymoens2@gmail.com"

from jarvis.core.assistant import JarvisAI
from jarvis.core.agent_manager import AgentManager, Agent, AgentRole, AgentStatus

__all__ = [
    "JarvisAI",
    "AgentManager",
    "Agent",
    "AgentRole",
    "AgentStatus"
]

# Jarvis AI Assistant

A sophisticated AI assistant inspired by the intelligent butler system from Iron Man. Jarvis is designed to be a helpful, witty, and capable digital assistant with advanced capabilities and multi-agent coordination.

## Features

### Core Capabilities

- **Natural Language Processing**: Understand and respond to complex conversational requests
- **Task Management**: Create, organize, and track tasks and reminders
- **Information Retrieval**: Search and summarize information from various sources
- **System Control**: Manage device settings, applications, and smart home integration
- **Data Analysis**: Process and analyze data, generate reports and insights
- **Predictive Assistance**: Learn user patterns and anticipate needs
- **Multi-Language Support**: Communicate in multiple languages
- **Context Awareness**: Maintain conversation history and understand context across interactions

### Advanced Features

- **Voice Recognition & Synthesis**: Understand voice commands and respond naturally
- **Scheduling & Calendar Management**: Manage appointments, meetings, and events
- **Email & Communication**: Draft, send, and organize communications
- **Document Processing**: Read, summarize, and create documents
- **Code Assistance**: Help with programming tasks and debugging
- **Research & Knowledge Base**: Access and organize information efficiently
- **Integration Hub**: Connect with external services and APIs
- **Security & Monitoring**: Protect systems and monitor for anomalies
- **Personalization**: Adapt responses and recommendations based on user preferences
- **Humor & Personality**: Maintain a helpful and engaging conversational style

### Multi-Agent System ⭐ NEW

- **Agent Creation**: Spawn specialized AI agents with specific roles and capabilities
- **Task Delegation**: Automatically assign tasks to agents based on required capabilities
- **Agent Communication**: Direct inter-agent messaging for complex task coordination
- **Capability-Based Routing**: Find and utilize the best agent for any task
- **System Monitoring**: Track agent status, workload, and performance
- **Specialized Roles**:
  - **Scheduler**: Handles meeting scheduling, calendar management, reminders
  - **Email Handler**: Manages email composition, sending, organization
  - **Data Analyst**: Performs data analysis, generates reports, visualizations
  - **Code Assistant**: Helps with debugging, code generation, reviews
  - **Researcher**: Searches information, compiles research, verifies facts
  - **Monitor**: Tracks system health, detects anomalies, alerts on issues
  - **General**: Versatile agent for various tasks

## Installation

```bash
git clone https://github.com/leroys2-glitch/Jarvis-ai.git
cd Jarvis-ai
pip install -r requirements.txt
```

## Quick Start

### Basic Conversation

```python
from jarvis import JarvisAI

# Initialize Jarvis
jarvis = JarvisAI(name="Jarvis")

# Have a conversation
response = jarvis.process("What can you help me with today?")
print(response)
```

### Multi-Agent System

```python
from jarvis import JarvisAI

# Initialize Jarvis
jarvis = JarvisAI(name="Jarvis")

# Create specialized agents
scheduler = jarvis.create_agent("Chronos", "scheduler")
email_handler = jarvis.create_agent("Mailbot", "email_handler")
analyst = jarvis.create_agent("DataMind", "data_analyst")

# Delegate tasks to agents
jarvis.delegate_task(
    capability="schedule_meeting",
    task_description="Schedule team meeting for tomorrow at 2 PM",
    priority="high"
)

# Agent-to-agent communication
jarvis.send_agent_message(
    from_agent_id=scheduler,
    to_agent_id=email_handler,
    message="Meeting scheduled. Please send confirmation email."
)

# Monitor system status
status = jarvis.get_system_status()
print(f"Active agents: {status['active_agents']}")
print(f"Agents busy: {status['busy_agents']}")
```

## Project Structure

```
Jarvis-ai/
├── jarvis/
│   ├── __init__.py
│   ├── core/
│   │   ├── assistant.py           # Main Jarvis class with agent management
│   │   ├── agent_manager.py       # Multi-agent system manager
│   │   ├── nlp_engine.py
│   │   └── context_manager.py
│   ├── features/
│   │   ├── task_manager.py
│   │   ├── calendar_manager.py
│   │   ├── voice_engine.py
│   │   └── data_analyzer.py
│   ├── integrations/
│   │   ├── email_client.py
│   │   ├── smart_home.py
│   │   └── external_apis.py
│   └── utils/
│       ├── logger.py
│       └── config.py
├── tests/
│   ├── test_core.py
│   ├── test_agents.py
│   └── test_features.py
├── examples/
│   ├── basic_usage.py
│   └── multi_agent_demo.py        # Comprehensive multi-agent example
├── requirements.txt
├── config.yaml
└── README.md
```

## Configuration

Edit `config.yaml` to customize:
- Assistant name and personality
- Voice preferences and language
- Integrations and API keys
- System responses and behavior
- Agent defaults and capabilities

## Usage Examples

### Basic Conversation
```python
jarvis.process("Schedule a meeting for tomorrow at 2 PM")
```

### Task Management
```python
jarvis.create_task("Finish project report", priority="high")
jarvis.list_tasks()
jarvis.complete_task(task_id=1)
```

### Multi-Agent Task Delegation
```python
# Delegate to best available agent
jarvis.delegate_task(
    capability="analyze_data",
    task_description="Analyze Q4 sales data",
    priority="high"
)

# Get agents with specific capability
capable_agents = jarvis.get_agents_by_capability("send_email")

# Get all agents of a specific role
schedulers = jarvis.get_agents_by_role("scheduler")

# Broadcast message to all agents of a role
jarvis.broadcast_to_agents(
    agent_id=scheduler,
    message="Priority: High - System maintenance at 10 PM",
    target_role="monitor"
)
```

### Data Analysis
```python
data = jarvis.analyze_data(dataset)
jarvis.generate_report(data)
```

### Voice Interaction
```python
jarvis.enable_voice()
# Speak: "Jarvis, what's the weather?"
# Jarvis responds with the answer
```

## Architecture

Jarvis uses a modular, multi-agent architecture with:

- **Main Assistant**: Orchestrates all operations and delegates to agents
- **Agent Manager**: Manages agent lifecycle, communication, and task routing
- **NLP Engine**: Processes and understands natural language
- **Context Manager**: Maintains conversation history and state
- **Feature Modules**: Specialized handlers for different capabilities
- **Integration Layer**: Connects with external services
- **Voice Engine**: Handles speech recognition and synthesis

### Agent System Architecture

```
┌─────────────────────┐
│   JarvisAI (Main)   │
└──────────┬──────────┘
           │
           ├─► AgentManager
           │   ├─► Agent Registry
           │   ├─► Message Queue
           │   └─► Task Queue
           │
           ├─► Agent (Scheduler)
           ├─► Agent (EmailHandler)
           ├─► Agent (DataAnalyst)
           ├─► Agent (CodeAssistant)
           ├─► Agent (Researcher)
           └─► Agent (Monitor)
```

## Agent Methods

### Creating and Managing Agents
```python
# Create agent
agent_id = jarvis.create_agent(name="AgentName", role="scheduler")

# Get agent status
status = jarvis.get_agent_status(agent_id)

# List all agents
all_agents = jarvis.list_all_agents()

# Remove agent
jarvis.remove_agent(agent_id)
```

### Task Delegation
```python
# Delegate task (automatically routes to best agent)
success = jarvis.delegate_task(
    capability="schedule_meeting",
    task_description="Book conference room for 3 PM",
    priority="normal"
)
```

### Agent Communication
```python
# Send direct message between agents
jarvis.send_agent_message(
    from_agent_id=agent1_id,
    to_agent_id=agent2_id,
    message="Task complete, here are the results..."
)

# Broadcast to multiple agents
jarvis.broadcast_to_agents(
    agent_id=sender_id,
    message="System update incoming",
    target_role="monitor"  # optional
)
```

### System Monitoring
```python
# Get overall system status
status = jarvis.get_system_status()
# Returns: total_agents, active_agents, busy_agents, idle_agents, etc.

# Find agents by capability
agents = jarvis.get_agents_by_capability("send_email")

# Find agents by role
schedulers = jarvis.get_agents_by_role("scheduler")
```

## Examples

Run the comprehensive multi-agent demo:
```bash
python examples/multi_agent_demo.py
```

This demonstrates:
- Creating specialized agents
- System status monitoring
- Task delegation to multiple agents
- Agent-to-agent communication
- Finding agents by role and capability
- Natural language interaction

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Roadmap

- [x] Multi-agent system with capability-based routing
- [x] Inter-agent communication
- [ ] Advanced machine learning capabilities
- [ ] Real-time learning and adaptation
- [ ] Enhanced emotion recognition
- [ ] Predictive analytics expansion
- [ ] Multi-user support with agent persistence
- [ ] Hardware integration
- [ ] Mobile application
- [ ] Agent swarm optimization
- [ ] Hierarchical agent coordination

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Note**: This project is inspired by fictional AI systems and aims to explore the possibilities of intelligent assistant technology. The multi-agent system enables Jarvis to coordinate specialized AI agents for complex task management and execution.

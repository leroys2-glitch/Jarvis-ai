"""
Example usage of Jarvis AI with Multi-Agent System
"""

from jarvis import JarvisAI


def main():
    # Initialize Jarvis
    jarvis = JarvisAI(name="Jarvis")
    
    print("=" * 60)
    print("Jarvis AI - Multi-Agent System Demo")
    print("=" * 60)
    
    # Example 1: Create specialized agents
    print("\n[1] Creating Specialized Agents...")
    scheduler_agent = jarvis.create_agent("Chronos", "scheduler")
    email_agent = jarvis.create_agent("Mailbot", "email_handler")
    analyst_agent = jarvis.create_agent("DataMind", "data_analyst")
    code_agent = jarvis.create_agent("CodeGenius", "code_assistant")
    
    print(f"✓ Created Scheduler Agent: {scheduler_agent}")
    print(f"✓ Created Email Agent: {email_agent}")
    print(f"✓ Created Data Analyst Agent: {analyst_agent}")
    print(f"✓ Created Code Assistant Agent: {code_agent}")
    
    # Example 2: Check system status
    print("\n[2] System Status...")
    status = jarvis.get_system_status()
    print(f"Total Agents: {status['total_agents']}")
    print(f"Active Agents: {status['active_agents']}")
    print(f"Idle Agents: {status['idle_agents']}")
    print(f"Busy Agents: {status['busy_agents']}")
    
    # Example 3: List all agents with details
    print("\n[3] All Agents Details...")
    agents = jarvis.list_all_agents()
    for agent in agents:
        print(f"\n  • {agent['name']} ({agent['role']})")
        print(f"    Status: {agent['status']}")
        print(f"    Capabilities: {', '.join(agent['capabilities'])}")
        print(f"    Completed Tasks: {agent['completed_tasks']}")
    
    # Example 4: Delegate tasks to agents
    print("\n[4] Delegating Tasks...")
    
    # Schedule a meeting
    success = jarvis.delegate_task(
        capability="schedule_meeting",
        task_description="Schedule team meeting for tomorrow at 2 PM",
        priority="high"
    )
    print(f"✓ Schedule Meeting Task: {'Delegated' if success else 'Failed'}")
    
    # Send an email
    success = jarvis.delegate_task(
        capability="send_email",
        task_description="Send project status update to stakeholders",
        priority="normal"
    )
    print(f"✓ Send Email Task: {'Delegated' if success else 'Failed'}")
    
    # Analyze data
    success = jarvis.delegate_task(
        capability="analyze_data",
        task_description="Analyze quarterly sales data and generate report",
        priority="high"
    )
    print(f"✓ Data Analysis Task: {'Delegated' if success else 'Failed'}")
    
    # Debug code
    success = jarvis.delegate_task(
        capability="debug_code",
        task_description="Debug authentication module for login issues",
        priority="high"
    )
    print(f"✓ Code Debug Task: {'Delegated' if success else 'Failed'}")
    
    # Example 5: Send messages between agents
    print("\n[5] Agent-to-Agent Communication...")
    jarvis.send_agent_message(
        from_agent_id=scheduler_agent,
        to_agent_id=email_agent,
        message="Meeting scheduled for tomorrow. Please send confirmation email to attendees."
    )
    print("✓ Message sent from Scheduler to Email Agent")
    
    # Example 6: Get agents by capability
    print("\n[6] Finding Agents by Capability...")
    email_capable = jarvis.get_agents_by_capability("send_email")
    schedule_capable = jarvis.get_agents_by_capability("schedule_meeting")
    print(f"✓ Agents that can send emails: {len(email_capable)}")
    print(f"✓ Agents that can schedule meetings: {len(schedule_capable)}")
    
    # Example 7: Get agents by role
    print("\n[7] Finding Agents by Role...")
    schedulers = jarvis.get_agents_by_role("scheduler")
    analysts = jarvis.get_agents_by_role("data_analyst")
    print(f"✓ Scheduler Agents: {len(schedulers)}")
    print(f"✓ Data Analyst Agents: {len(analysts)}")
    
    # Example 8: Jarvis natural language interaction
    print("\n[8] Jarvis Natural Language Interaction...")
    responses = [
        "Hello Jarvis",
        "How many agents are active?",
        "Create a new data analyst agent",
        "Show me my agents",
    ]
    
    for user_input in responses:
        response = jarvis.process(user_input)
        print(f"\nUser: {user_input}")
        print(f"Jarvis: {response}")
    
    # Example 9: Check individual agent status
    print("\n[9] Individual Agent Status...")
    agent_info = jarvis.get_agent_status(scheduler_agent)
    if agent_info:
        print(f"\nAgent: {agent_info['name']}")
        print(f"Role: {agent_info['role']}")
        print(f"Status: {agent_info['status']}")
        print(f"Capabilities: {', '.join(agent_info['capabilities'][:3])}...")
        print(f"Tasks Completed: {agent_info['completed_tasks']}")
        print(f"Messages: {agent_info['messages_count']}")
    
    # Example 10: Final system status
    print("\n[10] Final System Status...")
    final_status = jarvis.get_system_status()
    print(f"Total Agents: {final_status['total_agents']}")
    print(f"Active Agents: {final_status['active_agents']}")
    print(f"System is operational and ready for commands!")
    
    print("\n" + "=" * 60)
    print("Demo Complete! Jarvis and agents are ready for deployment.")
    print("=" * 60)


if __name__ == "__main__":
    main()

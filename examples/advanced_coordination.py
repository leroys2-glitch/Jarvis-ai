"""
Advanced example - Agent coordination for complex tasks
"""

from jarvis import JarvisAI


def main():
    # Initialize Jarvis
    jarvis = JarvisAI(name="Jarvis")
    
    print("=" * 70)
    print("Jarvis AI - Advanced Agent Coordination Example")
    print("=" * 70)
    
    # Scenario: Complex project management task
    print("\n[SCENARIO] Project Status Report Generation")
    print("-" * 70)
    
    # Step 1: Create specialized agents
    print("\n[Step 1] Creating Agent Team...")
    scheduler = jarvis.create_agent("Chronos", "scheduler")
    data_analyst = jarvis.create_agent("Analytics", "data_analyst")
    researcher = jarvis.create_agent("ResearchBot", "researcher")
    code_expert = jarvis.create_agent("CodeGenius", "code_assistant")
    
    print(f"  ✓ Scheduler: {scheduler}")
    print(f"  ✓ Data Analyst: {data_analyst}")
    print(f"  ✓ Researcher: {researcher}")
    print(f"  ✓ Code Expert: {code_expert}")
    
    # Step 2: Delegate tasks to different agents
    print("\n[Step 2] Delegating Tasks to Agents...")
    
    tasks = [
        ("schedule_meeting", "Schedule stakeholder meeting for next Monday at 10 AM", "high"),
        ("analyze_data", "Analyze project metrics and generate performance report", "high"),
        ("search_information", "Research latest industry trends and competitor updates", "normal"),
        ("debug_code", "Review and optimize database queries", "normal"),
    ]
    
    for capability, description, priority in tasks:
        success = jarvis.delegate_task(capability, description, priority)
        status = "✓ Delegated" if success else "✗ Failed"
        print(f"  {status}: {description[:50]}...")
    
    # Step 3: Setup inter-agent communication
    print("\n[Step 3] Setting Up Agent Communication...")
    
    # Scheduler sends meeting details to researcher
    jarvis.send_agent_message(
        from_agent_id=scheduler,
        to_agent_id=researcher,
        message="Meeting scheduled for Monday 10 AM. Please prepare briefing on industry trends."
    )
    print(f"  ✓ Scheduler → Researcher: Meeting briefing request sent")
    
    # Analyst sends report to scheduler
    jarvis.send_agent_message(
        from_agent_id=data_analyst,
        to_agent_id=scheduler,
        message="Performance report complete: 95% on-time delivery, 12% efficiency improvement"
    )
    print(f"  ✓ Analyst → Scheduler: Performance metrics shared")
    
    # Code expert sends optimization results to analyst
    jarvis.send_agent_message(
        from_agent_id=code_expert,
        to_agent_id=data_analyst,
        message="Database queries optimized. Query time reduced by 40%."
    )
    print(f"  ✓ Code Expert → Analyst: Optimization complete")
    
    # Step 4: Check agent status
    print("\n[Step 4] Agent Status Report...")
    system_status = jarvis.get_system_status()
    print(f"  Total Agents: {system_status['total_agents']}")
    print(f"  Active Agents: {system_status['active_agents']}")
    print(f"  Busy Agents: {system_status['busy_agents']}")
    print(f"  Idle Agents: {system_status['idle_agents']}")
    
    # Step 5: Find agents by capability
    print("\n[Step 5] Capability-Based Agent Discovery...")
    
    schedule_agents = jarvis.get_agents_by_capability("schedule_meeting")
    analysis_agents = jarvis.get_agents_by_capability("analyze_data")
    
    print(f"  Agents that can schedule meetings: {len(schedule_agents)}")
    print(f"  Agents that can analyze data: {len(analysis_agents)}")
    
    # Step 6: Broadcast urgent message
    print("\n[Step 6] Broadcasting Urgent Alert...")
    count = jarvis.broadcast_to_agents(
        agent_id=scheduler,
        message="URGENT: Project deadline moved up by 2 days",
        target_role="scheduler"
    )
    print(f"  ✓ Alert sent to {count} scheduler agent(s)")
    
    # Step 7: Individual agent details
    print("\n[Step 7] Individual Agent Details...")
    for agent_id in [scheduler, data_analyst, researcher, code_expert]:
        agent_info = jarvis.get_agent_status(agent_id)
        if agent_info:
            print(f"\n  Agent: {agent_info['name']}")
            print(f"    Role: {agent_info['role']}")
            print(f"    Status: {agent_info['status']}")
            print(f"    Capabilities: {len(agent_info['capabilities'])} available")
            print(f"    Tasks Completed: {agent_info['completed_tasks']}")
            print(f"    Messages: {agent_info['messages_count']}")
    
    # Step 8: List all agents
    print("\n[Step 8] Full Agent Roster...")
    all_agents = jarvis.list_all_agents()
    for i, agent in enumerate(all_agents, 1):
        print(f"  {i}. {agent['name']} ({agent['role']}) - Status: {agent['status']}")
    
    # Step 9: Simulate natural language queries
    print("\n[Step 9] Natural Language Queries...")
    queries = [
        "How many agents are active?",
        "Which agents can send emails?",
        "What's the system status?",
    ]
    
    for query in queries:
        response = jarvis.process(query)
        print(f"\n  User: {query}")
        print(f"  Jarvis: {response}")
    
    # Step 10: Summary
    print("\n[Summary]")
    print("-" * 70)
    final_status = jarvis.get_system_status()
    print(f"✓ Project team assembled: {final_status['total_agents']} specialized agents")
    print(f"✓ Tasks delegated: {len(tasks)} parallel task streams")
    print(f"✓ Inter-agent communication: {sum(1 for a in all_agents if a['messages_count'] > 0)} agents coordinating")
    print(f"✓ System Status: Ready for execution")
    
    print("\n" + "=" * 70)
    print("Advanced coordination example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()

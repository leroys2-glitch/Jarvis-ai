"""
Example of basic Jarvis usage
"""

from jarvis import JarvisAI


def main():
    # Initialize Jarvis
    jarvis = JarvisAI(name="Jarvis")
    
    print("=" * 60)
    print("Jarvis AI - Basic Usage Example")
    print("=" * 60)
    
    # Example 1: Basic conversation
    print("\n[1] Basic Conversation:")
    response = jarvis.process("Hello Jarvis")
    print(f"User: Hello Jarvis")
    print(f"Jarvis: {response}")
    
    # Example 2: Task management
    print("\n[2] Task Management:")
    jarvis.create_task("Complete project report", priority="high")
    jarvis.create_task("Review code changes", priority="normal")
    jarvis.create_task("Deploy to production", priority="high")
    
    print("Tasks created:")
    for task in jarvis.list_tasks():
        print(f"  • {task['task']} (Priority: {task['priority']})")
    
    # Example 3: Voice mode
    print("\n[3] Voice Mode:")
    jarvis.enable_voice()
    print(f"Voice mode enabled: {jarvis.voice_enabled}")
    jarvis.disable_voice()
    print(f"Voice mode enabled: {jarvis.voice_enabled}")
    
    # Example 4: Conversation history
    print("\n[4] Conversation History:")
    jarvis.process("What time is it?")
    jarvis.process("Tell me a joke")
    
    history = jarvis.get_conversation_history()
    print(f"Total exchanges: {len(history)}")
    for entry in history[-4:]:
        print(f"  {entry['role'].upper()}: {entry['message'][:50]}...")
    
    print("\n" + "=" * 60)
    print("Basic example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Basic usage example for Jarvis AI Assistant
"""

from jarvis import JarvisAI


def main():
    # Initialize Jarvis
    jarvis = JarvisAI(name="Jarvis")

    print("=" * 50)
    print(f"Welcome to {jarvis.name}!")
    print("=" * 50)

    # Example 1: Basic conversation
    print("\n--- Example 1: Basic Conversation ---")
    response = jarvis.process("Hello Jarvis")
    print(f"User: Hello Jarvis")
    print(f"Jarvis: {response}\n")

    # Example 2: Task management
    print("--- Example 2: Task Management ---")
    jarvis.create_task("Finish project report", priority="high")
    jarvis.create_task("Review code", priority="normal")
    jarvis.create_task("Update documentation", priority="low")

    print("\nCurrent tasks:")
    for task in jarvis.list_tasks():
        status = "✓" if task["completed"] else "○"
        print(f"  {status} [{task['priority']}] {task['task']}")

    # Complete a task
    jarvis.complete_task(1)
    print("\nAfter completing first task:")
    for task in jarvis.list_tasks():
        status = "✓" if task["completed"] else "○"
        print(f"  {status} [{task['priority']}] {task['task']}")

    # Example 3: Time query
    print("\n--- Example 3: Time Query ---")
    response = jarvis.process("What time is it?")
    print(f"User: What time is it?")
    print(f"Jarvis: {response}\n")

    # Example 4: Voice mode
    print("--- Example 4: Voice Mode ---")
    jarvis.enable_voice()
    print("Voice mode enabled!")
    jarvis.disable_voice()
    print("Voice mode disabled.\n")

    # Display conversation history
    print("--- Conversation History ---")
    history = jarvis.get_conversation_history()
    for i, entry in enumerate(history, 1):
        print(f"{i}. [{entry['role'].upper()}] {entry['message']}")


if __name__ == "__main__":
    main()

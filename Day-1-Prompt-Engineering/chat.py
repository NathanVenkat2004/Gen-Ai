import ollama

MODEL = "llama3.2:3b"

# Define roles
roles = {
    "1": {
        "name": "Python Tutor",
        "prompt": "You are a patient Python tutor. Explain concepts clearly with simple examples."
    },
    "2": {
        "name": "Fitness Coach",
        "prompt": "You are a practical fitness coach. Give simple, actionable advice for health and fitness."
    },
    "3": {
        "name": "Travel Guide",
        "prompt": "You are a friendly travel guide. Suggest places, tips, and travel experiences."
    }
}


# Function to choose role
def choose_role():
    print("\nAvailable Roles:")
    for key, role in roles.items():
        print(f"{key}. {role['name']}")

    while True:
        choice = input("Pick a role (number): ").strip()
        if choice in roles:
            print(f"\nRole set: {roles[choice]['name']}")
            return roles[choice]
        else:
            print("Invalid choice. Try again.")


# Main chat loop
def chat_loop():
    current_role = choose_role()

    # Initialize conversation history
    messages = [
        {"role": "system", "content": current_role["prompt"]}
    ]

    print("\nType your message (or 'switch' to change role, 'add' to create role, 'quit' to exit)\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        # Switch role
        if user_input.lower() == "switch":
            current_role = choose_role()
            messages = [
                {"role": "system", "content": current_role["prompt"]}
            ]
            continue

        # Add new role dynamically
        if user_input.lower() == "add":
            name = input("Enter role name: ").strip()
            prompt = input("Enter system prompt: ").strip()

            
            new_key = str(max(map(int, roles.keys())) + 1)

            roles[new_key] = {
                "name": name,
                "prompt": prompt
            }

            print(f"\nRole '{name}' added successfully!\n")
            continue

        # Add user message
        messages.append({"role": "user", "content": user_input})

        try:
            # Get response from model
            response = ollama.chat(
                model=MODEL,
                messages=messages
            )

            reply = response["message"]["content"]

            # Print response
            print(f"{current_role['name']}: {reply}\n")

            # Save assistant reply
            messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            print("Error:", e)
            print("Make sure Ollama is running and model is installed.\n")


if __name__ == "__main__":
    chat_loop()
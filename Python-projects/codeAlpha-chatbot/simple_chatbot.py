def get_reply(message):
    message = message.lower().strip()

    if message == "hello":
        return "Hi!"
    elif message == "how are you":
        return "I'm fine, thanks!"
    elif message == "what is your name":
        return "I'm a simple chatbot."
    elif message == "thanks":
        return "You're welcome!"
    else:
        return "Sorry, I don't understand."


name = input("What is your name? ")
print(f"Hi {name}, how are you?")

user_input = input("Say something (type 'bye' to quit): ")

while user_input.lower().strip() != "bye":
    print(get_reply(user_input))
    user_input = input("Say something (type 'bye' to quit): ")

print("Goodbye!")
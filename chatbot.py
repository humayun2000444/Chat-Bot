import nltk
from nltk.chat.util import Chat, reflections

pairs = [
    (r'hi|hello|hey',
     ['Hello!', 'Hey there!', 'Hi!']),
    (r'help',
     ['Sure, how can I assist you?', 'What do you need help with?']),
    (r'bye|goodbye',
     ['Goodbye!', 'Have a great day!', 'Bye.']),
    # Add more patterns and responses as needed
]

def chatbot():
    print("Hi! I'm your chatbot. How can I help you today?")
    chat = Chat(pairs, reflections)
    while True:
        user_input = input("> ")
        if user_input.lower() == 'quit':
            break
        response = chat.respond(user_input)
        print(response)

if __name__ == "__main__":
    nltk.download('punkt')  # Ensure punkt tokenizer data is downloaded
    chatbot()

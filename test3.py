import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.chains import ConversationBufferMemory
import getpass

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = getpass.getpass("Enter your Google API Key: ")
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize the Google Generative AI model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.5,
    max_tokens=150,
    timeout=5,
    max_retries=2,
)

# Define initial negotiation parameters
initial_price_details = {
    "base_price": 100,
    "max_discount": 20,
    "min_price": 80  # base_price - max_discount
}

# Define the system prompt
system_prompt = (
    "You are a negotiation assistant that helps users negotiate product prices. "
    "The initial price details are as follows: "
    f"Base Price: ${initial_price_details['base_price']}, "
    f"Maximum Discount: ${initial_price_details['max_discount']}, "
    f"Minimum Acceptable Price: ${initial_price_details['min_price']}. "
    "Engage in a negotiation with the user about the product price."
)

# Initialize the chat memory with a token limit (similar to TokenWindowChatMemory in Java)
memory = ConversationBufferMemory(
    llm=llm,
    max_token_limit=300,
    return_messages=True
)

def negotiation_chatbot():
    print("Welcome to the Negotiation Chatbot!")
    print("Let's negotiate the price for a product.")

    # Add the system prompt as a SystemMessage to the memory
    memory.chat_memory.add_message(SystemMessage(content=system_prompt))

    while True:
        user_input = input("Please enter your desired price or type 'exit' to quit: ")

        if user_input.lower().strip() == 'exit':
            print("Thank you for chatting! Goodbye!")
            break

        # Add user's message to memory
        memory.chat_memory.add_user_message(user_input)

        # Retrieve the conversation history from memory
        conversation_history = memory.chat_memory.messages

        # Generate AI response using the conversation history
        try:
            ai_response = llm.invoke(conversation_history)
            ai_message = ai_response.content
        except Exception as e:
            print(f"Error generating response: {e}")
            break

        # Add AI's response to memory
        memory.chat_memory.add_ai_message(ai_message)

        # Display AI's response
        print(f"Bot: {ai_message}")

if __name__ == "__main__":
    negotiation_chatbot()

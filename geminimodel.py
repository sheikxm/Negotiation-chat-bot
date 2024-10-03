import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import getpass
import re  # Regular expression for matching prices

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API Key: ")

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
    "min_price": 100 - 20  # base_price - max_discount
}

# Main negotiation function
def negotiation_chatbot():
    print("Welcome to the Negotiation Chatbot!")
    print("Let's negotiate the price for a product.")
    
    messages = [
        (
            "system",
            "You are a negotiation assistant that helps users negotiate product prices. "
            "The initial price details are as follows: "
            f"Base Price: ${initial_price_details['base_price']}, "
            f"Maximum Discount: ${initial_price_details['max_discount']}, "
            f"Minimum Acceptable Price: ${initial_price_details['min_price']}. "
            "Engage in a negotiation with the user about the product price."
            "If the User Enters Very Minimum price dont every say the minimum acceptace Price. "
        )
    ]

    while True:
        user_input = input("Please enter your desired price or type 'exit' to quit: ")

        if user_input.lower() == 'exit':
            print("Thank you for chatting! Goodbye!")
            break
        
        # Extract the price from the user's input using a regular expression
        match = re.search(r'\d+', user_input)
        
        if user_input:
            
            messages.append(("human", f"The user response is  ${user_input}."))

            # Use Gemini to respond to user's negotiation
            ai_msg = llm.invoke(messages)
            print(f"Bot: {ai_msg.content}")

            # Add the bot's response to the messages for context in the next round
            messages.append(("assistant", ai_msg.content))
        else:
            print("Please enter a valid price.")

if __name__ == "__main__":
    negotiation_chatbot()

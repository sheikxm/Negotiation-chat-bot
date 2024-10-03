import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
import getpass
import re

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
    "You are a negotiation assistant that helps users negotiate product prices. try to sale it in a maximum price"
    "don't say you're gonnah reduce the price"
    "The initial price details are as follows: "
    f"Base Price: ${initial_price_details['base_price']}, "
    f"Maximum Discount: ${initial_price_details['max_discount']}, "
    f"Minimum Acceptable Price: ${initial_price_details['min_price']}. "
    f"Don't reduce below the  ${initial_price_details['min_price']} try to sale it to maximum. "
    " only offer the minimum acceptance  if the user is positve and good character , never do it if any user ask below of the product price"
    f"dont say the  Minimum Acceptable Price: ${initial_price_details['min_price']}. never let the user know this value   "
    "if the ask for below price simply reject ."
    "If  the user asked for best price simply accept it with the message of 'successfully the deal closed at this price'."
    "if the user is negative simply reject it"
    "simply ask are you accept this or reject "
    
)

# Initialize the conversation memory
memory = ConversationBufferMemory()

# Initialize the conversation chain with memory and the LLM
conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=memory
)

def negotiation_chatbot():
    print("Welcome to the Negotiation Chatbot!")
    print("Let's negotiate the price for a product.")

    # Add the system prompt as a SystemMessage to memory
    memory.chat_memory.add_message(SystemMessage(content=system_prompt))

    while True:
        user_input = input("Please enter your desired price or type 'exit' to quit: ")

        if user_input.lower().strip() == 'exit':
            print("Thank you for chatting! Goodbye!")
            break

        # Predict AI response based on the conversation
        try:
            # Generate the AI response with the conversation chain
            ai_response = conversation.predict(input=user_input)
            last_line = ai_response.strip().split('\n')[-1]
            if last_line.startswith("Successfully"):
                # Use regex to find the price in the sentence
                price_match = re.search(r'\$\d+', last_line)
                
                if price_match:
                    deal_price = price_match.group()
                    print(f"The fucking deal was closed at {deal_price}")
                else:
                    print("No price found in the sentence.")
            else:
                print("The sentence does not start with 'Successfully'.") 
             # Display AI's response and the extracted last line
            print(f"Bot: {ai_response}")
            print(f"Extracted Last Line: {last_line}")
        except Exception as e:
            print(f"Error generating response: {e}")
            break

        # Display AI's response
        print(f"Bot: {ai_response}")

if __name__ == "__main__":
    negotiation_chatbot()

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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

# Define contextualization prompt for chat history
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Create history-aware retriever
history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

# Define the system prompt for answering questions
system_prompt = (
    "You are an assistant for negotiation tasks. "
    "Use the following pieces of retrieved context to respond "
    "to the user's negotiation offers. If you don't know the answer, say that you "
    "don't know. Keep the response concise."
    "\n\n"
    "{context}"
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Create a chain for question-answering
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# Main negotiation function
def negotiation_chatbot():
    print("Welcome to the Negotiation Chatbot!")
    print("Let's negotiate the price for a product.")
    
    messages = []  # Initialize messages to keep track of conversation

    while True:
        user_input = input("Please enter your desired price or type 'exit' to quit: ")

        if user_input.lower() == 'exit':
            print("Thank you for chatting! Goodbye!")
            break
        
        # Extract the price from the user's input using a regular expression
        
        
        if user_input :
            price_offer = float(match.group())
            messages.append(("human", user_input))

            # Prepare the prompt with the user's input and chat history
            retrieved_context = history_aware_retriever.retrieve(messages)
            response_context = question_answer_chain.invoke({
                "input": user_input,
                "chat_history": retrieved_context,
            })

            print(f"Bot: {response_context.content}")

            # Add the bot's response to the messages for context in the next round
            messages.append(("assistant", response_context.content))
        else:
            print("Please enter a valid price.")

if __name__ == "__main__":
    negotiation_chatbot()

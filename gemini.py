import getpass
import os
from dotenv import load_dotenv
from typing import Sequence

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import Annotated, TypedDict


# Load the Google API key from .env file or request it securely
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your GOOGLE_API_KEY: ")

# Initialize the Gemini model from Langchain
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Setting up a system prompt for question-answering task with Gemini
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of context to answer the question. "
    "If you don't know the answer, say that you don't know. "
    "Use three sentences maximum and keep the answer concise."
    "\n\n"
    "{context}"
)

# Define a Chat Prompt with placeholder for chat history and human input
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),  # Placeholder for history
        ("human", "{input}"),  # User input
    ]
)

# Simple question-answer chain setup with Gemini and prompt
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)


# Define a state to hold chat history and current input/output
class State(TypedDict):
    input: str
    chat_history: Annotated[Sequence[BaseMessage], add_messages]
    context: str
    answer: str


# Function to invoke the LLM chain and update chat history
def call_model(state: State):
    response = question_answer_chain.invoke(state)
    return {
        "chat_history": [
            HumanMessage(state["input"]),
            AIMessage(response["answer"]),
        ],
        "context": response["context"],
        "answer": response["answer"],
    }


# Create a state graph for managing chat history flow
workflow = StateGraph(state_schema=State)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Compile the workflow with a memory saver (in-memory persistence for this case)
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Function to simulate conversation with Gemini
def chat_with_gemini(input_message: str, config: dict):
    # Simulate invoking the model
    result = app.invoke({"input": input_message}, config=config)
    # Return the response and update chat history
    print(f"Gemini: {result['answer']}")
    return result

# Configuration for chat session
config = {"configurable": {"thread_id": "abc123"}}

# Example usage: Chatting with the Gemini model
response_1 = chat_with_gemini("What is machine learning?", config=config)
response_2 = chat_with_gemini("Can you explain supervised learning?", config=config)
response_3 = chat_with_gemini("How does overfitting occur?", config=config)

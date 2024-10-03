from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

import getpass

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

memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=memory
)

# conversation.predict(input="Hi there! I am Sam")
# conversation.predict(input="can you guess my name")
print(conversation.memory.buffer)
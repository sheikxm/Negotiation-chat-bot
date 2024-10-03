from fastapi import FastAPI
from pydantic import BaseModel
from threading import Lock
import requests
from concurrent.futures import ThreadPoolExecutor
from langchain.llms import LLM

# Initialize FastAPI app
app = FastAPI()

# Create a Lock to ensure thread-safe operations
lock = Lock()

# Define the Gemini LLM using LangChain's LLM wrapper
class GeminiLLM(LLM):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _call(self, prompt: str, stop=None):
        # Locking the thread to avoid race conditions when accessing the API
        with lock:
            response = requests.post(
                "https://api.gemini.com/v1/negotiate",  # Example Gemini API endpoint
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"prompt": prompt}
            )
            return response.json().get('response', 'API error')

    @property
    def _identifying_params(self):
        return {"api_key": self.api_key}

# Initialize Gemini API key and LangChain LLM
gemini_llm = GeminiLLM(api_key="your_gemini_api_key")

# Basic input model for negotiation
class NegotiationInput(BaseModel):
    customer_message: str
    product: str
    initial_price: float
    desired_price: float

# Thread pool for concurrency
executor = ThreadPoolExecutor(max_workers=5)

# Function to handle the negotiation with Gemini LLM
def handle_negotiation(input: NegotiationInput):
    prompt = f"The customer wants to negotiate the price for {input.product}. Their message: {input.customer_message}"
    bot_response = gemini_llm._call(prompt)
    
    return {
        "supplier_response": bot_response,
        "initial_price": input.initial_price,
        "desired_price": input.desired_price
    }

# FastAPI endpoint to negotiate price
@app.post("/negotiate/")
async def negotiate(input: NegotiationInput):
    # Execute the negotiation in parallel using ThreadPoolExecutor
    future = executor.submit(handle_negotiation, input)
    result = future.result()

    return result

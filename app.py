from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FastAPI setup
app = FastAPI()

# Mount static files (for serving CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates (for serving HTML pages)
templates = Jinja2Templates(directory="templates")

# Set up the Gemini (Google Generative AI) LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.4,
    max_tokens=100,
    timeout=10,
    max_retries=3
)

# Define negotiation input model
class NegotiationInput(BaseModel):
    product: str
    price: int
    user_input: str

# Define the negotiation logic using Gemini AI
def negotiate_with_ai(price, user_input):
    messages = [
        ("system", "You are a negotiation assistant for a supplier."),
        ("human", f"The customer offered ${price}. The customer said: '{user_input}'. Respond with a negotiation message."),
    ]
    
    # Generate a response using Gemini via Langchain
    ai_msg = llm.invoke(messages)
    
    return ai_msg.content

# POST endpoint for handling negotiation requests
@app.post("/negotiate")
async def negotiate_price(negotiation: NegotiationInput):
    product = negotiation.product
    initial_price = negotiation.price
    user_input = negotiation.user_input
    
    # Call the AI-based negotiation function
    response = negotiate_with_ai(initial_price, user_input)
    
    return {"product": product, "negotiation_response": response}

# Serve the HTML page (index page)
@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

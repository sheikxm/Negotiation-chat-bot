import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
import re

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Google API Key not found in environment variables")

# Initialize the FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the URL of your frontend if it's hosted elsewhere
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, including POST
    allow_headers=["*"],  # Allow all headers, including Content-Type, Authorization, etc.
)
# Initialize the Google Generative AI model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.5,
    max_tokens=150,
    timeout=5,
    max_retries=2,
)

# Initialize conversation memory
memory = ConversationBufferMemory()
# Initialize the conversation chain with memory and the LLM
conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=memory
)
# Define the schema for incoming price data
class PriceDetails(BaseModel):
    base_price: float
    max_discount: float
    min_price: float
    user_input: str

# Negotiation chatbot logic
def create_negotiation_prompt(price_details):
    system_prompt = (
      "You are a negotiation assistant that helps users negotiate product prices. try to sale it in a maximum price"
      "don't say you're gonnah reduce the price"
      "The initial price details are as follows: "
      f"Base Price: ${price_details['base_price']}, "
      f"Maximum Discount: ${price_details['max_discount']}, "
      f"Minimum Acceptable Price: ${price_details['min_price']}. "
      f"Don't reduce below the  ${price_details['min_price']} try to sale it to maximum. "
      " only offer the minimum acceptance  if the user is positve and good character , never do it if any user ask below of the product price"
      f"dont say the  Minimum Acceptable Price: ${price_details['min_price']}. never let the user know this value   "
      "if the ask for below price simply reject ."
      "If  the user asked for best price simply accept it with the message of 'successfully the deal closed at this price'."
      "if the user is negative simply reject it"
      "if the user is not accepting your offer for 4 times then say 'sorry your offer is rejected Thank You' ."
      "always use chat "
    )
    return system_prompt

# Endpoint to receive price details and start negotiation
@app.post("/negotiate/")
async def negotiate(price_details: PriceDetails, request: Request):
    # Add system prompt to the memory with price details
    # Clear memory for each new negotiation
    system_prompt = create_negotiation_prompt(price_details.dict())
    memory.chat_memory.add_message(SystemMessage(content=system_prompt))

    # Parse the user's price input from the request body
    body = await request.json()
    user_input = body.get("user_input", "")
    
    if not user_input:
        raise HTTPException(status_code=400, detail="User input not provided")

    try:
        # Predict AI response based on the user input
        conversation = ConversationChain(llm=llm, verbose=False, memory=memory)
        ai_response = conversation.predict(input=user_input)

        # Extract last line from AI response
        last_line = ai_response.strip().split('\n')[-1]

        # Check if deal is successfully closed
        if last_line.startswith("Successfully"):
            # Use regex to find the price in the sentence
            price_match = re.search(r'\$\d+', last_line)
            if price_match:
                deal_price = price_match.group()
                return {"response": f"Deal closed successfully at {deal_price}"}
            else:
                return {"message": "No price found in the response."}
        else:
            return {"response": ai_response, "message": "Negotiation is ongoing."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

# Start FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

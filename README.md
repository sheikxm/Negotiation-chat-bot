# Price Negotiation Chatbot with FastAPI and Google Generative AI
![Screenshot of Chatbot](https://github.com/sheikxm/Negotiation-chat-bot/blob/main/Images/Screenshot%20from%202024-10-04%2001-59-12.png)
![Screenshot of Chatbot](https://github.com/sheikxm/Negotiation-chat-bot/blob/main/Images/Screenshot%20from%202024-10-04%2001-59-43.png)


This project is a FastAPI-based chatbot that simulates price negotiations for products. The chatbot integrates with Google Generative AI (LangChain framework) to negotiate prices with users based on predefined rules and logic. The chatbot tries to maximize the sale price while adhering to minimum acceptable price rules.

## Features

- **Interactive Price Negotiation:** The chatbot negotiates prices with users using predefined logic to maximize sale price.
- **Google Generative AI Integration:** Uses Google Generative AI for natural language conversation.
- **Customizable Negotiation Logic:** The chatbot adjusts behavior based on user inputs, such as rejecting offers or closing deals.
- **FastAPI Backend:** The app is built with FastAPI for performance and simplicity.
- **CORS Support:** Allows easy integration with frontend applications.

## Installation

### Prerequisites

- Python 3.8+
- FastAPI
- LangChain
- Google Generative AI API Access
- dotenv for environment variable management

### Install Dependencies

```bash
pip install fastapi pydantic langchain_google_genai python-dotenv uvicorn

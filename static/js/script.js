// Function to start the negotiation with the chatbot
function startNegotiation(productName, initialPrice) {
    // Display the chatbot
    document.querySelector('.chatbox').style.display = 'block';

    // Post initial price to the server
    fetch('/negotiate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product: productName,
            price: initialPrice
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display the initial message from the server in the chat
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML += `<p>Chatbot: Initial price for ${productName} is $${initialPrice}. Server response: ${data.message}</p>`;
        messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to the latest message
    })
    .catch(error => console.error('Error:', error));
}

// Send button functionality
document.getElementById('sendBtn').addEventListener('click', function() {
    const userInput = document.getElementById('userInput').value;
    const messagesDiv = document.getElementById('messages');
    
    // Display the user's message
    messagesDiv.innerHTML += `<p>You: ${userInput}</p>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to the latest message
    
    // Clear input field
    document.getElementById('userInput').value = '';
    
    // Simulate chatbot response
    messagesDiv.innerHTML += `<p>Chatbot: You entered ${userInput}</p>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

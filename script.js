document.addEventListener('DOMContentLoaded', () => {
    const products = document.querySelectorAll('.buy-btn');
    const chatModal = document.getElementById('chat-modal');
    const closeModal = document.querySelector('.close');
    const chatContent = document.getElementById('chat-content');
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    
    let selectedProductPrice = 0;
    let selectedProductId = 0;

    // Open chatbot modal on 'Buy' button click
    products.forEach((btn) => {
        btn.addEventListener('click', (event) => {
            const productElement = event.target.closest('.product');
            selectedProductId = productElement.dataset.id;
            selectedProductPrice = parseFloat(productElement.querySelector('p').textContent.replace('Price: $', ''));
            
            // Open chat modal
            chatModal.style.display = "block";
            
            // Display product details in chat
            chatContent.innerHTML += `<p>Bot: You are negotiating for Product ${selectedProductId}. The initial price is $${selectedProductPrice}.</p>`;
        });
    });

    // Close the chat modal
    closeModal.addEventListener('click', () => {
        chatModal.style.display = "none";
        chatContent.innerHTML = "";  // Clear chat content
    });

    // Send user input to the FastAPI server
    sendBtn.addEventListener('click', async () => {
        const userPrice = userInput.value.trim();
        if (userPrice === "") return;

        // Calculate the minimum price based on 20% discount
        const maxDiscount = selectedProductPrice * 0.20;
        const minPrice = selectedProductPrice - maxDiscount;

        // Send request to FastAPI server
        const response = await fetch('http://127.0.0.1:8000/negotiate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                base_price: selectedProductPrice,
                max_discount: maxDiscount,
                min_price: minPrice,
                user_input: userPrice
            })
        });

        const data = await response.json();
        chatContent.innerHTML += `<p>User: ${userPrice}</p>`;
        chatContent.innerHTML += `<p>Bot: ${data.response}</p>`;

        userInput.value = "";  // Clear the input field
    });
});

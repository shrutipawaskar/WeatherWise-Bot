document.getElementById("send-button").addEventListener("click", function() {
    const userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return; // Prevent sending empty messages

    appendMessage(userInput, 'user'); // Append user message
    document.getElementById("user-input").value = ''; // Clear input field
    document.getElementById("send-button").disabled = true; // Disable button
    document.getElementById("loading").style.display = "block"; // Show loading

    getResponse(userInput); // Fetch response from the chatbot
});

function appendMessage(message, sender) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("div");
    messageElement.className = sender === 'user' ? 'user-message' : 'bot-message'; // Set class based on sender
    messageElement.textContent = (sender === 'user' ? "You: " : "Chatbot: ") + message; // Prefix message
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

function getResponse(userInput) {
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: userInput })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage(data.response, 'bot'); // Append bot response
    })
    .catch(error => {
        appendMessage("Sorry, I couldn't fetch the response.", 'bot'); // Handle errors
    })
    .finally(() => {
        document.getElementById("send-button").disabled = false; // Re-enable button
        document.getElementById("loading").style.display = "none"; // Hide loading
    });
}
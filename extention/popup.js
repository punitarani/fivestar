document.addEventListener("DOMContentLoaded", function () {
    const quoteElement = document.getElementById("quote");
    const urlElement = document.getElementById("url");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const chatHistory = document.getElementById("chat-history");

    // Fetch a new quote when the popup is opened
    fetchNewQuote();

    // Get the current tab's URL and display it in the popup
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
        const currentUrl = tabs[0].url;
        urlElement.textContent = currentUrl;
    });

    // Function to fetch a new quote
    function fetchNewQuote() {
        fetch("https://api.quotable.io/random")
            .then(response => response.json())
            .then(data => {
                quoteElement.textContent = data.content;
            })
            .catch(error => {
                quoteElement.textContent = "Failed to fetch quote";
                console.error(error);
            });
    }

    sendButton.addEventListener("click", function () {
        const userMessage = userInput.value;
        if (userMessage.trim() !== "") {
            addMessage(userMessage, "user");
            // Call the function to handle the bot's response
            handleBotResponse(userMessage);
            userInput.value = "";
        }
    });

    function handleBotResponse(userMessage) {
        // In this example, the bot simply echoes back the user's message
        addMessage(userMessage, "bot");
    }

    function addMessage(message, sender) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", sender);
        messageElement.textContent = message;
        chatHistory.appendChild(messageElement);
    }
});

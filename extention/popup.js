document.addEventListener("DOMContentLoaded", function () {
    const quoteElement = document.getElementById("quote");
    const urlElement = document.getElementById("url");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const chatHistory = document.getElementById("chat-history");
    const productSummaryElement = document.getElementById("product-summary");

    // Fetch a new quote when the popup is opened
    fetchNewQuote();

    // Get the current tab's URL and display it in the popup
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
        const currentUrl = tabs[0].url;
        urlElement.textContent = currentUrl;

        // Fetch a new product summary when the popup is opened
        fetchProductSummary(currentUrl);
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

    function extractProductId(url) {
        const pattern = /\/dp\/([A-Z0-9]{10})/;
        const match = url.match(pattern);
        if (match && match[1]) {
            return match[1];
        } else {
            return null;
        }
    }

    // Function to fetch a new product summary
    function fetchProductSummary(url) {
        const productId = extractProductId(url);
        fetch(`http://localhost:8000/summarize-product?product_id=${productId}`)
            .then(response => response.json())
            .then(data => {
                productSummaryElement.textContent = data.summary;
            })
            .catch(error => {
                productSummaryElement.textContent = "Failed to fetch product summary";
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

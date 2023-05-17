document.addEventListener("DOMContentLoaded", function () {
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const chatHistory = document.getElementById("chat-history");
    const productSummaryElement = document.getElementById("product-summary");
    const productTitleElement = document.getElementById("product-title");

    // Get the current tab's URL and fetch the product title and summary
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
        const currentUrl = tabs[0].url;
        fetchProductTitle(currentUrl);
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

    // Function to fetch the product title, description and features
    function fetchProductTitle(url) {
        const productId = extractProductId(url);
        fetch(`http://localhost:8000/info?product_id=${productId}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                productTitleElement.textContent = data.title;
                // If description and features are available, display them
                if (data.description) {
                    productSummaryElement.textContent = data.description;
                }
                if (data.features && data.features.length > 0) {
                    for (const feature of data.features) {
                        productSummaryElement.textContent += '\n' + feature;
                    }
                }
                // Add a line indicating that a summary is being generated
                productSummaryElement.textContent += '\n(Summarizing in the background...)';
            })
            .catch(error => {
                productTitleElement.textContent = "Product Information";
                console.error(error);
            });
    }

    // Function to fetch a new product summary
    function fetchProductSummary(url) {
        const productId = extractProductId(url);
        fetch(`http://localhost:8000/summarize-product?product_id=${productId}`)
            .then(response => response.json())
            .then(data => {
                // Overwrite the description and features with the summary
                productSummaryElement.textContent = data.summary;
            })
            .catch(error => {
                // Replace the last line with "Failed to summarize"
                let textContent = productSummaryElement.textContent;
                let lastNewlineIndex = textContent.lastIndexOf('\n');
                if (lastNewlineIndex !== -1) {
                    productSummaryElement.textContent = textContent.substring(0, lastNewlineIndex) + '\n(Failed to summarize)';
                } else {
                    productSummaryElement.textContent = '(Failed to summarize)';
                }
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

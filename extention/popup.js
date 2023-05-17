document.addEventListener("DOMContentLoaded", function () {
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const chatHistory = document.getElementById("chat-history");
    const productSummaryElement = document.getElementById("product-summary");
    const productTitleElement = document.getElementById("product-title");
    const productReviewsElement = document.getElementById("product-reviews");
    const productProsElement = document.getElementById("product-pros");
    const productConsElement = document.getElementById("product-cons");

    // Get the current tab's URL and fetch the product info, summary, reviews, pros, and cons
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
        const currentUrl = tabs[0].url;
        fetchProductTitle(currentUrl);
        fetchProductSummary(currentUrl);
        fetchProductReviews(currentUrl);
        fetchProductProsCons(currentUrl);
    });

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
                console.log("Product info: ", data);
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
                console.log("Summary: ", data)
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

    // Function to fetch product reviews
    function fetchProductReviews(url) {
        const productId = extractProductId(url);
        fetch(`http://localhost:8000/summarize-reviews?product_id=${productId}`)
            .then(response => response.json())
            .then(data => {
                console.log("Reviews: ", data);
                productReviewsElement.textContent = data.reviews;
            })
            .catch(error => {
                console.error(error);
            });
    }

    // Function to fetch product pros and cons
    function fetchProductProsCons(url) {
        const productId = extractProductId(url);
        fetch(`http://localhost:8000/pros-cons?product_id=${productId}`)
            .then(response => response.json())
            .then(data => {
                console.log("Pros and cons: ", data);
                if (data.pros && data.pros.length > 0) {
                    productProsElement.innerHTML = '<h3>Pros:</h3>';
                    for (const pro of data.pros) {
                        const listItem = document.createElement('li');
                        listItem.textContent = pro;
                        productProsElement.appendChild(listItem);
                    }
                } else {
                    productProsElement.textContent = 'No pros found';
                }

                if (data.cons && data.cons.length > 0) {
                    productConsElement.innerHTML = '<h3>Cons:</h3>';
                    for (const con of data.cons) {
                        const listItem = document.createElement('li');
                        listItem.textContent = con;
                        productConsElement.appendChild(listItem);
                    }
                } else {
                    productConsElement.textContent = 'No cons found';
                }
            })
            .catch(error => {
                productProsElement.textContent = 'Failed to fetch product pros';
                productConsElement.textContent = 'Failed to fetch product cons';
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

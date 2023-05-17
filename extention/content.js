chrome.runtime.sendMessage({ message: "getURL" }, function(response) {
  const urlElement = document.getElementById("url");
  if (urlElement) {
    urlElement.textContent = response.url;
  }
});

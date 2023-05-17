chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.message === "getURL") {
    const url = sender.tab.url;
    sendResponse({ url: url });
  }
});

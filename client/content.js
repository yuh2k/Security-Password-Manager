
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "checkForInputs") {
        let inputs = document.querySelectorAll('input[type="password"]');
        if (inputs.length > 0) {
            chrome.runtime.sendMessage({url: window.location.href, action: "passwordInputDetected"});
        }
    }
});


window.onload = function() {
    chrome.runtime.sendMessage({action: "checkForInputs"});
};

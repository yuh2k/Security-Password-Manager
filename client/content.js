// content.js
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "checkForInputs") {
        let inputs = document.querySelectorAll('input[type="password"]');
        if (inputs.length > 0) {
            chrome.runtime.sendMessage({url: window.location.href, action: "passwordInputDetected"});
        }
    }
});

// 当内容脚本加载时触发
window.onload = function() {
    chrome.runtime.sendMessage({action: "checkForInputs"});
};

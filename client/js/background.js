// background.js
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.passwordFieldsDetected) {
      // pop up
      chrome.browserAction.openPopup();
    }
  });
  
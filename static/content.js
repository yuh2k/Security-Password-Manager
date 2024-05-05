document.addEventListener('DOMContentLoaded', function() {
    const passwordFields = document.querySelectorAll('input[type=password]');
    if (passwordFields.length) {
      // detect password input
      chrome.runtime.sendMessage({passwordFieldsDetected: true});
    }
  });
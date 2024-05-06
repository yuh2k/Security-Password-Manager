// popup.js
document.addEventListener('DOMContentLoaded', function() {
    chrome.runtime.sendMessage({action: "checkLoginStatus"}, function(response) {
        if (response.loggedIn) {
            document.getElementById('loginDiv').style.display = 'none';
            document.getElementById('infoDiv').style.display = 'block';
        } else {
            document.getElementById('loginDiv').style.display = 'block';
            document.getElementById('infoDiv').style.display = 'none';
        }
    });
});

document.getElementById('loginButton').addEventListener('click', function() {
    chrome.runtime.sendMessage({action: "login"});
});

document.getElementById('logoutButton').addEventListener('click', function() {
    chrome.runtime.sendMessage({action: "logout"});
});

document.getElementById('checkLeak').addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        let url = tabs[0].url;
        let password = prompt("Enter the password to check for leaks:");
        chrome.runtime.sendMessage({action: "checkLeak", password: password, url: url});
    });
});

// background.js

// 背景脚本是长时间运行的，可以用来维护登录状态
let isLoggedIn = false;

const API_URL = `http://127.0.0.1:5000`;

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    switch(request.action) {
        case "login":
            performLogin();
            break;
        case "logout":
            performLogout();
            break;
        case "savePassword":
            savePassword(request.password, request.url);
            break;
        case "getPassword":
            getPassword(request.password, request.url);
            break;
        case "checkLeak":
            checkPasswordLeak(request.password);
            break;
    }
});

function performLogin() {
    chrome.identity.launchWebAuthFlow({
        url: API_URL + '/login', 
        interactive: true
    }, function(redirectUrl) {
        if (chrome.runtime.lastError) {
            console.error("Login failed: ", chrome.runtime.lastError.message);
            return;
        }
        console.log('Logged in!');
        isLoggedIn = true;
    });
}


function performLogout() {
    fetch(API_URL + '/logout', {
        method: 'POST'
    }).then(response => response.json())
      .then(data => {
        console.log('Logged out!');
        isLoggedIn = false;
    }).catch(error => console.error('Logout failed', error));
}

function savePassword(password, currentUrl) {
    if (!isLoggedIn) {
        console.error('User not logged in.');
        return;
    }
    fetch(API_URL + '/encrypt-and-save', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({password, url: currentUrl})
    }).then(response => response.json())
      .then(data => {
        chrome.runtime.sendMessage({action: "alert", message: data.message});
    }).catch(error => console.error('Save password failed', error));
}

function getPassword(password, currentUrl) {
    if (!isLoggedIn) {
        console.error('User not logged in.');
        return;
    }
    fetch(API_URL + '/get-password', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({password, url: currentUrl})
    }).then(response => {
        if (!response.ok) throw new Error('Failed to fetch password');
        return response.json();
    }).then(data => {
        chrome.runtime.sendMessage({action: "alert", message: "Encrypted Password: " + data.encryptedPassword});
    }).catch(error => console.error('Get password failed', error));
}

function checkPasswordLeak(password) {
    if (!isLoggedIn) {
        console.error('User not logged in.');
        return;
    }
    fetch(API_URL + '/check-password-leak', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({password})
    }).then(response => {
        if (!response.ok) throw new Error('Failed to check password leak');
        return response.json();
    }).then(data => {
        chrome.runtime.sendMessage({action: "alert", message: "Password has been leaked " + data.leak_count + " times"});
    }).catch(error => console.error('Check password leak failed', error));
}

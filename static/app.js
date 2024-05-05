function login() {
    window.location.href = '/login';
}


window.onload = function() {
    fetch('/check-login')
    .then(response => response.json())
    .then(data => {
        if (data.loggedIn) {
            document.getElementById('content').style.display = 'block'; 
            document.getElementById('loginButton').style.display = 'none'; 
        } else {
            document.getElementById('content').style.display = 'none';
            document.getElementById('loginButton').style.display = 'block';
        }
    });
};


function logout() {
    fetch('/logout')
    .then(() => {
        document.getElementById('content').style.display = 'none';
        document.getElementById('loginButton').style.display = 'block';
    });
}

document.getElementById('savePasswordForm').onsubmit = async function(event) {
    event.preventDefault();
    const password = document.getElementById('password').value;
    const url = document.getElementById('url').value;

    const response = await fetch('/encrypt-and-save', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({password, url})  
    });
    const data = await response.json();
    alert(data.message);
};


document.getElementById('getPasswordForm').onsubmit = async function(event) {
    event.preventDefault();
    const password = document.getElementById('get_password').value;
    const url = document.getElementById('get_url').value;

    const response = await fetch('/get-password', {
        method: 'POST',  // 注意这里改为POST，与后端保持一致
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({password, url})
    });
    const data = await response.json();
    if (response.ok) {
        alert("Encrypted Password: " + data.encryptedPassword);
    } else {
        alert("Error: " + data.message);
    }
};


document.getElementById('checkPasswordLeakForm').onsubmit = async function(event) {
    event.preventDefault();
    const password = document.getElementById('leak_password').value;

    const response = await fetch('/check-password-leak', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({password})
    });
    const data = await response.json();
    if (response.ok) {
        alert("Password has been leaked " + data.leak_count + " times");
    } else {
        alert("Error: " + data.message);
    }
};



function login() {
    window.location.href = '/login';
}


window.onload = function() {
    fetch('/check-login')
    .then(response => response.json())
    .then(data => {
        if (data.loggedIn) {
            document.getElementById('content').style.display = 'block'; // 显示内容
            document.getElementById('loginButton').style.display = 'none'; // 隐藏登录按钮
        } else {
            document.getElementById('content').style.display = 'none'; // 隐藏内容
            document.getElementById('loginButton').style.display = 'block'; // 显示登录按钮
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
        method: 'GET',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({password, url})  
    });
    const data = await response.json();
    alert(data.message);
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
    alert(data.message);
};

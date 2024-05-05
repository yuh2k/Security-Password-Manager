function login() {
    console.log("Redirecting to login...");
    window.location.href = '/login';

}

document.getElementById('savePasswordForm').onsubmit = async function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const url = document.getElementById('url').value;

    const response = await fetch('/encrypt-and-save', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email, password, url})
    });
    const data = await response.json();
    alert(data.message);
};

document.getElementById('getPasswordForm').onsubmit = async function(event) {
    event.preventDefault();
    const email = document.getElementById('get_email').value;
    const password = document.getElementById('get_password').value;
    const url = document.getElementById('get_url').value;
    const queryParams = new URLSearchParams({email, password, url}).toString();
    const fetchUrl = `/get-password?${queryParams}`;
    const response = await fetch(fetchUrl, {
        method: 'GET'
    });
    const data = await response.json();
    document.getElementById('getPasswordResult').textContent = data.message;
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
    document.getElementById('checkPasswordLeakResult').textContent = data.message;
    alert(data.message);
};

document.addEventListener('DOMContentLoaded', function() {
    var loginButton = document.getElementById('loginBtn');
    loginButton.addEventListener('click', function() {
        // Google OAuth 
        console.log('Login with Google');
    });

    var generateButton = document.getElementById('generatePasswordBtn');
    generateButton.addEventListener('click', function() {
        var username = "user@example.com"; // !!!
        var password = "12345"; // !!!
        var url = "https://example.com"; // !!!

        fetch('http://localhost:5000/encrypt-and-save', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password, url})
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            document.getElementById('generatedPassword').value = data.encryptedPassword;
        })
        .catch(error => console.error('Error:', error));
    });
});

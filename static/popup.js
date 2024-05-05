document.getElementById('googleLogin').addEventListener('click', function() {
    chrome.identity.getAuthToken({interactive: true}, function(token) {
      console.log('Google token:', token);
      // 你可以在这里添加调用LOGIN API的代码，可能需要将token传送到你的服务器以验证身份
    });
  });
  
  document.getElementById('generate').addEventListener('click', function() {
    const domain = document.getElementById('domain').value;
    getPasswordFromServer(domain); // 从服务器获取密码
  });
  
  function getPasswordFromServer(domain) {
    // 使用fetch API发起GET请求
    fetch(`https://your-backend.com/get-password?domain=${encodeURIComponent(domain)}`, {
      method: 'GET',
      headers: {
        // 可能需要认证头或其他安全措施
        'Authorization': 'Bearer your-auth-token',
        'Content-Type': 'application/json'
      }
    }).then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Network response was not ok.');
      }
    }).then(data => {
      document.getElementById('password').textContent = data.password; // 假设密码字段为password
      checkPasswordLeak(data.password); // 调用泄露检测API
    }).catch(error => {
      console.error('There was a problem with the fetch operation:', error);
      document.getElementById('password').textContent = 'Failed to fetch password';
    });
  }
  
  function checkPasswordLeak(password) {
    // 假设你的后端有一个检测密码泄露的API
    fetch(`https://your-backend.com/leak-detect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer your-auth-token'
      },
      body: JSON.stringify({password: password})
    }).then(response => response.json())
      .then(data => {
        if (data.isLeaked) {
          alert("Warning: This password has been leaked before!");
        }
      }).catch(error => {
        console.error("Leak detection failed:", error);
      });
  }
  
  document.getElementById('save').addEventListener('click', function() {
    const password = document.getElementById('password').textContent;
    savePassword(password); // 调用加密并保存密码的API
  });
  
  function savePassword(password) {
    // 发送密码到后端进行加密保存
    fetch(`https://your-backend.com/encrypt-and-save`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer your-auth-token'
      },
      body: JSON.stringify({password: password})
    }).then(response => {
      if (response.ok) {
        alert("Password saved successfully!");
      } else {
        alert("Failed to save password.");
      }
    }).catch(error => {
      console.error("Error saving password:", error);
    });
  }
  
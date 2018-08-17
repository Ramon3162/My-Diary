const registerUser = () => {
    fetch('http://127.0.0.1:5000/auth/signup', {
      method: 'POST',
      body: JSON.stringify({
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        confirm_password: document.getElementById('confirm_password').value
      }),
      headers: {
        'Content-type': 'application/json;'
      }
      })
      .then(response => response.json())
      .then(registerData => {
        if(registerData.message === "User created successfully"){
          window.location.href = "./login.html";
        }else{
            document.getElementById('error-message').innerHTML = registerData.message;
        }
      })
  }
  
const loginUser = () => {
    fetch('http://127.0.0.1:5000/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
      }),
      headers: {
        'Content-type' : 'application/json;'
      }
    })
    .then(response => response.json())
    .then(loginData => {
        if(loginData.message === "Login successfull"){
            window.location.href = "./profile.html";
            sessionStorage.setItem("token",loginData.token);
        }else{
            document.getElementById('error-message').innerHTML = loginData.message;
        }
    })
  }
 
  const publishEntry = () => {
    fetch('http://127.0.0.1:5000/api/v1/entries', {
      method: 'POST',
      body: JSON.stringify({
        title: document.getElementById('title').value,
        description: document.getElementById('description').value
      }),
      headers: {
        'Authorization' : `Bearer ${sessionStorage.getItem("token")}`,
        'Content-type' : 'application/json;'
      }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message)
    })
  }

  const getEntries = () => {
    fetch('http://127.0.0.1:5000/api/v1/entries', {
      headers: {
        'Authorization' : `Bearer ${sessionStorage.getItem("token")}`,
        'Content-type' : 'application/json;'
      }
    })
    .then(response => response.json())
    .then(entriesData => {
      if(entriesData.message === "All entries found successfully"){
        window.location.href = "./entry_list.html";
      }else{
          document.getElementById('error-message').innerHTML = entriesData.message;
      }
    })
  }
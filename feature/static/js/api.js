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
      .then(data => {
        if(data.message === "User created successfully"){
            document.getElementById('error-message').innerHTML = "Your account has been created successfully.";
        }else{
            document.getElementById('error-message').innerHTML = data.message;
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
    .then(data => {
        if(data.message === "Login successfull"){
            window.location.href = "./profile.html";
        }else{
            document.getElementById('error-message').innerHTML = data.message;
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
        Authorization: `Bearer `,
        'Content-type' : 'application/json;'
      }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message)
    })
  }
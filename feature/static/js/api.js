let signupUrl = 'http://127.0.0.1:5000/auth/signup';
let loginUrl = 'http://127.0.0.1:5000/auth/login';
let entriesUrl = 'http://127.0.0.1:5000/api/v1/entries';


const registerUser = () => {
    fetch(signupUrl, {
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
    fetch(loginUrl, {
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
    fetch(entriesUrl, {
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
      if(data.message === "Entry created successfully"){
        window.location.href = "./entry.html";
        console.log(data.message);
        sessionStorage.setItem("title",data.Entry.title);
        sessionStorage.setItem("description",data.Entry.description);
        sessionStorage.setItem("date",data.Entry.date_posted);
      }else{
        document.getElementById('message').innerHTML = data.message;
      }
    })
  }

  const getSingleEntry = () => {
    let entry_id = event.srcElement.id;
    console.log(entry_id);
    fetch( `http://127.0.0.1:5000/api/v1/entries/${entry_id}`, {
      headers: {
        'Authorization' : `Bearer ${sessionStorage.getItem("token")}`,
        'Content-type' : 'applicatin/json;'
      }
    })
    .then(response => response.json())
    .then(entryData => {
      if(entryData.message === "Entry retrieved successfully"){
        window.location.href = "./entry.html";
        console.log(entryData.message);
        sessionStorage.removeItem("title");
        sessionStorage.removeItem("description");
        sessionStorage.removeItem("date");
        sessionStorage.setItem("title",entryData.Entry.title);
        sessionStorage.setItem("description",entryData.Entry.description);
        sessionStorage.setItem("date",entryData.Entry.date_posted);
      }else{
        document.getElementById('message').innerHTML = entryData.message;
      }
    })
  }

  const editEntry = () => {
    let entry_id = event.srcElement.id;
    console.log(entry_id);
    fetch( `http://127.0.0.1:5000/api/v1/entries/${entry_id}`, {
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
      if(data.message === "Entry created successfully"){
        window.location.href = "./entry.html";
        console.log(data.message);
        sessionStorage.setItem("title",data.Entry.title);
        sessionStorage.setItem("description",data.Entry.description);
        sessionStorage.setItem("date",data.Entry.date_posted);
      }else{
        document.getElementById('message').innerHTML = data.message;
      }
    })
  }

  const showSingleEntry = () => {
    document.getElementById('title-section').innerHTML += 
      `<h2>${sessionStorage.getItem("title")}</h2>
      <p>${sessionStorage.getItem("date")}</p>`;
    document.getElementById('diary-content').innerHTML += `<p>${sessionStorage.getItem("description")}</p>`;
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
        let i;
        for(i = 0; i < entriesData.Entries.length; i++){
          console.log(entriesData.Entries.length);
          sessionStorage.setItem('entry_id', entriesData.Entries[i].id);
          document.getElementById('entry-data').innerHTML += `
          <tr>
            <td></td>
            <td><a href="javascript:void(0);" onclick="getSingleEntry()" id="${entriesData.Entries[i].id}">${entriesData.Entries[i].title}</a></td>
            <td>${entriesData.Entries[i].date_posted}</td>
            <td><a href="edit_entry.html" id="edit-icons">
                <i class="fa fa-pencil" id="${entriesData.Entries[i].id}"></i></a>
            </td>
            <td><a href="javascript:void(0);" id="edit-icons">
                <i class="fa fa-trash" onclick="confirmDelete()" id="${entriesData.Entries[i].id}"></i></a>
            </td>
          </tr>`
        }
        console.log(entriesData.message);
      }else{
        document.getElementById('message').innerHTML = entriesData.message;
      }
    })
  }

  // const getEntryId = () => {
  //   console.log(event.srcElement.id);
  // }
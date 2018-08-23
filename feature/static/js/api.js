let signupUrl = 'http://127.0.0.1:5000/auth/signup';
let loginUrl = 'http://127.0.0.1:5000/auth/login';
let entriesUrl = 'http://127.0.0.1:5000/api/v1/entries';

const setEntrySession = (id, title, desc, date) => {
  sessionStorage.setItem("id", id);
  sessionStorage.setItem("title", title);
  sessionStorage.setItem("description", desc);
  sessionStorage.setItem("date", date);
}

const destroyEntrySession = () => {
  sessionStorage.removeItem("id")
  sessionStorage.removeItem("title");
  sessionStorage.removeItem("description");
  sessionStorage.removeItem("date");
}

// const registerUser = () => {
//     fetch(signupUrl, {
//       method: 'POST',
//       body: JSON.stringify({
//         username: document.getElementById('username').value,
//         email: document.getElementById('email').value,
//         password: document.getElementById('password').value,
//         confirm_password: document.getElementById('confirm_password').value
//       }),
//       headers: {
//         'Content-type': 'application/json;'
//       }
//       })
//       .then(response => response.json())
//       .then(registerData => {
//         if(registerData.message === "User created successfully"){
//           window.location.href = "./login.html";
//         }else{
//             document.getElementById('error-message').innerHTML = registerData.message;
//         }
//       })
//   }
  
// const loginUser = () => {
//   fetch(loginUrl, {
//     method: 'POST',
//     body: JSON.stringify({
//       username: document.getElementById('username').value,
//       password: document.getElementById('password').value
//     }),
//     headers: {
//       'Content-type' : 'application/json;'
//     }
//   })
//   .then(response => response.json())
//   .then(loginData => {
//       if(loginData.message === "Login successfull"){
//           window.location.href = "./profile.html";
//           sessionStorage.setItem("token",loginData.token);
//       }else{
//           document.getElementById('error-message').innerHTML = loginData.message;
//       }
//   })
// }

// const getEntries = () => {
//   fetch(entriesUrl, {
//     headers: {
//       'Authorization' : `Bearer ${sessionStorage.getItem("token")}`,
//       'Content-type' : 'application/json;'
//     }
//   })
//   .then(response => response.json())
//   .then(entriesData => {
//     if(entriesData.message === "All entries found successfully"){
//       let i;
//       for(i = 0; i < entriesData.Entries.length; i++){
//         console.log(entriesData.Entries.length);
//         sessionStorage.setItem((i+1), entriesData.Entries[i].id);
//         document.getElementById('entry-data').innerHTML += `
//         <tr>
//           <td></td>
//           <td><a href="javascript:void(0);" onclick="getSingleTableEntry(this)">
//             ${entriesData.Entries[i].title}</a>
//           </td>
//           <td>${entriesData.Entries[i].date_posted}</td>
//           <td><a href="javascript:void(0);" id="edit-icons" onclick="editTableEntry(this)">
//               <i class="fa fa-pencil"></i></a>
//           </td>
//           <td><a href="javascript:void(0);" id="edit-icons" onclick="deleteTableEntry(this)">
//               <i class="fa fa-trash""></i></a>
//           </td>
//         </tr>`
//       }
//       console.log(entriesData.message);
//     }else{
//       let table = document.getElementById('entry-data');
//       table.style.display = "none";
//       document.getElementById('message').innerHTML = entriesData.message;
//     }
//   })
// }
 
// const publishEntry = () => {
//   fetch(entriesUrl, {
//     method: 'POST',
//     body: JSON.stringify({
//       title: document.getElementById('title').value,
//       description: document.getElementById('description').value
//     }),
//     headers: {
//       'Authorization' : `Bearer ${sessionStorage.getItem("token")}`,
//       'Content-type' : 'application/json;'
//     }
//   })
//   .then(response => response.json())
//   .then(data => {
//     if(data.message === "Entry created successfully"){
//       window.location.href = "./entry.html";
//       console.log(data.message);
//       let id = data.Entry.id;
//       let title = data.Entry.title;
//       let desc = data.Entry.description;
//       let date = data.Entry.date_posted;
//       destroyEntrySession();
//       setEntrySession(id, title, desc, date);
//     }else{
//       document.getElementById('message').innerHTML = data.message;
//     }
//   })
// }

const deleteEntry = (entryId) => {
  let confirmation = confirm("Are you sure you want to delete this entry?");
  if(confirmation == true){
    fetch( `http://127.0.0.1:5000/api/v1/entries/${entryId}`, {
      method: 'DELETE',
      headers: {
        'Authorization' : `Bearer ${sessionStorage.getItem("token")}`,
        'Content-type' : 'application/json;'
      }
      })
      .then(response => response.json())
      .then(data => {
        if(data.message === "Entry deleted successfully"){
          document.location.replace("./entry_list.html");
          console.log(data.message);
        }else{
          document.getElementById('message').innerHTML = data.message;
        }
    })
  }
}


const deleteTableEntry = (tableRow) => {
  let index = tableRow.parentNode.parentNode.rowIndex;
  let entryId = sessionStorage.getItem(index);
  console.log(entryId);
  deleteEntry(entryId);
}

const deleteViewEntry = () => {
  let entryId = sessionStorage.getItem("id");
  console.log(entryId);
  deleteEntry(entryId);
}

// const getEntry = (entryId) => {
//   fetch( `http://127.0.0.1:5000/api/v1/entries/${entryId}`, {
//     headers: {
//      'Authorization' : `Bearer ${sessionStorage.getItem("token")}`,
//      'Content-type' : 'applicatin/json;'
//     }
//   })
//   .then(response => response.json())
//   .then(entryData => {
//   if(entryData.message === "Entry retrieved successfully"){    
//     console.log(entryData.message);
//     window.location.replace("./entry.html");
//     let id = entryData.Entry.id;
//     let title = entryData.Entry.title;
//     let desc = entryData.Entry.description;
//     let date = entryData.Entry.date_posted;
//     destroyEntrySession();
//     setEntrySession(id, title, desc, date);
//   }else{
//     document.getElementById('message').innerHTML = entryData.message;
//   }
//   })
// }

// const getSingleTableEntry = (tableRow) => {
//   let index = tableRow.parentNode.parentNode.rowIndex;
//   let entryId = sessionStorage.getItem(index);
//   console.log(entryId);
//   getEntry(entryId); 
// }

// const showSingleEntry = () => {
//   document.getElementById('title-section').innerHTML += 
//     `<h2>${sessionStorage.getItem("title")}</h2>
//     <p>${sessionStorage.getItem("date")}</p>`;
//   document.getElementById('diary-content').innerHTML +=
//   `<p>${sessionStorage.getItem("description")}</p>`;
// }

// const editEntry = () => {
//   let entryId = sessionStorage.getItem("id");
//   fetch( `http://127.0.0.1:5000/api/v1/entries/${entryId}`, {
//     method: 'PUT',
//     body: JSON.stringify({
//       title: document.getElementById('title').value,
//       description: document.getElementById('entry').value
//     }),
//     headers: {
//       'Authorization' : `Bearer ${sessionStorage.getItem("token")}`,
//       'Content-type' : 'application/json;'
//     }
//   })
//   .then(response => response.json())
//   .then(entryData => {
//     if(entryData.message === "Entry updated successfully"){
//       console.log(entryData.message);
//       window.location.href = "./entry.html";
//       let id = entryData.Entry.id;
//       let title = entryData.Entry.title;
//       let desc = entryData.Entry.description;
//       let date = entryData.Entry.date_posted;
//       destroyEntrySession();
//       setEntrySession(id, title, desc, date);
//     }else{
//       document.getElementById('message').innerHTML = entryData.message;
//     }
//   })
// }

// const editTableEntry = (tableRow) => {
//   let index = tableRow.parentNode.parentNode.rowIndex;
//   let entryId = sessionStorage.getItem(index);   
//   console.log(entryId);
//   // getEntry(entryId);
// }

// const entryData = () => {
//   document.getElementById("title").value = sessionStorage.getItem("title");
//   document.getElementById("entry").value = sessionStorage.getItem("description");
// }
    
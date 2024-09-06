document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  //send the mail
  document.querySelector('#compose-form').onsubmit = function(event) {
    event.preventDefault(); // Prevent the default form submission

    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body: document.querySelector('#compose-body').value
        }),
        headers: {
          'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        //Check for errors
        if (result.error) {
          alert(result.error);
        } else {
          console.log(result.message);
          // Load the user sent mailbox only if it was send
          load_mailbox('sent');
        }
    })
  };
}


function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // //show the mails from the mailbox
  // fetch(`/emails/${mailbox}`)
  // .then(response => response.json())
  // .then(emails => {
  // // Print emails in console
  // console.log(emails);
  // //Show the emails
  // emails.forEach(email =>{
  //   const emailDiv = document.createElement('div'); //creat the element div
  //   //Color of the email
  //   emailDiv.style.backgroundColor = 'white'; //Unread
  //   if (email.read) {
  //     emailDiv.style.backgroundColor = 'gray'; //Read
  //   }
  //   //Complete with information
  //   emailDiv.innerHTML = `
  //   <strong>From:</strong> ${email.sender}
  //   <strong>Subject:</strong> ${email.subject}
  //   <strong>Body:</strong> ${email.body}
  //   `
  //   })
  // });
  // .catch(error => {
  //   alert(error);
  // })
}



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
  document.querySelector('#selected-email').style.display = 'none';
  

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Send the mail
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
        // Check for errors
        if (result.error) {
          alert(result.error);
          compose_email();
        } else {
          // Load the user sent mailbox only if it was sent
          load_mailbox('sent');
        }
    })
    .catch(error => {
      console.log('Error:', error); // any error charging the page
    });
  };
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#selected-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show the mails from the mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Clear previous emails
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    
    // Show the emails
    emails.forEach(email => {
      const emailDiv = document.createElement('div'); // Create the element div
      emailDiv.className = 'email-item';  // Add class for styling

      // Set background color based on read status
      emailDiv.style.backgroundColor = email.read ? 'gray' : 'white';

      // Complete with information
      emailDiv.innerHTML = `
        <strong>From:</strong> ${email.sender} <br>
        <strong>Subject:</strong> ${email.subject} <br>
        <small><strong>Timestamp:</strong> ${email.timestamp}</small>
      `;

      // Add padding and border-radius to match CSS styles
      emailDiv.classList.add('p-3', 'mb-2', 'border', 'rounded');

      // Event listener to view a specific email
      emailDiv.addEventListener('click', () => {
        view_email(email.id); // Allows to see the email
      });

      // Add to the view
      document.querySelector('#emails-view').appendChild(emailDiv);

      // Add archive/unarchive button if needed
      if (mailbox === 'archive' || mailbox === 'inbox') {
        button_function(mailbox, email.id);
      }
    });
  })
  .catch(error => {
    console.log('Error:', error); // Any error in charging the page
  });
}

function view_email(id) {
  // Show the email
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#selected-email').style.display = 'block';

  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      // The content
      document.querySelector('#selected-email').innerHTML = `
        <p><strong>Sender:</strong> ${email.sender}</p>
        <p><strong>Recipients:</strong> ${email.recipients}</p>
        <p><strong>Subject:</strong> ${email.subject}</p>
        <p><strong>Body:</strong> ${email.body}</p>
        <p><small>Timestamp: ${email.timestamp}</small></p>
        <button id="reply-button" class="btn btn-sm btn-outline-primary">Reply</button>
      `;

      // Reply button
      document.querySelector('#reply-button').addEventListener('click', () => {
        compose_email();

        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-subject').value = email.subject.startsWith("Re:") ? email.subject : `Re: ${email.subject}`;
        document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote:\n${email.body}\n\n`;
      });

      // Mark as read
      return fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      });
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function button_function(mailbox, id) {
  const archive_button = document.createElement('button'); // Create the element button for archive mails
  archive_button.classList.add('btn', 'btn-sm', 'btn-outline-primary', 'mt-2');  // Add Bootstrap classes

  archive_button.innerHTML = mailbox === 'archive' ? 'Unarchive' : 'Archive'; // Select the HTML

  archive_button.addEventListener('click', () => {
    const is_archive = archive_button.innerHTML === 'Archive'; // Boolean value: true = Archive, false = Unarchive

    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: is_archive
      })
    })
    .then(() => {
      // Reload inbox after using the button
      load_mailbox('inbox');
    })
    .catch(error => {
      console.log('Error:', error); // General errors
    });
  });

  // Add to the view with margin-top for spacing
  document.querySelector('#emails-view').appendChild(archive_button);
}

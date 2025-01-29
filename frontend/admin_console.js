const editUserModal = new bootstrap.Modal(document.getElementById('editUserModal'));

// Check if the user is logged in (check for token in localStorage)
function checkLoginStatus() {
  const token = localStorage.getItem('auth_token');  // Change this key based on how you store the token
  if (!token) {
    window.location.href = 'login.html';  // Redirect to login page
  }
}

// Fetch users from the backend
function fetchUsers() {
  fetch('http://127.0.0.1:5000/api/users', {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('auth_token')}`  // Include token in the request header
    }
  })
    .then(response => response.json())
    .then(data => {
      const users = Array.isArray(data) ? data : [];  // Directly use data if it's an array
      console.log(users); // Log the users array

      userList.innerHTML = '';  // Clear the existing list

      if (users.length === 0) {
        userList.innerHTML = '<tr><td colspan="9" class="text-center">No users found</td></tr>';
      } else {
        users.forEach(user => {
          const userRow = document.createElement('tr');
          
          // Set the "active" field's text color to green if true, red if false
          const activeClass = user.active ? 'text-success' : 'text-danger';
          const activeText = user.active ? 'Active' : 'Inactive';
          
          userRow.innerHTML = `
            <td>${user.name}</td>
            <td>${user.city}</td>
            <td>${user.age}</td>
            <td>${user.phone_number}</td>
            <td>${user.birth_date || 'N/A'}</td>
            <td class="${activeClass}">${activeText}</td>
            <td>${user.created_at}</td>
            <td>${user.updated_at || 'N/A'}</td>
            <td>
              <button class="btn btn-info btn-sm" onclick="openEditModal(${user.id})">Edit</button>
              <button class="btn btn-warning btn-sm" onclick="toggleActivation(${user.id}, ${user.active})">${user.active ? 'Deactivate' : 'Activate'}</button>
              <button class="btn btn-danger btn-sm" onclick="deleteUser(${user.id}, true)">Delete Permanently</button>
            </td>
          `;
          userList.appendChild(userRow);
        });
      }
    })
    .catch(error => console.error('Error fetching users:', error));
}

// Create a new user
createUserForm.addEventListener('submit', function(event) {
  event.preventDefault();

  const newUser = {
    name: document.getElementById('createName').value,
    city: document.getElementById('createCity').value,
    age: document.getElementById('createAge').value,
    phone_number: document.getElementById('createPhone').value,
    birth_date: document.getElementById('createBirthDate').value
  };

  fetch('http://127.0.0.1:5000/api/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('auth_token')}`  // Add token to request
    },
    body: JSON.stringify(newUser)
  })
  .then(response => response.json())
  .then(() => {
    fetchUsers();
    createUserForm.reset();
  })
  .catch(error => console.error('Error creating user:', error));
});

// Open the edit modal
function openEditModal(userId) {
  fetch(`http://127.0.0.1:5000/api/users/${userId}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('auth_token')}`  // Add token to request
    }
  })
  .then(response => response.json())
  .then(user => {
    // Set user fields in the modal
    document.getElementById('editName').value = user.name;
    document.getElementById('editCity').value = user.city;
    document.getElementById('editAge').value = user.age;
    document.getElementById('editPhone').value = user.phone_number;

    // Format birth_date to match the input date format (YYYY-MM-DD)
    const birthDate = user.birth_date ? new Date(user.birth_date) : null;
    if (birthDate) {
      // Ensure the birth_date is in the correct format: YYYY-MM-DD
      const formattedDate = birthDate.toISOString().split('T')[0];
      document.getElementById('editBirthDate').value = formattedDate;
    } else {
      // If no birth_date, set to empty
      document.getElementById('editBirthDate').value = '';
    }

    document.getElementById('editUserId').value = user.id;

    // Show the modal (Bootstrap 5)
    editUserModal.show();  // This should work now
  })
  .catch(error => console.error('Error fetching user:', error));
}

// Update an existing user
editUserForm.addEventListener('submit', function(event) {
  event.preventDefault();

  const updatedUser = {
    id: document.getElementById('editUserId').value,
    name: document.getElementById('editName').value,
    city: document.getElementById('editCity').value,
    age: document.getElementById('editAge').value,
    phone_number: document.getElementById('editPhone').value,
    birth_date: document.getElementById('editBirthDate').value || null  // Set null if no birth date entered
  };

  fetch(`http://127.0.0.1:5000/api/users/${updatedUser.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('auth_token')}`  // Add token to request
    },
    body: JSON.stringify(updatedUser)
  })
  .then(response => response.json())
  .then(() => {
    fetchUsers();
    editUserModal.hide();
  })
  .catch(error => console.error('Error updating user:', error));
});

// Delete a user
function deleteUser(userId, isHardDelete = false) {
  const deleteUrl = isHardDelete 
    ? `http://127.0.0.1:5000/api/users/${userId}/hard_delete`  // Hard delete endpoint
    : `http://127.0.0.1:5000/api/users/${userId}/soft_delete`; // Soft delete endpoint

  if (confirm(`Are you sure you want to ${isHardDelete ? "permanently delete" : "deactivate"} this user?`)) {
    fetch(deleteUrl, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`  // Add token to request
      }
    })
    .then(response => response.json())
    .then(() => {
      fetchUsers();  // Reload the user list after deletion
    })
    .catch(error => console.error('Error deleting user:', error));
  }
}

// Toggle activation/deactivation of a user
function toggleActivation(userId, isActive) {
  const action = 'toggle_active';  // Action is "toggle_active" instead of activate/deactivate
  const url = `http://127.0.0.1:5000/api/users/${userId}/${action}`;

  fetch(url, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('auth_token')}`  // Add token to request
    }
  })
  .then(response => response.json())
  .then(() => {
    fetchUsers();  // Reload the user list after the change
  })
  .catch(error => console.error('Error toggling user activation:', error));
}

// Initial check for login status
checkLoginStatus();

// Initial fetch of users when page loads
fetchUsers();

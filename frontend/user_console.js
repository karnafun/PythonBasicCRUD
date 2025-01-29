// Ensure user is authenticated and fetch their data
document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('auth_token');
    if (!token) {
        window.location.href = 'login.html'; // Redirect to login if no token is found
    } else {
        fetchUserData();
    }
});

function fetchUserData() {
    const token = localStorage.getItem('auth_token');
    fetch('http://127.0.0.1:5000/api/users/me', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(user => {
        if (user) {
            // Populate user data in the view
            document.getElementById('userName').textContent = user.name;
            document.getElementById('userCity').textContent = user.city;
            document.getElementById('userAge').textContent = user.age;
            document.getElementById('userPhone').textContent = user.phone_number;
            document.getElementById('userBirthDate').textContent = user.birth_date || 'N/A';
            
            // Fill in the edit form with current values
            document.getElementById('editName').value = user.name;
            document.getElementById('editCity').value = user.city;
            document.getElementById('editAge').value = user.age;
            document.getElementById('editPhone').value = user.phone_number;
            document.getElementById('editBirthDate').value = formatDate(user.birth_date) || '';
        } else {
            alert('User data could not be retrieved.');
        }
    })
    .catch(error => console.error('Error fetching user data:', error));
}
function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Months are 0-based
    const day = date.getDate().toString().padStart(2, '0');
    
    return `${year}-${month}-${day}`;
}
// Handle form submission to update user data
document.getElementById('editUserForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const updatedUser = {
        name: document.getElementById('editName').value,
        city: document.getElementById('editCity').value,
        age: document.getElementById('editAge').value,
        phone_number: document.getElementById('editPhone').value,
        birth_date: document.getElementById('editBirthDate').value || null
    };

    const token = localStorage.getItem('auth_token');
    fetch('http://127.0.0.1:5000/api/users/me', {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedUser)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('User information updated successfully.');
            fetchUserData(); // Reload the updated user data
        } else {
            alert('Failed to update user information.');
        }
    })
    .catch(error => console.error('Error updating user data:', error));
});

document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const loginFormContainer = document.getElementById("loginFormContainer");
    const registerFormContainer = document.getElementById("registerFormContainer");

    // Toggle between login and register forms
    const showRegisterForm = document.getElementById("showRegisterForm");
    const showLoginForm = document.getElementById("showLoginForm");

    showRegisterForm.addEventListener("click", function() {
        loginFormContainer.style.display = "none";
        registerFormContainer.style.display = "block";
    });

    showLoginForm.addEventListener("click", function() {
        loginFormContainer.style.display = "block";
        registerFormContainer.style.display = "none";
    });

    // Handle Login Form Submission
    loginForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const data = {
            username: username,
            password: password
        };

        fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                localStorage.setItem('auth_token', data.token);
                if (data.user.role === 'admin') {
                    window.location.href = "admin_console.html";
                } else {
                    window.location.href = "user_console.html";
                }
            } else {
                showErrorMessage("Invalid credentials. Please try again.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showErrorMessage("An error occurred while authenticating. Please try again later.");
        });
    });

    // Handle Register Form Submission
    registerForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const newUsername = document.getElementById("newUsername").value;
        const newPassword = document.getElementById("newPassword").value;
        const verifyPassword = document.getElementById("verifyPassword").value;

        if (newPassword !== verifyPassword) {
            showErrorMessage("Passwords do not match!");
            return;
        }

        const data = {
            username: newUsername,
            password: newPassword
        };

        fetch('http://127.0.0.1:5000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                showSuccessMessage("Account created successfully! Please log in.");
                loginFormContainer.style.display = "block";
                registerFormContainer.style.display = "none";
            } else {
                showErrorMessage(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showErrorMessage("An error occurred while registering. Please try again later.");
        });
    });

    // Function to display error messages
    function showErrorMessage(message) {
        const errorMessage = document.createElement("div");
        errorMessage.classList.add("error-message");
        errorMessage.innerText = message;

        document.body.appendChild(errorMessage);
        setTimeout(() => {
            errorMessage.remove();
        }, 5000);
    }

    // Function to display success messages
    function showSuccessMessage(message) {
        const successMessage = document.createElement("div");
        successMessage.classList.add("success-message");
        successMessage.innerText = message;

        document.body.appendChild(successMessage);
        setTimeout(() => {
            successMessage.remove();
        }, 5000);
    }
});

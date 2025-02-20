const state = {
    users: [],
    currentView: 'dashboard',  // Starts with dashboard as default
    loading: false,
    error: null
};

let userVal = {
    name: 'a',
    email: 'a',
    password: 'a'

};

function switchPanel(viewerId) {
    // Remove active class from all views and links
    document.querySelectorAll('.part').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.sidebar-menu a').forEach(s => s.classList.remove('active'));

    // Add active class to current view and link
    document.getElementById(viewerId).classList.add('active');
    document.querySelector(`.sidebar-menu a[href="#${viewerId}"]`)?.classList.add('active');

    state.currentView = viewerId;

    // Load view-specific data
    
}

document.querySelector('.sidebar').addEventListener('click', (e) => {
    if (e.target.tagName === 'A' && e.target.getAttribute('href')?.startsWith('#')) {
        e.preventDefault();
        const viewerId = e.target.getAttribute('href').slice(1);
        if (viewerId !== 'logoutBtn') {
            switchPanel(viewerId);
        }
    }
});

//Create user

let createbt = document.getElementById('createbt');
let openPanel = document.getElementById('back-panel');
let closePanel = document.getElementById('closePanel');

function popUpPanel() {
    openPanel.classList.add('show');
}

function closePopUpPanel() {
    openPanel.classList.remove('show');
}

createbt.addEventListener('click', popUpPanel);
closePanel.addEventListener('click', closePopUpPanel);


function userLoad() {
    fetch("http://localhost:8000/api/get_userLoad/")
    .then(response => response.json())
    .then(data => {
        tbody = document.getElementById('userTableBody');
        tbody.innerHTML = '';
        data.users.forEach(user => {
            tbody.innerHTML += `
            <tr>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td>${user.status}</td>
                <td>${user.role.role_name}</td>
                <td>${user.status}</td>
                <td><button onclick="openEditPanel('${user.id}')">Edit</button></td>
                <td><button onclick="deleteUser(${user.id})" class="delete-btn">Delete</button></td>
            </tr>`;
        })
    })
    .catch(error => {
        console.error('Error loading users:', error);
    });
}

function openEditPanel(userId) {
    fetch(`/api/users/${userId}/`)
        .then(response => response.json())
        .then(user => {
            // Set current info
            document.getElementById('currentName').textContent = user.name;
            document.getElementById('currentEmail').textContent = user.email;
            document.getElementById('currentStatus').textContent = user.status;
            document.getElementById('currentRole').textContent = user.role.role_name;
            document.getElementById('newStatus').innerHTML = `
            <option value="active" ${user.status === 'active' ? 'selected' : ''}>Active</option>
            <option value="inactive" ${user.status === 'inactive' ? 'selected' : ''}>Inactive</option>
            <option value="banned" ${user.status === 'banned' ? 'selected' : ''}>Ban</option>`;
            document.getElementById('newRole').innerHTML = `
            <option value="1" ${user.role.role_name === 'admin' ? 'selected' : ''}>Admin</option>
            <option value="2" ${user.role.role_name === 'basicuser' ? 'selected' : ''}>User</option>`;

            // Set hidden user ID
            document.getElementById('userId').value = userId;

            // Show the panel
            document.getElementById('editPanel').style.display = 'block';

        });
}

function closeEditPanel() {
    document.getElementById('editPanel').style.display = 'none';
    document.getElementById('editForm').reset();
}

function handleEdit(event) {
    event.preventDefault();
    const userId = document.getElementById('userId').value;
    
    const newData = {
        name: document.getElementById('newName').value || document.getElementById('currentName').textContent,
        email: document.getElementById('newEmail').value || document.getElementById('currentEmail').textContent,
        status: document.getElementById('newStatus').value || document.getElementById('currentStatus').textContent,
        role_id: document.getElementById('newRole').value || document.getElementById('currentRole').textContent
    };

    fetch(`/api/users/${userId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(newData)
    })
    .then(response => response.json())
    .then(data => {
        closeEditPanel();
        userLoad();  // Reload the table
    })
    .catch(error => {
        console.error('Error updating user:', error);
    });
}

function deleteUser(userId) {
    if(confirm('Are you sure you want to delete this user?')) {
        fetch(`/api/users/${userId}/`, {
            method: 'DELETE',
            headers: {
                
            }
        })
        .then(response => {
            
            userLoad();  // Reload the table
            
        })
        .catch(error => console.error('Error:', error));
    }
}

function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000)); // Expiration time
    const expires = "expires=" + d.toUTCString();
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

// Function to get cookies
function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i].trim();
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// Function to delete cookies
function deleteCookie(name) {
    document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

// Toggle function for Microsoft authentication
function toggleMicrosoftAuth() {
    const isChecked = document.getElementById('microsoftAuth').checked;
    document.getElementById('name').disabled = isChecked;
    document.getElementById('user_email').disabled = isChecked;
    document.getElementById('submitButton').textContent = isChecked ? "Continue with Microsoft" : "Submit";
}

// Function to handle registration or Microsoft login
function nextStep() {
    const id = document.getElementById('id').value.trim();
    const password = document.getElementById('password').value;
    const retypePassword = document.getElementById('retypePassword').value;
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('user_email').value.trim();

    if (!id || !password || !retypePassword) {
        showModal('Please fill in all required fields.');
        return;
    }
    if (password.length < 7) {
        showModal('Password must be at least 7 characters long.');
        return;
    }
    if (password !== retypePassword) {
        showModal('Passwords do not match.');
        return;
    }

    if (!microsoftAuth) {
        if (!name || !email) {
            showModal('Please fill in all fields.');
            return;
        }

        // Set cookies for user_id and user_password (expiring in 7 days)
        document.cookie = `sessionId=${id}; path=/; max-age=${60 * 60 * 24 * 7}`; // Expires in 7 days
        document.cookie = `password=${password}; path=/; max-age=${60 * 60 * 24 * 7}`; // Expires in 7 days

        const userData = {
            id,
            password,
            name,
            email
        };

        // Manual form submission
        fetch('/api/user_register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showModal(data.message);
            } else {
                showModal(data.message);
            }
        })
        .catch(error => {
            showModal('An error occurred. Please try again.');
            console.error('Error:', error);
        });

    } else {
        // Microsoft authentication flow: Set cookies for id and password before redirect
        document.cookie = `sessionId=${id}; path=/; max-age=${60 * 60 * 24 * 7}`; // Expires in 7 days
        document.cookie = `password=${password}; path=/; max-age=${60 * 60 * 24 * 7}`; // Expires in 7 days
        window.location.href = '/login/microsoft/';
    }
}

// Function to show modal with message
function showModal(message) {
    document.getElementById('modalMessage').textContent = message;
    document.getElementById('messageModal').style.display = 'block';
}

// Function to close the modal
function closeModal() {
    const modalMessage = document.getElementById('modalMessage').textContent;
    document.getElementById('messageModal').style.display = 'none';

    // Redirect to login page if the registration was successful
    if (modalMessage === 'User registered successfully!') {
        window.location.href = '/login/';
    }
}

// Function to get Microsoft authentication data from cookies
function getMicrosoftAuthData() {
    const userId = getCookie('sessionId');  // Correct cookie name
    const userPassword = getCookie('password');  // Correct cookie name

    if (userId && userPassword) {
        console.log("User ID:", userId);
        console.log("User Password:", userPassword);
        // You can now use these credentials to continue the authentication flow
    } else {
        console.log('No session data found.');
    }
}


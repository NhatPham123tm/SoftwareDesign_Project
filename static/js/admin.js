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


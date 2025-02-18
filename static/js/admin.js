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

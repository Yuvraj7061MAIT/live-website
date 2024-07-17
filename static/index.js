function toggleProfile() {
    var profileMenu = document.getElementById('profile-menu');
    profileMenu.classList.toggle('show');
}

function logout(event) {
    event.preventDefault();
    fetch("/logout", { method: "POST" })
        .then(response => {
            if (response.ok) {
                // Remove profile icon
                var profileIcon = document.getElementById('profile-icon');
                if (profileIcon) {
                    profileIcon.parentNode.removeChild(profileIcon);
                }
                // Change logout button to login button
                var logoutBtn = document.getElementById('logout-btn');
                logoutBtn.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-phone" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 4h5l2 5l-3 3l5 5l3 -3l5 2v5h-5l-2 -5l-3 3l-5 -5l3 -3z" /></svg>
                    <span>Login</span>
                `;
                logoutBtn.setAttribute('href', '/login');
                logoutBtn.setAttribute('id', 'login-btn');
                logoutBtn.removeAttribute('onclick');
            }
        })
        .catch(error => console.error('Logout error:', error));
}

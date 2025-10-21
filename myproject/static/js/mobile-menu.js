function toggleMobileMenu(event) {
    event.preventDefault();
    const mobileMenu = document.getElementById('mobileProfileMenu');
    mobileMenu.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

function closeMobileMenu() {
    const mobileMenu = document.getElementById('mobileProfileMenu');
    mobileMenu.classList.remove('active');
    document.body.style.overflow = ''; // Restore scrolling
}

// Close menu when clicking outside
document.addEventListener('click', function(event) {
    const mobileMenu = document.getElementById('mobileProfileMenu');
    const isClickInside = mobileMenu.contains(event.target);
    const isMenuButton = event.target.closest('[onclick="toggleMobileMenu(event)"]');
    
    if (!isClickInside && !isMenuButton && mobileMenu.classList.contains('active')) {
        closeMobileMenu();
    }
});

// Handle back button
window.addEventListener('popstate', function() {
    const mobileMenu = document.getElementById('mobileProfileMenu');
    if (mobileMenu.classList.contains('active')) {
        closeMobileMenu();
    }
});
// Mobile Profile Menu Functions
function showMobileProfileMenu() {
    const menu = document.getElementById('mobileProfileMenu');
    const overlay = document.querySelector('.mobile-menu-overlay');
    
    if (menu && window.innerWidth <= 768) {
        // Create overlay if it doesn't exist
        if (!overlay) {
            const newOverlay = document.createElement('div');
            newOverlay.className = 'mobile-menu-overlay';
            document.body.appendChild(newOverlay);
        }
        
        // Show menu and overlay
        menu.style.display = 'block';
        setTimeout(() => {
            menu.classList.add('active');
            if (overlay) overlay.style.display = 'block';
        }, 10);
        
        // Prevent body scrolling
        document.body.style.overflow = 'hidden';
    }
}

function closeMobileProfileMenu() {
    const menu = document.getElementById('mobileProfileMenu');
    const overlay = document.querySelector('.mobile-menu-overlay');
    
    if (menu) {
        menu.classList.remove('active');
        if (overlay) overlay.style.display = 'none';
        
        // Wait for animation to finish before hiding
        setTimeout(() => {
            menu.style.display = 'none';
            // Re-enable body scrolling
            document.body.style.overflow = '';
        }, 300);
    }
}

// Close menu when clicking overlay
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('mobile-menu-overlay')) {
        closeMobileProfileMenu();
    }
});
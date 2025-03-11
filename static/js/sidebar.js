/**
 * Enhanced sidebar functionality for Yaşar University website
 */
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const content = document.getElementById('content');
    
    // Initialize sidebar state from localStorage if available
    const sidebarState = localStorage.getItem('sidebarState');
    
    // Function to toggle sidebar
    function toggleSidebar() {
        const isActive = sidebar.classList.contains('active');
        const isMobile = window.innerWidth < 992;
        
        if (isMobile) {
            // For mobile: just toggle active class
            sidebar.classList.toggle('active');
        } else {
            // For desktop: toggle active class and adjust content margin
            sidebar.classList.toggle('active');
            
            if (isActive) {
                // Sidebar is currently active, so hide it
                content.style.marginLeft = '0px';
                sidebarToggle.style.left = '10px';
                localStorage.setItem('sidebarState', 'hidden');
            } else {
                // Sidebar is currently hidden, so show it
                content.style.marginLeft = '250px';
                sidebarToggle.style.left = '260px';
                localStorage.setItem('sidebarState', 'visible');
            }
        }
    }
    
    // Apply initial state
    if (window.innerWidth < 992) {
        // On mobile, always start with sidebar hidden
        content.style.marginLeft = '0px';
        sidebar.classList.remove('active');
    } else {
        // On desktop, respect saved preference or default to visible
        if (sidebarState === 'hidden') {
            content.style.marginLeft = '0px';
            sidebarToggle.style.left = '10px';
            sidebar.classList.remove('active');
        } else {
            content.style.marginLeft = '250px';
            sidebarToggle.style.left = '260px';
            sidebar.classList.add('active');
        }
    }
    
    // Toggle button event listener
    sidebarToggle.addEventListener('click', toggleSidebar);
    
    // Handle window resize events
    window.addEventListener('resize', function() {
        const isMobile = window.innerWidth < 992;
        
        if (isMobile) {
            // On mobile: collapse sidebar and reset content margin
            content.style.marginLeft = '0px';
            sidebarToggle.style.left = '10px';
        } else {
            // On desktop: respect the current state
            if (sidebar.classList.contains('active')) {
                content.style.marginLeft = '250px';
                sidebarToggle.style.left = '260px';
            } else {
                content.style.marginLeft = '0px';
                sidebarToggle.style.left = '10px';
            }
        }
    });
    
    // Add active class to current page link in sidebar
    const currentPath = window.location.pathname;
    const sidebarLinks = sidebar.querySelectorAll('a');
    
    sidebarLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active', 'bg-light', 'fw-bold');
        }
    });
});

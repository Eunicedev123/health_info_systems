// Main JavaScript for Health Information System

document.addEventListener('DOMContentLoaded', function() {
    // Auto-close alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Add date formatting helper
    const dateElements = document.querySelectorAll('.format-date');
    dateElements.forEach(function(element) {
        const date = new Date(element.textContent);
        element.textContent = date.toLocaleDateString();
    });
    
    // Add client search functionality
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.focus();
        
        // Clear search with escape key
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                searchInput.value = '';
                searchInput.form.submit();
            }
        });
    }
});
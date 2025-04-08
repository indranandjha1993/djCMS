/**
 * Admin Dashboard JavaScript
 * Enhances the admin dashboard with interactive features
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard components
    initializeCharts();
    initializeTooltips();
    initializeCollapsibleSections();
    
    // Add event listeners for quick actions
    document.querySelectorAll('.quick-action').forEach(function(action) {
        action.addEventListener('mouseenter', function() {
            this.querySelector('.quick-action-icon').classList.add('animate-bounce');
        });
        
        action.addEventListener('mouseleave', function() {
            this.querySelector('.quick-action-icon').classList.remove('animate-bounce');
        });
    });
});

/**
 * Initialize charts for the dashboard
 */
function initializeCharts() {
    // This is a placeholder for chart initialization
    // You can integrate Chart.js or another library here
    console.log('Charts initialized');
}

/**
 * Initialize tooltips for the dashboard
 */
function initializeTooltips() {
    // Add tooltip functionality to elements with data-tooltip attribute
    document.querySelectorAll('[data-tooltip]').forEach(function(element) {
        element.setAttribute('title', element.getAttribute('data-tooltip'));
    });
}

/**
 * Initialize collapsible sections
 */
function initializeCollapsibleSections() {
    document.querySelectorAll('.dashboard-widget-header').forEach(function(header) {
        header.addEventListener('click', function() {
            const content = this.nextElementSibling;
            
            // Check if the content is already collapsed
            const isCollapsed = content.style.display === 'none';
            
            // Toggle the content visibility
            content.style.display = isCollapsed ? 'block' : 'none';
            
            // Add/remove collapsed class for styling
            if (isCollapsed) {
                this.classList.remove('collapsed');
            } else {
                this.classList.add('collapsed');
            }
        });
    });
}
/**
 * Main JavaScript file for djCMS
 * Contains all interactive functionality for the site
 */

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle with animation
    initMobileMenu();
    
    // Search modal functionality
    initSearchModal();
    
    // User menu dropdown functionality
    initUserMenu();
    
    // Back to top button functionality
    initBackToTopButton();
    
    // Add scroll effects to header
    initHeaderScrollEffects();
    
    // Animate elements when they come into view
    initScrollAnimations();
    
    // Add keyboard navigation for dropdown menus
    initKeyboardNavigation();
    
    // Add smooth scrolling for anchor links
    initSmoothScrolling();
});

// Register Service Worker for PWA support
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/service-worker.js')
            .then(registration => {
                console.log('Service Worker registered with scope:', registration.scope);
            })
            .catch(error => {
                console.error('Service Worker registration failed:', error);
            });
    });
}

// Add support for prefers-reduced-motion
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

if (prefersReducedMotion.matches) {
    document.documentElement.classList.add('no-animation');
    
    // Add a style element to disable animations
    const style = document.createElement('style');
    style.textContent = `
        .no-animation * {
            animation: none !important;
            transition: none !important;
        }
    `;
    document.head.appendChild(style);
}

// Add dark mode support if theme supports it
const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)');

function setDarkModeClass(darkMode) {
    if (darkMode) {
        document.documentElement.classList.add('dark-mode');
    } else {
        document.documentElement.classList.remove('dark-mode');
    }
}

// Set initial dark mode state
setDarkModeClass(prefersDarkMode.matches);

// Listen for changes in dark mode preference
prefersDarkMode.addEventListener('change', (e) => {
    setDarkModeClass(e.matches);
});

/**
 * Initialize mobile menu functionality with PWA best practices
 */
function initMobileMenu() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuBackdrop = document.getElementById('mobile-menu-backdrop');
    const closeMobileMenuButton = document.getElementById('close-mobile-menu');
    
    if (mobileMenuButton && mobileMenu && mobileMenuBackdrop) {
        // Track touch start position for swipe detection
        let touchStartX = 0;
        let touchEndX = 0;
        
        // Open mobile menu with proper animation
        mobileMenuButton.addEventListener('click', function() {
            openMobileMenu();
        });
        
        // Open mobile menu function
        const openMobileMenu = function() {
            // Ensure the menu is on top with inline styles
            mobileMenuBackdrop.style.zIndex = '999999';
            mobileMenu.style.zIndex = '1000000';
            
            // First make backdrop visible
            mobileMenuBackdrop.classList.remove('hidden');
            
            // Force a reflow to ensure the backdrop is visible before animating
            void mobileMenuBackdrop.offsetWidth;
            
            // Then animate the menu
            requestAnimationFrame(() => {
                mobileMenu.classList.remove('translate-x-full');
                mobileMenu.classList.add('translate-x-0');
            });
            
            mobileMenuButton.setAttribute('aria-expanded', 'true');
            
            // Prevent body scrolling - fixed position approach for better compatibility
            document.body.classList.add('overflow-hidden');
            document.body.classList.add('mobile-menu-open');
            document.documentElement.classList.add('mobile-menu-open');
            
            // Announce to screen readers
            const announcement = document.createElement('div');
            announcement.setAttribute('aria-live', 'polite');
            announcement.setAttribute('class', 'sr-only');
            announcement.textContent = 'Navigation menu opened';
            document.body.appendChild(announcement);
            setTimeout(() => announcement.remove(), 1000);
        };
        
        // Close mobile menu function
        const closeMobileMenu = function() {
            mobileMenu.classList.remove('translate-x-0');
            mobileMenu.classList.add('translate-x-full');
            
            // Wait for animation to complete before hiding backdrop
            setTimeout(() => {
                mobileMenuBackdrop.classList.add('hidden');
            }, 300);
            
            mobileMenuButton.setAttribute('aria-expanded', 'false');
            
            // Re-enable body scrolling
            document.body.classList.remove('overflow-hidden');
            document.body.classList.remove('mobile-menu-open');
            document.documentElement.classList.remove('mobile-menu-open');
            
            // Announce to screen readers
            const announcement = document.createElement('div');
            announcement.setAttribute('aria-live', 'polite');
            announcement.setAttribute('class', 'sr-only');
            announcement.textContent = 'Navigation menu closed';
            document.body.appendChild(announcement);
            setTimeout(() => announcement.remove(), 1000);
        };
        
        // Close button click
        if (closeMobileMenuButton) {
            closeMobileMenuButton.addEventListener('click', closeMobileMenu);
        }
        
        // Close when clicking on backdrop
        mobileMenuBackdrop.addEventListener('click', function(event) {
            if (event.target === mobileMenuBackdrop) {
                closeMobileMenu();
            }
        });
        
        // Handle escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && !mobileMenuBackdrop.classList.contains('hidden')) {
                closeMobileMenu();
            }
        });
        
        // Handle swipe gestures for mobile
        mobileMenu.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        mobileMenu.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });
        
        // Handle swipe right to close menu
        function handleSwipe() {
            const swipeThreshold = 100; // Minimum distance for a swipe
            if (touchEndX - touchStartX > swipeThreshold) {
                // Swiped right, close the menu
                closeMobileMenu();
            }
        }
        
        // Add edge swipe detection to open menu (PWA pattern)
        document.addEventListener('touchstart', function(e) {
            // Only detect edge swipes when menu is closed
            if (mobileMenuBackdrop.classList.contains('hidden')) {
                touchStartX = e.changedTouches[0].screenX;
                
                // Check if touch started near the right edge (within 20px)
                if (touchStartX > window.innerWidth - 20) {
                    document.addEventListener('touchend', handleEdgeSwipe, { once: true, passive: true });
                }
            }
        }, { passive: true });
        
        function handleEdgeSwipe(e) {
            touchEndX = e.changedTouches[0].screenX;
            const swipeDistance = touchStartX - touchEndX;
            
            // If swiped left from right edge for at least 50px
            if (swipeDistance > 50) {
                openMobileMenu();
            }
        }
        
        // Mobile dropdown toggles with improved touch handling
        const mobileDropdownToggles = document.querySelectorAll('.mobile-dropdown-toggle');
        mobileDropdownToggles.forEach(toggle => {
            toggle.addEventListener('click', function() {
                const dropdownMenu = this.nextElementSibling;
                const icon = this.querySelector('i');
                
                if (dropdownMenu && dropdownMenu.classList.contains('mobile-dropdown-menu')) {
                    // Toggle with animation
                    if (dropdownMenu.classList.contains('hidden')) {
                        dropdownMenu.classList.remove('hidden');
                        dropdownMenu.style.maxHeight = '0';
                        requestAnimationFrame(() => {
                            dropdownMenu.style.maxHeight = dropdownMenu.scrollHeight + 'px';
                        });
                    } else {
                        dropdownMenu.style.maxHeight = '0';
                        setTimeout(() => {
                            dropdownMenu.classList.add('hidden');
                        }, 300);
                    }
                    
                    if (icon) {
                        icon.classList.toggle('rotate-180');
                    }
                    
                    // Update aria attributes
                    const expanded = this.getAttribute('aria-expanded') === 'true' || false;
                    this.setAttribute('aria-expanded', !expanded);
                }
            });
        });
    }
}

/**
 * Initialize search modal functionality
 */
function initSearchModal() {
    const searchButton = document.getElementById('search-button');
    const searchModal = document.getElementById('search-modal');
    const closeSearchButton = document.getElementById('close-search');
    const modalSearch = document.getElementById('modal-search');
    
    if (searchButton && searchModal) {
        // Open search modal
        searchButton.addEventListener('click', function() {
            searchModal.classList.remove('hidden');
            // Focus the search input after a short delay to ensure modal is visible
            setTimeout(() => {
                if (modalSearch) modalSearch.focus();
            }, 100);
            // Prevent body scrolling
            document.body.classList.add('overflow-hidden');
        });
        
        // Close search modal function
        const closeSearchModal = function() {
            searchModal.classList.add('hidden');
            // Re-enable body scrolling
            document.body.classList.remove('overflow-hidden');
        };
        
        // Close button click
        if (closeSearchButton) {
            closeSearchButton.addEventListener('click', closeSearchModal);
        }
        
        // Close when clicking outside the modal content
        searchModal.addEventListener('click', function(event) {
            if (event.target === searchModal) {
                closeSearchModal();
            }
        });
        
        // Handle escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && !searchModal.classList.contains('hidden')) {
                closeSearchModal();
            }
        });
    }
}

/**
 * Initialize user menu dropdown functionality
 */
function initUserMenu() {
    const userMenuButton = document.getElementById('user-menu-button');
    const userDropdownMenu = document.getElementById('user-dropdown-menu');
    const userMenuArrow = document.getElementById('user-menu-arrow');
    
    if (userMenuButton && userDropdownMenu) {
        userMenuButton.addEventListener('click', function(e) {
            e.preventDefault();
            userDropdownMenu.classList.toggle('hidden');
            if (userMenuArrow) {
                userMenuArrow.classList.toggle('rotate-180');
            }
            
            // Set aria-expanded attribute
            const expanded = userMenuButton.getAttribute('aria-expanded') === 'true' || false;
            userMenuButton.setAttribute('aria-expanded', !expanded);
        });
        
        // Close when clicking outside
        document.addEventListener('click', function(event) {
            if (!userMenuButton.contains(event.target) && !userDropdownMenu.contains(event.target)) {
                userDropdownMenu.classList.add('hidden');
                if (userMenuArrow) {
                    userMenuArrow.classList.remove('rotate-180');
                }
                userMenuButton.setAttribute('aria-expanded', 'false');
            }
        });
        
        // Close on escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && !userDropdownMenu.classList.contains('hidden')) {
                userDropdownMenu.classList.add('hidden');
                if (userMenuArrow) {
                    userMenuArrow.classList.remove('rotate-180');
                }
                userMenuButton.setAttribute('aria-expanded', 'false');
            }
        });
    }
}

/**
 * Initialize back to top button functionality
 */
function initBackToTopButton() {
    const backToTopButton = document.getElementById('back-to-top');
    
    if (backToTopButton) {
        // Show/hide back to top button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopButton.classList.remove('scale-0');
                backToTopButton.classList.add('scale-100');
            } else {
                backToTopButton.classList.remove('scale-100');
                backToTopButton.classList.add('scale-0');
            }
        });
        
        // Scroll to top when button is clicked
        backToTopButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

/**
 * Initialize header scroll effects
 */
function initHeaderScrollEffects() {
    const header = document.querySelector('header');
    
    if (header) {
        const handleScroll = function() {
            const scrollTop = window.scrollY;
            
            // Add shadow and reduce padding on scroll
            if (scrollTop > 10) {
                header.classList.add('py-2');
                header.classList.remove('py-3');
                header.classList.add('shadow-elevated');
                header.classList.add('bg-white/95');
            } else {
                header.classList.remove('py-2');
                header.classList.add('py-3');
                header.classList.remove('shadow-elevated');
                header.classList.remove('bg-white/95');
            }
        };
        
        window.addEventListener('scroll', handleScroll);
        // Initial call to set correct state on page load
        handleScroll();
    }
}

/**
 * Initialize scroll animations
 */
function initScrollAnimations() {
    if ('IntersectionObserver' in window) {
        const animateElements = document.querySelectorAll('.card, .btn, h1, h2, h3, .animate-on-scroll');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, { 
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        animateElements.forEach(element => {
            observer.observe(element);
        });
    }
}

/**
 * Initialize keyboard navigation for dropdown menus
 */
function initKeyboardNavigation() {
    const dropdownMenus = document.querySelectorAll('.group');
    
    dropdownMenus.forEach(menu => {
        const trigger = menu.querySelector('[aria-haspopup="true"]');
        const dropdown = menu.querySelector('[role="menu"]');
        
        if (trigger && dropdown) {
            // Handle keyboard navigation
            trigger.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowDown') {
                    e.preventDefault();
                    
                    // Show dropdown
                    dropdown.classList.add('opacity-100', 'visible', 'translate-y-0');
                    dropdown.classList.remove('opacity-0', 'invisible', 'translate-y-2');
                    
                    // Focus first item
                    const firstItem = dropdown.querySelector('[role="menuitem"]');
                    if (firstItem) firstItem.focus();
                    
                    trigger.setAttribute('aria-expanded', 'true');
                }
            });
            
            // Handle keyboard navigation within dropdown
            dropdown.addEventListener('keydown', function(e) {
                const menuItems = dropdown.querySelectorAll('[role="menuitem"]');
                const currentIndex = Array.from(menuItems).indexOf(document.activeElement);
                
                if (e.key === 'Escape') {
                    // Close dropdown and focus trigger
                    dropdown.classList.remove('opacity-100', 'visible', 'translate-y-0');
                    dropdown.classList.add('opacity-0', 'invisible', 'translate-y-2');
                    trigger.setAttribute('aria-expanded', 'false');
                    trigger.focus();
                } else if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    const nextIndex = (currentIndex + 1) % menuItems.length;
                    menuItems[nextIndex].focus();
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    const prevIndex = (currentIndex - 1 + menuItems.length) % menuItems.length;
                    menuItems[prevIndex].focus();
                }
            });
            
            // Close dropdown when focus leaves
            menu.addEventListener('focusout', function(e) {
                if (!menu.contains(e.relatedTarget)) {
                    dropdown.classList.remove('opacity-100', 'visible', 'translate-y-0');
                    dropdown.classList.add('opacity-0', 'invisible', 'translate-y-2');
                    trigger.setAttribute('aria-expanded', 'false');
                }
            });
        }
    });
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScrolling() {
    const header = document.querySelector('header');
    
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                
                const headerOffset = header ? header.offsetHeight : 0;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset - 20;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
                
                // Update URL without page jump
                history.pushState(null, null, targetId);
                
                // Set focus to the target element
                targetElement.setAttribute('tabindex', '-1');
                targetElement.focus({ preventScroll: true });
            }
        });
    });
}
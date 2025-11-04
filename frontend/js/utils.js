/**
 * Utility functions
 */

/**
 * Get token from localStorage
 */
function getToken() {
    return localStorage.getItem('access_token');
}

/**
 * Set token in localStorage
 */
function setToken(token) {
    localStorage.setItem('access_token', token);
}

/**
 * Remove token from localStorage
 */
function removeToken() {
    localStorage.removeItem('access_token');
}

/**
 * Get current user from localStorage
 */
function getCurrentUser() {
    const userStr = localStorage.getItem('current_user');
    return userStr ? JSON.parse(userStr) : null;
}

/**
 * Set current user in localStorage
 */
function setCurrentUser(user) {
    localStorage.setItem('current_user', JSON.stringify(user));
}

/**
 * Remove current user from localStorage
 */
function removeCurrentUser() {
    localStorage.removeItem('current_user');
}

/**
 * Show error message
 */
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Hide after 5 seconds
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }
}

/**
 * Show success message
 */
function showSuccess(message) {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.className = 'success-message';
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Hide after 5 seconds
        setTimeout(() => {
            errorDiv.style.display = 'none';
            errorDiv.className = 'error-message';
        }, 5000);
    }
}

/**
 * Show loading indicator
 */
function showLoading() {
    const loadingDiv = document.getElementById('loading');
    if (loadingDiv) {
        loadingDiv.style.display = 'block';
    }
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    const loadingDiv = document.getElementById('loading');
    if (loadingDiv) {
        loadingDiv.style.display = 'none';
    }
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}


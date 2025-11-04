/**
 * Main application logic
 */

// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    
    // Setup form handlers
    setupFormHandlers();
});

/**
 * Check if user is authenticated
 */
function checkAuth() {
    const token = getToken();
    const user = getCurrentUser();
    
    if (token && user) {
        // User is logged in
        showApp();
    } else {
        // User is not logged in
        showAuth();
    }
}

/**
 * Show authentication section
 */
function showAuth() {
    document.getElementById('auth-section').style.display = 'block';
    document.getElementById('app-section').style.display = 'none';
}

/**
 * Show app section
 */
function showApp() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('app-section').style.display = 'block';
}

/**
 * Setup form handlers
 */
function setupFormHandlers() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    // Dish search form
    const dishSearchForm = document.getElementById('dish-search-form');
    if (dishSearchForm) {
        dishSearchForm.addEventListener('submit', handleDishSearch);
    }
    
    // Profile form
    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', handleProfileUpdate);
    }
}

/**
 * Handle login
 */
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        showLoading();
        const result = await authAPI.login(username, password);
        
        setToken(result.access_token);
        setCurrentUser(result.user);
        
        showApp();
        showSuccess('Login successful!');
    } catch (error) {
        showError(error.message || 'Login failed');
    } finally {
        hideLoading();
    }
}

/**
 * Handle register
 */
async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const householdSize = document.getElementById('register-household').value;
    
    try {
        showLoading();
        const result = await authAPI.register(username, email, password, householdSize);
        
        setToken(result.access_token);
        setCurrentUser(result.user);
        
        showApp();
        showSuccess('Registration successful!');
    } catch (error) {
        showError(error.message || 'Registration failed');
    } finally {
        hideLoading();
    }
}

/**
 * Handle dish search
 */
async function handleDishSearch(e) {
    e.preventDefault();
    
    const dishName = document.getElementById('dish-name').value;
    
    if (!dishName) {
        showError('Please enter a dish name');
        return;
    }
    
    try {
        showLoading();
        document.getElementById('recipe-results').style.display = 'none';
        document.getElementById('error-message').style.display = 'none';
        
        const result = await dishAPI.search(dishName);
        
        displayRecipeResults(result);
        showSuccess('Recipe found!');
    } catch (error) {
        showError(error.message || 'Recipe not found. Please try a different dish name.');
    } finally {
        hideLoading();
    }
}

/**
 * Handle profile update
 */
async function handleProfileUpdate(e) {
    e.preventDefault();
    
    const householdSize = document.getElementById('profile-household').value;
    const dietary = document.getElementById('profile-dietary').value;
    const dietaryRestrictions = dietary ? dietary.split(',').map(d => d.trim()) : [];
    
    try {
        showLoading();
        await userAPI.updateProfile({
            household_size: householdSize,
            dietary_restrictions: dietaryRestrictions
        });
        
        // Update local user
        const user = getCurrentUser();
        if (user) {
            user.household_size = householdSize;
            user.dietary_restrictions = dietaryRestrictions;
            setCurrentUser(user);
        }
        
        showSuccess('Profile updated successfully!');
    } catch (error) {
        showError(error.message || 'Failed to update profile');
    } finally {
        hideLoading();
    }
}

/**
 * Logout
 */
function logout() {
    removeToken();
    removeCurrentUser();
    showAuth();
    showSuccess('Logged out successfully');
}


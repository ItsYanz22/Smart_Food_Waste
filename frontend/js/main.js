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
    
    // Show welcome message with username
    const user = getCurrentUser();
    if (user && user.username) {
        const welcomeText = document.getElementById('welcome-text');
        if (welcomeText) {
            welcomeText.textContent = `Welcome Back, ${user.username}!`;
        }
    }
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
    
    // Recipe URL form
    const recipeUrlForm = document.getElementById('recipe-url-form');
    if (recipeUrlForm) {
        recipeUrlForm.addEventListener('submit', handleRecipeUrl);
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
    
    // Prevent multiple submissions
    const submitBtn = e.target.querySelector('button[type="submit"]');
    if (submitBtn && submitBtn.disabled) {
        return; // Already submitting
    }
    
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;
    
    if (!username || !password) {
        showError('Please enter username and password');
        return;
    }
    
    try {
        showLoading();
        if (submitBtn) submitBtn.disabled = true;
        
        const result = await authAPI.login(username, password);
        
        setToken(result.access_token);
        setCurrentUser(result.user);
        
        showApp();
        showSuccess('Login successful!');
    } catch (error) {
        console.error('Login error:', error);
        showError(error.message || 'Login failed. Please check your credentials.');
    } finally {
        hideLoading();
        if (submitBtn) submitBtn.disabled = false;
    }
}

/**
 * Handle register
 */
async function handleRegister(e) {
    e.preventDefault();
    
    // Prevent multiple submissions
    const submitBtn = e.target.querySelector('button[type="submit"]');
    if (submitBtn && submitBtn.disabled) {
        return; // Already submitting
    }
    
    const username = document.getElementById('register-username').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const password = document.getElementById('register-password').value;
    const householdSize = document.getElementById('register-household').value || '1';
    
    // Basic client-side validation
    if (!username || !email || !password) {
        showError('Please fill in all required fields');
        return;
    }
    
    if (password.length < 6) {
        showError('Password must be at least 6 characters');
        return;
    }
    
    try {
        showLoading();
        if (submitBtn) submitBtn.disabled = true;
        
        // Debug: Log what we're sending
        console.log('=== REGISTRATION REQUEST ===');
        console.log('Username:', username);
        console.log('Email:', email);
        console.log('Password length:', password.length);
        console.log('Household Size:', householdSize);
        
        const requestData = {
            username: username.trim(),
            email: email.trim().toLowerCase(),
            password: password,
            household_size: householdSize ? String(householdSize).trim() : '1'
        };
        console.log('Request data:', requestData);
        
        const result = await authAPI.register(username, email, password, householdSize);
        
        console.log('Registration success:', result);
        setToken(result.access_token);
        setCurrentUser(result.user);
        
        showApp();
        showSuccess('Registration successful!');
    } catch (error) {
        console.error('Registration error:', error);
        console.error('Error details:', {
            message: error.message,
            stack: error.stack
        });
        showError(error.message || 'Registration failed. Please try again.');
    } finally {
        hideLoading();
        if (submitBtn) submitBtn.disabled = false;
    }
}

/**
 * Handle dish search
 */
async function handleDishSearch(e) {
    e.preventDefault();
    
    const dishName = document.getElementById('dish-name').value.trim();
    
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
        showSuccess('Recipe found! Ingredients have been saved to the database.');
    } catch (error) {
        showError(error.message || 'Recipe not found. Please try a different dish name.');
    } finally {
        hideLoading();
    }
}

/**
 * Handle recipe URL submission
 */
async function handleRecipeUrl(e) {
    e.preventDefault();
    
    const recipeUrl = document.getElementById('recipe-url').value.trim();
    
    if (!recipeUrl) {
        showError('Please enter a recipe URL');
        return;
    }
    
    // Basic URL validation
    try {
        new URL(recipeUrl);
    } catch (error) {
        showError('Please enter a valid URL');
        return;
    }
    
    try {
        showLoading();
        document.getElementById('recipe-results').style.display = 'none';
        document.getElementById('error-message').style.display = 'none';
        
        const result = await dishAPI.extractFromUrl(recipeUrl);
        
        displayRecipeResults(result);
        showSuccess('Recipe extracted! Ingredients have been saved to the database.');
    } catch (error) {
        showError(error.message || 'Could not extract recipe from URL. Please try a different URL.');
    } finally {
        hideLoading();
    }
}

/**
 * Switch between search methods
 * Made global for onclick handlers
 */
window.switchSearchMethod = function(method) {
    const nameForm = document.getElementById('dish-search-form');
    const urlForm = document.getElementById('recipe-url-form');
    const tabs = document.querySelectorAll('.search-tabs .tab-btn');
    
    if (!nameForm || !urlForm) {
        console.error('Search forms not found');
        return;
    }
    
    if (method === 'name') {
        nameForm.style.display = 'block';
        urlForm.style.display = 'none';
        if (tabs.length >= 2) {
            tabs[0].classList.add('active');
            tabs[1].classList.remove('active');
        }
    } else {
        nameForm.style.display = 'none';
        urlForm.style.display = 'block';
        if (tabs.length >= 2) {
            tabs[0].classList.remove('active');
            tabs[1].classList.add('active');
        }
    }
};

/**
 * Download recipe PDF
 * Made global for onclick handlers
 */
window.downloadRecipePDF = async function() {
    if (!currentRecipeId) {
        showError('No recipe selected');
        return;
    }
    
    try {
        showLoading();
        const result = await dishAPI.downloadRecipePDF(currentRecipeId);
        if (result.pdf_url) {
            window.open(result.pdf_url, '_blank');
            showSuccess('Recipe PDF downloaded!');
        }
    } catch (error) {
        showError(error.message || 'Failed to download recipe PDF');
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
 * Made global for onclick handlers
 */
window.logout = function() {
    removeToken();
    removeCurrentUser();
    showAuth();
    showSuccess('Logged out successfully');
}


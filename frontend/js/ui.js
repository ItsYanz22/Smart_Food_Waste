/**
 * UI interaction functions
 */

let currentRecipe = null;
let currentRecipeId = null;

/**
 * Show login form
 */
function showLogin() {
    document.getElementById('login-form').classList.add('active');
    document.getElementById('register-form').classList.remove('active');
    document.querySelectorAll('.tab-btn')[0].classList.add('active');
    document.querySelectorAll('.tab-btn')[1].classList.remove('active');
}

/**
 * Show register form
 */
function showRegister() {
    document.getElementById('register-form').classList.add('active');
    document.getElementById('login-form').classList.remove('active');
    document.querySelectorAll('.tab-btn')[0].classList.remove('active');
    document.querySelectorAll('.tab-btn')[1].classList.add('active');
}

/**
 * Show section
 * Made global for onclick handlers
 */
window.showSection = function(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    const section = document.getElementById(`${sectionName}-section`);
    if (section) {
        section.classList.add('active');
    }
    
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    // Load data if needed
    if (sectionName === 'lists') {
        loadGroceryLists();
    } else if (sectionName === 'profile') {
        loadProfile();
    }
};

/**
 * Display recipe results
 */
function displayRecipeResults(recipeData) {
    currentRecipe = recipeData.recipe;
    currentRecipeId = recipeData.recipe.id;
    
    const resultsDiv = document.getElementById('recipe-results');
    const infoDiv = document.getElementById('recipe-info');
    
    if (!resultsDiv || !infoDiv) return;
    
    // Build recipe info HTML
    let html = `
        <div class="recipe-info">
            <h4>${recipeData.dish.name}</h4>
            <p><strong>Servings:</strong> ${currentRecipe.servings}</p>
            ${currentRecipe.source_url ? `<p><strong>Source:</strong> <a href="${currentRecipe.source_url}" target="_blank">${currentRecipe.source_url}</a></p>` : ''}
            <div class="ingredients-section">
                <h5>Ingredients (automatically saved to database):</h5>
                <ul class="ingredient-list">
    `;
    
    currentRecipe.ingredients.forEach(ing => {
        html += `
            <li>
                <span>${ing.name}</span>
                <span class="quantity">${ing.quantity} ${ing.unit || ''}</span>
            </li>
        `;
    });
    
    // Add instructions if available
    if (currentRecipe.instructions && currentRecipe.instructions.length > 0) {
        html += `
                </ul>
            </div>
            <div class="instructions-section">
                <h5>Instructions:</h5>
                <ol class="instruction-list">
        `;
        currentRecipe.instructions.forEach((instruction, index) => {
            html += `<li>${instruction}</li>`;
        });
        html += `</ol></div>`;
    } else {
        html += `</ul></div>`;
    }
    
    html += `</div>`;
    
    infoDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
    
    // Set default household size from user profile
    const user = getCurrentUser();
    if (user && user.household_size) {
        document.getElementById('household-size').value = user.household_size;
    }
}

/**
 * Generate grocery list
 * Made global for onclick handlers
 */
window.generateGroceryList = async function() {
    if (!currentRecipe) {
        showError('Please search for a recipe first');
        return;
    }
    
    const dishName = currentRecipe.dish_name;
    const householdSize = document.getElementById('household-size').value;
    
    if (!householdSize || householdSize < 1) {
        showError('Please enter a valid household size');
        return;
    }
    
    try {
        showLoading();
        const result = await groceryAPI.generate(dishName, householdSize, currentRecipeId);
        showSuccess('Grocery list generated successfully!');
        
        // Show the list
        showSection('lists');
        loadGroceryLists();
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Add dish to favorites
 * Made global for onclick handlers
 */
window.addToFavorites = async function() {
    if (!currentRecipe) {
        showError('No recipe selected');
        return;
    }
    
    try {
        await dishAPI.addFavorite(currentRecipe.dish_name);
        showSuccess('Dish added to favorites!');
        loadProfile(); // Refresh profile to show updated favorites
    } catch (error) {
        showError(error.message);
    }
}

/**
 * Load grocery lists
 */
async function loadGroceryLists() {
    const listsDiv = document.getElementById('grocery-lists');
    if (!listsDiv) return;
    
    try {
        const result = await groceryAPI.getLists();
        const lists = result.grocery_lists || [];
        
        if (lists.length === 0) {
            listsDiv.innerHTML = '<p class="empty-state">No grocery lists yet. Search for a dish to get started!</p>';
            return;
        }
        
        let html = '';
        lists.forEach(list => {
            html += `
                <div class="grocery-list-card">
                    <h3>${list.dish_name}</h3>
                    <div class="meta">
                        Household Size: ${list.household_size} | Created: ${formatDate(list.created_at)}
                    </div>
                    <p><strong>Items:</strong> ${list.items.length}</p>
                    <div class="grocery-list-actions">
                        <button class="btn btn-primary" onclick="viewGroceryList('${list.id}')">View</button>
                        <button class="btn btn-success" onclick="downloadPDF('${list.id}')">Download PDF</button>
                        <button class="btn btn-secondary" onclick="downloadCSV('${list.id}')">Download CSV</button>
                        <button class="btn btn-secondary" onclick="deleteGroceryList('${list.id}')">Delete</button>
                    </div>
                </div>
            `;
        });
        
        listsDiv.innerHTML = html;
    } catch (error) {
        showError(error.message);
        listsDiv.innerHTML = '<p class="empty-state">Error loading grocery lists</p>';
    }
}

/**
 * View grocery list details
 */
async function viewGroceryList(listId) {
    try {
        const result = await groceryAPI.getList(listId);
        const list = result;
        
        // Display list in a modal or new section
        alert(`Grocery List: ${list.dish_name}\nItems: ${list.items.length}\nHousehold Size: ${list.household_size}`);
    } catch (error) {
        showError(error.message);
    }
}

/**
 * Download PDF
 */
async function downloadPDF(listId) {
    try {
        const result = await groceryAPI.downloadPDF(listId);
        if (result.pdf_url) {
            window.open(result.pdf_url, '_blank');
        }
    } catch (error) {
        showError(error.message);
    }
}

/**
 * Download CSV
 */
async function downloadCSV(listId) {
    try {
        const result = await groceryAPI.downloadCSV(listId);
        const csvData = result.csv_data;
        const dishName = result.dish_name;
        
        // Convert to CSV format
        let csv = 'Ingredient,Quantity,Unit,Category\n';
        csvData.forEach(item => {
            csv += `${item.ingredient},${item.quantity},${item.unit},${item.category}\n`;
        });
        
        // Download
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${dishName}_grocery_list.csv`;
        a.click();
    } catch (error) {
        showError(error.message);
    }
}

/**
 * Delete grocery list
 */
async function deleteGroceryList(listId) {
    if (!confirm('Are you sure you want to delete this grocery list?')) {
        return;
    }
    
    try {
        await groceryAPI.deleteList(listId);
        showSuccess('Grocery list deleted');
        loadGroceryLists();
    } catch (error) {
        showError(error.message);
    }
}

/**
 * Load user profile
 */
async function loadProfile() {
    try {
        const result = await userAPI.getProfile();
        const user = result;
        
        // Update form fields
        document.getElementById('profile-household').value = user.household_size || '1';
        document.getElementById('profile-dietary').value = user.dietary_restrictions ? user.dietary_restrictions.join(', ') : '';
        
        // Load favorite dishes
        const favoritesDiv = document.getElementById('favorite-dishes');
        if (favoritesDiv && user.favorite_dishes) {
            let html = '';
            user.favorite_dishes.forEach(dish => {
                html += `<span class="favorite-dish-tag" onclick="searchDishFromFavorite('${dish}')">${dish}</span>`;
            });
            favoritesDiv.innerHTML = html || '<p>No favorite dishes yet</p>';
        }
    } catch (error) {
        showError(error.message);
    }
}

/**
 * Search dish from favorite
 */
function searchDishFromFavorite(dishName) {
    document.getElementById('dish-name').value = dishName;
    showSection('search');
    document.getElementById('dish-search-form').dispatchEvent(new Event('submit'));
}


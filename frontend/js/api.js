/**
 * API communication functions
 */

const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Make API request with authentication
 */
async function apiRequest(endpoint, method = 'GET', data = null) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const options = {
        method,
        headers
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Request failed');
        }
        
        return result;
    } catch (error) {
        throw error;
    }
}

/**
 * Auth API calls
 */
const authAPI = {
    register: async (username, email, password, householdSize) => {
        return apiRequest('/auth/register', 'POST', {
            username,
            email,
            password,
            household_size: householdSize
        });
    },
    
    login: async (username, password) => {
        return apiRequest('/auth/login', 'POST', {
            username,
            password
        });
    },
    
    getCurrentUser: async () => {
        return apiRequest('/auth/me', 'GET');
    }
};

/**
 * Dish API calls
 */
const dishAPI = {
    search: async (dishName) => {
        return apiRequest('/dish/search', 'POST', {
            dish_name: dishName
        });
    },
    
    getFavorites: async () => {
        return apiRequest('/dish/favorites', 'GET');
    },
    
    addFavorite: async (dishName) => {
        return apiRequest('/dish/favorites', 'POST', {
            dish_name: dishName
        });
    }
};

/**
 * Grocery API calls
 */
const groceryAPI = {
    generate: async (dishName, householdSize, recipeId) => {
        return apiRequest('/grocery/generate', 'POST', {
            dish_name: dishName,
            household_size: householdSize,
            recipe_id: recipeId
        });
    },
    
    getLists: async () => {
        return apiRequest('/grocery/lists', 'GET');
    },
    
    getList: async (listId) => {
        return apiRequest(`/grocery/lists/${listId}`, 'GET');
    },
    
    updateList: async (listId, data) => {
        return apiRequest(`/grocery/lists/${listId}`, 'PUT', data);
    },
    
    deleteList: async (listId) => {
        return apiRequest(`/grocery/lists/${listId}`, 'DELETE');
    },
    
    downloadPDF: async (listId) => {
        return apiRequest(`/grocery/lists/${listId}/download/pdf`, 'GET');
    },
    
    downloadCSV: async (listId) => {
        return apiRequest(`/grocery/lists/${listId}/download/csv`, 'GET');
    }
};

/**
 * User API calls
 */
const userAPI = {
    getProfile: async () => {
        return apiRequest('/user/profile', 'GET');
    },
    
    updateProfile: async (data) => {
        return apiRequest('/user/profile', 'PUT', data);
    }
};


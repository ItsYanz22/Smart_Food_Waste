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
        
        // Clone response for error handling
        const responseClone = response.clone();
        
        // Try to parse as JSON first
        let result;
        const contentType = response.headers.get('content-type') || '';
        
        if (contentType.includes('application/json')) {
            try {
                result = await response.json();
            } catch (jsonError) {
                // If JSON parsing fails, try text
                const text = await responseClone.text();
                throw new Error(text || `Server returned ${response.status} with invalid JSON`);
            }
        } else {
            // Non-JSON response
            const text = await response.text();
            if (!response.ok) {
                throw new Error(text || `Server returned ${response.status}`);
            }
            // Success with non-JSON - return text
            return { message: text };
        }
        
        // Check if response is OK
        if (!response.ok) {
            const errorMsg = result.error || result.message || `Request failed with status ${response.status}`;
            console.error('API Error:', {
                status: response.status,
                endpoint: endpoint,
                error: errorMsg,
                data: result
            });
            throw new Error(errorMsg);
        }
        
        return result;
    } catch (error) {
        // Network errors or fetch failures
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Failed to connect to server. Make sure the backend is running on http://localhost:5000');
        }
        // If it's already an Error with a message, pass it through
        if (error instanceof Error) {
            throw error;
        }
        // Otherwise, wrap it
        throw new Error(`Network error: ${error.message || 'Unknown error occurred'}`);
    }
}

/**
 * Auth API calls
 */
const authAPI = {
    register: async (username, email, password, householdSize) => {
        const data = {
            username: username ? username.trim() : '',
            email: email ? email.trim().toLowerCase() : '',
            password: password || '',
            household_size: householdSize ? String(householdSize).trim() : '1'
        };
        
        console.log('authAPI.register - Sending data:', {
            ...data,
            password: '***' // Don't log password
        });
        
        return apiRequest('/auth/register', 'POST', data);
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
    
    extractFromUrl: async (recipeUrl) => {
        return apiRequest('/dish/extract-url', 'POST', {
            recipe_url: recipeUrl
        });
    },
    
    getFavorites: async () => {
        return apiRequest('/dish/favorites', 'GET');
    },
    
    addFavorite: async (dishName) => {
        return apiRequest('/dish/favorites', 'POST', {
            dish_name: dishName
        });
    },
    
    downloadRecipePDF: async (recipeId) => {
        return apiRequest(`/dish/recipe/${recipeId}/pdf`, 'GET');
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


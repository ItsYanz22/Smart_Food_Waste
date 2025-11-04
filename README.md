# AI-Based Smart Food Waste Management

A smart waste management application that helps users track purchases and food ingredients based on daily routines, reducing food waste through AI-assisted grocery planning.

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [How Files Work Together](#how-files-work-together)
4. [Data Flow](#data-flow)
5. [File Relationships](#file-relationships)
6. [Setup Instructions](#setup-instructions)
7. [API Documentation](#api-documentation)

---

## Overview

This application helps users reduce food waste by:
- Taking dish name as input
- Automatically fetching recipe and ingredients
- Scaling quantities based on household size
- Generating organized grocery lists
- Storing data for future reuse

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                            │
│  (HTML/CSS/JS) - User Interface                            │
│  ├── index.html - Main UI structure                        │
│  ├── js/main.js - App initialization & event handlers      │
│  ├── js/api.js - API communication layer                   │
│  ├── js/ui.js - UI interaction functions                   │
│  └── js/utils.js - Helper utilities                        │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP Requests (REST API)
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                         BACKEND API                          │
│  (Flask/Python) - REST API Server                          │
│  ├── app.py - Flask app initialization & routing          │
│  ├── config.py - Configuration settings                    │
│  ├── routes/ - API endpoints                               │
│  │   ├── auth.py - Authentication                          │
│  │   ├── dish.py - Dish search & recipes                  │
│  │   ├── grocery.py - Grocery list management             │
│  │   └── user.py - User profile                           │
│  └── services/ - Business logic                            │
│      ├── recipe_service.py - Recipe fetching               │
│      ├── ingredient_extractor.py - Parse ingredients       │
│      ├── quantity_calculator.py - Scale quantities        │
│      ├── grocery_list_builder.py - Build lists            │
│      └── pdf_generator.py - Generate PDFs                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                         AI MODULE                            │
│  (NLP Processing)                                            │
│  ├── nlp_processor.py - Text normalization                 │
│  ├── dish_recognizer.py - Dish name recognition           │
│  └── query_processor.py - Search query building           │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                         DATABASE                             │
│  (MongoDB) - Data Storage                                    │
│  ├── models/ - Data models                                  │
│  │   ├── user.py - User accounts & preferences            │
│  │   ├── dish.py - Dish information                       │
│  │   ├── recipe.py - Recipe data                          │
│  │   ├── ingredient.py - Ingredient catalog               │
│  │   └── grocery_list.py - Saved grocery lists            │
│  └── External APIs (Google Search, Spoonacular)            │
└──────────────────────────────────────────────────────────────┘
```

---

## How Files Work Together

### 1. **Application Initialization Flow**

```
User opens browser → frontend/index.html loads
    ↓
frontend/js/main.js runs on DOMContentLoaded
    ↓
Checks authentication (getToken() from utils.js)
    ↓
If logged in → Shows app (app-section)
If not → Shows login form (auth-section)
```

### 2. **User Authentication Flow**

```
User fills login form → frontend/js/main.js handlesLogin()
    ↓
frontend/js/api.js → authAPI.login() sends POST to /api/auth/login
    ↓
backend/routes/auth.py → login() function
    ↓
backend/models/user.py → User.objects() queries MongoDB
    ↓
If valid → JWT token generated → Sent back to frontend
    ↓
frontend/js/utils.js → setToken() stores in localStorage
    ↓
User redirected to main app
```

### 3. **Dish Search & Recipe Fetching Flow**

```
User enters dish name → frontend/js/main.js handleDishSearch()
    ↓
frontend/js/api.js → dishAPI.search() sends POST to /api/dish/search
    ↓
backend/routes/dish.py → search_dish() function
    ↓
backend/ai_module/dish_recognizer.py → normalize_dish_name()
    ↓
Checks MongoDB (backend/models/dish.py) for existing dish
    ↓
If found → Returns cached recipe
If not found → backend/services/recipe_service.py → fetch_recipe()
    ↓
backend/ai_module/query_processor.py → build_search_query()
    ↓
Google Search API called → Recipe HTML fetched
    ↓
backend/services/ingredient_extractor.py → extract_from_html()
    ↓
Parses ingredients → Returns structured data
    ↓
Recipe saved to MongoDB (backend/models/recipe.py)
    ↓
Response sent back to frontend
    ↓
frontend/js/ui.js → displayRecipeResults() shows recipe
```

### 4. **Grocery List Generation Flow**

```
User clicks "Generate Grocery List" → frontend/js/ui.js generateGroceryList()
    ↓
frontend/js/api.js → groceryAPI.generate() sends POST to /api/grocery/generate
    ↓
backend/routes/grocery.py → generate_grocery_list()
    ↓
backend/services/quantity_calculator.py → scale_ingredients()
    │   - Takes recipe servings and household size
    │   - Calculates scaled quantities
    ↓
backend/services/grocery_list_builder.py → build_list()
    │   - Groups ingredients by category
    │   - Combines duplicates
    │   - Organizes by category order
    ↓
GroceryList saved to MongoDB (backend/models/grocery_list.py)
    ↓
backend/services/pdf_generator.py → generate_pdf()
    │   - Creates PDF using ReportLab
    │   - Saves to backend/static/pdfs/
    ↓
Response with grocery list and PDF URL sent to frontend
    ↓
frontend/js/ui.js → loadGroceryLists() displays list
```

---

## Data Flow

### Complete User Journey Example

```
1. USER REGISTRATION
   frontend/index.html (register form)
   → frontend/js/main.js (handleRegister)
   → frontend/js/api.js (authAPI.register)
   → backend/routes/auth.py (register)
   → backend/models/user.py (User document created)
   → MongoDB stores user data

2. DISH SEARCH
   frontend/index.html (search form)
   → frontend/js/main.js (handleDishSearch)
   → frontend/js/api.js (dishAPI.search)
   → backend/routes/dish.py (search_dish)
   → backend/ai_module/dish_recognizer.py (normalize)
   → backend/services/recipe_service.py (fetch_recipe)
   → backend/ai_module/query_processor.py (build query)
   → Google Search API (external)
   → backend/services/ingredient_extractor.py (parse)
   → backend/models/recipe.py (save recipe)
   → backend/models/dish.py (link dish to recipe)
   → Response back through chain
   → frontend/js/ui.js (displayRecipeResults)

3. GENERATE GROCERY LIST
   frontend/js/ui.js (generateGroceryList)
   → frontend/js/api.js (groceryAPI.generate)
   → backend/routes/grocery.py (generate_grocery_list)
   → backend/services/quantity_calculator.py (scale)
   → backend/services/grocery_list_builder.py (organize)
   → backend/models/grocery_list.py (save)
   → backend/services/pdf_generator.py (create PDF)
   → Response with PDF URL
   → frontend/js/ui.js (show success, load lists)
```

---

## File Relationships

### Backend Core Files

#### `backend/app.py`
- **Purpose**: Main Flask application entry point
- **Depends on**: `config.py`, all route files
- **Initializes**: Flask app, CORS, JWT, Rate Limiter
- **Registers**: Blueprints from `routes/` directory
- **Serves**: Static files from `backend/static/`

#### `backend/config.py`
- **Purpose**: Centralized configuration
- **Reads**: Environment variables from `.env`
- **Provides**: Configuration to all other backend files
- **Used by**: `app.py`, all route files, all services

### Models (Database Schema)

#### `backend/models/user.py`
- **Purpose**: User account and preferences
- **Relationships**: 
  - References in `grocery_list.py` (user_id)
  - Used by `routes/auth.py` and `routes/user.py`
- **Stores**: Username, email, household_size, favorites, dietary restrictions

#### `backend/models/dish.py`
- **Purpose**: Dish information
- **Relationships**: 
  - Links to `recipe.py` (recipe_id)
  - Used by `routes/dish.py`
- **Stores**: Dish name, normalized name, aliases, servings

#### `backend/models/recipe.py`
- **Purpose**: Recipe data with ingredients
- **Relationships**: 
  - Referenced by `dish.py` (recipe_id)
  - Used by `routes/dish.py` and `routes/grocery.py`
- **Stores**: Ingredients, instructions, servings, source URL

#### `backend/models/ingredient.py`
- **Purpose**: Ingredient catalog for categorization
- **Relationships**: 
  - Used by `services/ingredient_extractor.py`
- **Stores**: Name, synonyms, category, common units

#### `backend/models/grocery_list.py`
- **Purpose**: Saved grocery lists
- **Relationships**: 
  - References `user.py` (user_id)
  - Used by `routes/grocery.py`
- **Stores**: Items, household size, PDF URL, notes

### Routes (API Endpoints)

#### `backend/routes/auth.py`
- **Purpose**: Authentication endpoints
- **Depends on**: `models/user.py`, `utils/validators.py`
- **Endpoints**: `/api/auth/register`, `/api/auth/login`, `/api/auth/me`
- **Uses**: JWT for token generation

#### `backend/routes/dish.py`
- **Purpose**: Dish search and recipe fetching
- **Depends on**: 
  - `models/dish.py`, `models/recipe.py`
  - `services/recipe_service.py`
  - `ai_module/dish_recognizer.py`
- **Endpoints**: `/api/dish/search`, `/api/dish/favorites`

#### `backend/routes/grocery.py`
- **Purpose**: Grocery list management
- **Depends on**: 
  - `models/grocery_list.py`, `models/recipe.py`
  - `services/quantity_calculator.py`
  - `services/grocery_list_builder.py`
  - `services/pdf_generator.py`
- **Endpoints**: `/api/grocery/generate`, `/api/grocery/lists/*`

#### `backend/routes/user.py`
- **Purpose**: User profile management
- **Depends on**: `models/user.py`
- **Endpoints**: `/api/user/profile`

### Services (Business Logic)

#### `backend/services/recipe_service.py`
- **Purpose**: Fetch recipes from external APIs
- **Depends on**: 
  - `config.py` (API keys)
  - `services/ingredient_extractor.py`
- **Calls**: Google Search API, Spoonacular API (fallback)
- **Returns**: Structured recipe data

#### `backend/services/ingredient_extractor.py`
- **Purpose**: Parse ingredients from HTML/recipe text
- **Depends on**: BeautifulSoup for HTML parsing
- **Uses**: Regex patterns and NLP for extraction
- **Returns**: List of ingredient dictionaries

#### `backend/services/quantity_calculator.py`
- **Purpose**: Scale ingredient quantities based on household size
- **Input**: Ingredients list, recipe servings, household size
- **Logic**: Calculates scale factor, handles fractions, converts units
- **Returns**: Scaled ingredients list

#### `backend/services/grocery_list_builder.py`
- **Purpose**: Organize and categorize grocery items
- **Input**: Scaled ingredients list
- **Logic**: Groups by category, combines duplicates, sorts
- **Returns**: Organized grocery list

#### `backend/services/pdf_generator.py`
- **Purpose**: Generate PDF grocery lists
- **Depends on**: ReportLab library
- **Input**: GroceryList document
- **Output**: PDF file in `backend/static/pdfs/`
- **Returns**: PDF URL path

### AI/NLP Module

#### `ai_module/nlp_processor.py`
- **Purpose**: Text normalization and processing
- **Used by**: `dish_recognizer.py`, `query_processor.py`
- **Functions**: normalize_text(), tokenize(), extract_keywords()

#### `ai_module/dish_recognizer.py`
- **Purpose**: Recognize and normalize dish names
- **Depends on**: `nlp_processor.py`
- **Used by**: `routes/dish.py`
- **Functions**: normalize_dish_name(), find_similar_dishes()

#### `ai_module/query_processor.py`
- **Purpose**: Build optimized search queries
- **Depends on**: `nlp_processor.py`
- **Used by**: `services/recipe_service.py`
- **Functions**: build_search_query(), extract_dish_from_query()

### Frontend Files

#### `frontend/index.html`
- **Purpose**: Main HTML structure
- **Contains**: All UI elements (forms, sections, buttons)
- **Loads**: All JavaScript files at bottom

#### `frontend/js/main.js`
- **Purpose**: Application entry point and event handlers
- **Depends on**: `utils.js`, `api.js`, `ui.js`
- **Functions**: 
  - checkAuth() - Check if user is logged in
  - handleLogin() - Process login form
  - handleDishSearch() - Process dish search
  - handleProfileUpdate() - Update user profile

#### `frontend/js/api.js`
- **Purpose**: API communication layer
- **Functions**: 
  - apiRequest() - Generic API call function
  - authAPI - Authentication calls
  - dishAPI - Dish/recipe calls
  - groceryAPI - Grocery list calls
  - userAPI - User profile calls
- **Uses**: Fetch API for HTTP requests

#### `frontend/js/ui.js`
- **Purpose**: UI interaction and display functions
- **Depends on**: `api.js`, `utils.js`
- **Functions**: 
  - displayRecipeResults() - Show recipe
  - loadGroceryLists() - Display saved lists
  - generateGroceryList() - Trigger list generation
  - showSection() - Navigate between sections

#### `frontend/js/utils.js`
- **Purpose**: Utility functions
- **Functions**: 
  - getToken() / setToken() - JWT token management
  - getCurrentUser() / setCurrentUser() - User data
  - showError() / showSuccess() - Display messages
  - showLoading() / hideLoading() - Loading indicators

### Utilities

#### `backend/utils/validators.py`
- **Purpose**: Input validation
- **Used by**: `routes/auth.py`
- **Functions**: validate_email(), validate_password(), validate_dish_name()

#### `backend/utils/converters.py`
- **Purpose**: Unit conversion utilities
- **Used by**: `services/quantity_calculator.py`
- **Functions**: convert_unit(), normalize_unit()

### Database Scripts

#### `database/init_db.py`
- **Purpose**: Initialize MongoDB database
- **Connects**: To MongoDB using `config.py`
- **Creates**: Indexes for all models
- **Run**: Once during setup

#### `database/seed_data.py`
- **Purpose**: Seed database with initial data
- **Creates**: Common ingredients in `models/ingredient.py`
- **Run**: Once during setup

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- MongoDB (local or MongoDB Atlas)
- Google Search API key and Engine ID
- (Optional) Spoonacular API key

### Installation

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your API keys and MongoDB URI
   ```

4. **Initialize database**
   ```bash
   python database/init_db.py
   python database/seed_data.py
   ```

5. **Run the application**
   ```bash
   python backend/app.py
   ```

6. **Open frontend**
   - Open `frontend/index.html` in a web browser
   - Or serve it using a local server (e.g., `python -m http.server 8000` in frontend directory)

---

## API Documentation

### Authentication Endpoints

#### `POST /api/auth/register`
- **Purpose**: Register new user
- **Request Body**: `{username, email, password, household_size}`
- **Response**: `{access_token, user}`
- **Flow**: `routes/auth.py` → `models/user.py` → MongoDB

#### `POST /api/auth/login`
- **Purpose**: Login user
- **Request Body**: `{username, password}`
- **Response**: `{access_token, user}`
- **Flow**: `routes/auth.py` → `models/user.py` → JWT token generation

#### `GET /api/auth/me`
- **Purpose**: Get current user
- **Headers**: `Authorization: Bearer <token>`
- **Response**: User object
- **Flow**: `routes/auth.py` → JWT validation → `models/user.py`

### Dish & Recipe Endpoints

#### `POST /api/dish/search`
- **Purpose**: Search for dish and fetch recipe
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: `{dish_name}`
- **Response**: `{dish, recipe, from_cache}`
- **Flow**: 
  1. `routes/dish.py` → `dish_recognizer.py` (normalize)
  2. Check `models/dish.py` for cached recipe
  3. If not found → `recipe_service.py` → Google Search API
  4. `ingredient_extractor.py` → Parse ingredients
  5. Save to `models/recipe.py` and `models/dish.py`

#### `GET /api/dish/favorites`
- **Purpose**: Get user's favorite dishes
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{favorite_dishes}`
- **Flow**: `routes/dish.py` → `models/user.py` → `models/dish.py`

#### `POST /api/dish/favorites`
- **Purpose**: Add dish to favorites
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: `{dish_name}`
- **Response**: `{message, favorite_dishes}`
- **Flow**: `routes/dish.py` → `models/user.py` (update)

### Grocery List Endpoints

#### `POST /api/grocery/generate`
- **Purpose**: Generate grocery list
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: `{dish_name, household_size, recipe_id}`
- **Response**: `{grocery_list}`
- **Flow**: 
  1. `routes/grocery.py` → `models/recipe.py` (get recipe)
  2. `quantity_calculator.py` (scale ingredients)
  3. `grocery_list_builder.py` (organize)
  4. `models/grocery_list.py` (save)
  5. `pdf_generator.py` (create PDF)

#### `GET /api/grocery/lists`
- **Purpose**: Get all user's grocery lists
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{grocery_lists}`
- **Flow**: `routes/grocery.py` → `models/grocery_list.py`

#### `GET /api/grocery/lists/<id>/download/pdf`
- **Purpose**: Download grocery list as PDF
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{pdf_url}`
- **Flow**: `routes/grocery.py` → `pdf_generator.py` → `static/pdfs/`

#### `GET /api/grocery/lists/<id>/download/csv`
- **Purpose**: Download grocery list as CSV
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{csv_data}`
- **Flow**: `routes/grocery.py` → Format CSV data

### User Profile Endpoints

#### `GET /api/user/profile`
- **Purpose**: Get user profile
- **Headers**: `Authorization: Bearer <token>`
- **Response**: User object
- **Flow**: `routes/user.py` → `models/user.py`

#### `PUT /api/user/profile`
- **Purpose**: Update user profile
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: `{household_size, dietary_restrictions, ...}`
- **Response**: `{user}`
- **Flow**: `routes/user.py` → `models/user.py` (update)

---

## Key Concepts

### Authentication Flow
1. User registers/logs in → JWT token generated
2. Token stored in localStorage (frontend)
3. Token sent in `Authorization` header for all API calls
4. Backend validates token using `@jwt_required()` decorator

### Caching Strategy
1. First search for dish → Fetch from Google Search API
2. Recipe saved to MongoDB
3. Subsequent searches → Return cached recipe from database
4. Reduces API calls and improves performance

### Quantity Scaling
1. Recipe has default servings (e.g., 4 people)
2. User enters household size (e.g., 2 people)
3. Scale factor = household_size / recipe_servings (2/4 = 0.5)
4. All ingredient quantities multiplied by scale factor
5. Handles fractions (1/2 cup → 1/4 cup for 2 people)

### Ingredient Categorization
1. Ingredients extracted from recipe
2. Categorized using keyword matching (meat, dairy, produce, etc.)
3. Grouped by category in grocery list
4. Makes shopping easier (all produce together)

---

## Team

- **Team Leader**: Priyanshu Sahoo
- **Team Members**: 
  - Kshitij Chandel
  - Soumyadeep Banik
  - Hariom Singh

---

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed (`pip install -r requirements.txt`)
2. **MongoDB connection**: Check `MONGO_URI` in `.env` file
3. **API errors**: Verify Google Search API key and Engine ID
4. **CORS errors**: Check `CORS_ORIGINS` in `config.py`
5. **PDF generation**: Ensure `static/pdfs/` directory exists and is writable

---

## Next Steps

1. Add more error handling
2. Implement unit tests
3. Add more recipe sources
4. Enhance AI/NLP processing
5. Add mobile app support
6. Implement IoT sensor integration (future)

---

This documentation explains how all files work together in the AI-Based Smart Food Waste Management system. Each component has a specific role and communicates with others through well-defined interfaces, creating a cohesive and functional application.

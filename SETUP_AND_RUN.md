# Setup and Run Guide - AI-Based Smart Food Waste Management

This guide will help you set up, run, and test the application step by step.

---

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.10 or higher** installed
   - Check: `python --version` or `python3 --version`
   - Download: https://www.python.org/downloads/

2. **MongoDB** installed and running
   - Local MongoDB: https://www.mongodb.com/try/download/community
   - OR MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas
   - Check: `mongod --version`

3. **Google Search API Key** (required)
   - Get it from: https://developers.google.com/custom-search/v1/overview
   - You'll need:
     - API Key
     - Search Engine ID

4. **Spoonacular API Key** (optional, for backup)
   - Get it from: https://spoonacular.com/food-api

---

## Step 1: Set Up Project Directory

1. **Navigate to project directory**
   ```bash
   cd "F:\Code Playground\NitA"
   ```

2. **Verify project structure**
   ```
   You should see:
   - backend/
   - frontend/
   - ai_module/
   - database/
   - README.md
   ```

---

## Step 2: Create Virtual Environment

1. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **On Mac/Linux:**
   ```bash
   source venv/bin/activate
   ```

3. **Verify activation** (you should see `(venv)` in your terminal)
   ```bash
   # Your prompt should now show: (venv) F:\Code Playground\NitA>
   ```

---

## Step 3: Install Dependencies

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   pip list
   # You should see Flask, mongoengine, requests, etc.
   ```

---

## Step 4: Set Up MongoDB

### Option A: Local MongoDB

1. **Start MongoDB service**
   
   **On Windows:**
   ```bash
   # Usually MongoDB starts automatically as a service
   # If not, run: net start MongoDB
   ```
   
   **On Mac/Linux:**
   ```bash
   sudo systemctl start mongod
   # OR
   mongod --dbpath /path/to/data
   ```

2. **Verify MongoDB is running**
   ```bash
   mongosh
   # Should connect to MongoDB shell
   # Type: exit
   ```

3. **MongoDB URI**: `mongodb://localhost:27017/smart_waste_db`

### Option B: MongoDB Atlas (Cloud)

1. **Create account**: https://www.mongodb.com/cloud/atlas

2. **Create cluster** (free tier available)

3. **Get connection string**
   - Go to: Connect → Connect your application
   - Copy connection string
   - Format: `mongodb+srv://username:password@cluster.mongodb.net/smart_waste_db`

---

## Step 5: Configure Environment Variables

1. **Create `.env` file in backend directory**
   ```bash
   cd backend
   # Create .env file (copy from example below)
   ```

2. **Edit `.env` file** with your configuration:

   ```env
   # Flask Configuration
   SECRET_KEY=your-secret-key-change-this-in-production-12345
   JWT_SECRET_KEY=your-jwt-secret-key-change-this-67890

   # MongoDB Configuration
   # Option A: Local MongoDB
   MONGO_URI=mongodb://localhost:27017/smart_waste_db
   
   # Option B: MongoDB Atlas (replace with your connection string)
   # MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/smart_waste_db

   # Google Search API Configuration
   GOOGLE_SEARCH_API_KEY=your-google-search-api-key-here
   GOOGLE_SEARCH_ENGINE_ID=your-google-search-engine-id-here

   # Spoonacular API (Optional - Backup)
   SPOONACULAR_API_KEY=your-spoonacular-api-key-here

   # CORS Configuration (for frontend)
   CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
   ```

3. **Get Google Search API Key**:
   - Go to: https://console.cloud.google.com/
   - Create new project or select existing
   - Enable "Custom Search API"
   - Go to: APIs & Services → Credentials
   - Create API Key
   - Create Custom Search Engine: https://programmablesearchengine.google.com/
   - Get Search Engine ID

---

## Step 6: Initialize Database

1. **Run database initialization**
   ```bash
   # From project root directory
   python database/init_db.py
   ```

   Expected output:
   ```
   Connecting to MongoDB...
   Connected to MongoDB successfully!
   Creating indexes...
   ✓ User indexes created
   ✓ Dish indexes created
   ✓ Recipe indexes created
   ✓ Ingredient indexes created
   ✓ Grocery list indexes created
   
   Database initialization complete!
   ```

2. **Seed initial data**
   ```bash
   python database/seed_data.py
   ```

   Expected output:
   ```
   Connecting to MongoDB...
   Connected!
   
   Seeding ingredients...
     ✓ Created ingredient: Tomato
     ✓ Created ingredient: Onion
     ...
   ✓ Ingredients seeding complete!
   
   Database seeding complete!
   ```

---

## Step 7: Start the Backend Server

1. **Navigate to backend directory** (if not already there)
   ```bash
   cd backend
   ```

2. **Run Flask application**
   ```bash
   python app.py
   ```

   Expected output:
   ```
   * Running on http://0.0.0.0:5000
   * Debug mode: on
   ```

3. **Verify server is running**
   - Open browser: http://localhost:5000
   - You should see: `{"status": "healthy", "message": "AI-Based Smart Food Waste Management API", "version": "1.0.0"}`
   - Or test: http://localhost:5000/api/health

4. **Keep this terminal open** - server must keep running

---

## Step 8: Start the Frontend

### Option A: Using Python HTTP Server (Recommended)

1. **Open a NEW terminal window** (keep backend running in first terminal)

2. **Navigate to frontend directory**
   ```bash
   cd "F:\Code Playground\NitA\frontend"
   ```

3. **Start HTTP server**
   ```bash
   python -m http.server 8000
   ```

4. **Open browser**
   - Go to: http://localhost:8000
   - You should see the application interface

### Option B: Direct File Opening

1. **Navigate to frontend directory**
   ```bash
   cd "F:\Code Playground\NitA\frontend"
   ```

2. **Open index.html**
   - Right-click `index.html` → Open with → Your browser
   - Note: Some features may not work due to CORS if opened directly

---

## Step 9: Test the Application

### Test 1: Health Check

1. **Backend API**
   - Open: http://localhost:5000/api/health
   - Should return: `{"status": "healthy", "api": "running"}`

### Test 2: User Registration

1. **Open frontend**: http://localhost:8000

2. **Click "Register" tab**

3. **Fill form:**
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `test123`
   - Household Size: `2`

4. **Click "Register"**

5. **Expected**: 
   - Success message
   - Automatically logged in
   - Shows main app interface

### Test 3: Search for a Dish

1. **Make sure you're logged in**

2. **In "Search Dish" section:**
   - Enter dish name: `Biryani` or `Pasta` or `Curry`
   - Click "Search Recipe"

3. **Expected**:
   - Loading indicator appears
   - Recipe found with ingredients list
   - Shows servings information

### Test 4: Generate Grocery List

1. **After recipe is found:**
   - Enter household size (e.g., `2`)
   - Click "Generate Grocery List"

2. **Expected**:
   - Success message
   - Navigates to "My Lists" section
   - Shows generated grocery list

### Test 5: Download PDF

1. **In "My Lists" section:**
   - Click "Download PDF" on any grocery list

2. **Expected**:
   - PDF opens in new tab/downloads
   - Contains formatted grocery list

### Test 6: View Profile

1. **Click "Profile" tab**

2. **Expected**:
   - Shows current household size
   - Shows favorite dishes (if any)
   - Can update profile

---

## Step 10: Test API Directly (Using Postman/curl)

### Test Authentication

```bash
# Register User
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2",
    "email": "test2@example.com",
    "password": "test123",
    "household_size": "2"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2",
    "password": "test123"
  }'

# Save the access_token from response
```

### Test Dish Search

```bash
# Replace YOUR_TOKEN with actual token from login
curl -X POST http://localhost:5000/api/dish/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "dish_name": "Biryani"
  }'
```

### Test Grocery List Generation

```bash
# Replace YOUR_TOKEN and RECIPE_ID with actual values
curl -X POST http://localhost:5000/api/grocery/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "dish_name": "Biryani",
    "household_size": "4",
    "recipe_id": "RECIPE_ID"
  }'
```

---

## Troubleshooting

### Issue 1: "Module not found" errors

**Solution:**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Issue 2: MongoDB connection error

**Error:** `pymongo.errors.ServerSelectionTimeoutError`

**Solutions:**
- Check MongoDB is running: `mongosh` should connect
- Verify MONGO_URI in `.env` file
- For Atlas: Check IP whitelist and credentials

### Issue 3: Flask app won't start

**Error:** `Port 5000 already in use`

**Solution:**
```bash
# Change port in app.py
# OR kill process using port 5000
# Windows: netstat -ano | findstr :5000
# Then: taskkill /PID <PID> /F
```

### Issue 4: CORS errors in browser

**Error:** `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution:**
- Check `CORS_ORIGINS` in `.env` includes your frontend URL
- Restart Flask server after changing `.env`

### Issue 5: Google Search API errors

**Error:** `403 Forbidden` or `Invalid API key`

**Solution:**
- Verify API key in `.env` file
- Check API key is enabled in Google Cloud Console
- Verify Search Engine ID is correct
- Check API quota/limits

### Issue 6: Recipe not found

**Error:** "Recipe not found. Please try a different dish name."

**Possible causes:**
- Google Search API quota exceeded
- Dish name too obscure
- Internet connection issue

**Solution:**
- Try common dish names: "Pasta", "Biryani", "Pizza"
- Check API quota in Google Cloud Console
- Verify internet connection

### Issue 7: PDF generation fails

**Error:** `Permission denied` or PDF not created

**Solution:**
```bash
# Create static/pdfs directory manually
mkdir -p backend/static/pdfs
# On Windows: mkdir backend\static\pdfs
```

### Issue 8: Frontend can't connect to backend

**Error:** `Failed to fetch` or network error

**Solution:**
- Verify backend is running on port 5000
- Check `API_BASE_URL` in `frontend/js/api.js` (should be `http://localhost:5000/api`)
- Make sure CORS is configured correctly

---

## Quick Start Checklist

- [ ] Python 3.10+ installed
- [ ] MongoDB installed and running
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with API keys
- [ ] Database initialized (`python database/init_db.py`)
- [ ] Database seeded (`python database/seed_data.py`)
- [ ] Backend server running (`python backend/app.py`)
- [ ] Frontend server running (`python -m http.server 8000`)
- [ ] Tested registration and login
- [ ] Tested dish search
- [ ] Tested grocery list generation

---

## Development Tips

1. **Keep both terminals open:**
   - Terminal 1: Backend server (`python backend/app.py`)
   - Terminal 2: Frontend server (`python -m http.server 8000`)

2. **Monitor logs:**
   - Backend logs show in Terminal 1
   - Check browser console (F12) for frontend errors

3. **Hot reload:**
   - Flask auto-reloads on code changes
   - Refresh browser to see frontend changes

4. **Database inspection:**
   ```bash
   mongosh
   use smart_waste_db
   show collections
   db.users.find()
   db.recipes.find()
   ```

---

## Next Steps

Once everything is running:

1. **Test all features** systematically
2. **Add more recipes** by searching different dishes
3. **Generate multiple grocery lists**
4. **Test PDF and CSV downloads**
5. **Explore the code** to understand the flow

---

## Need Help?

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Verify all **prerequisites** are installed
3. Check **logs** in terminal and browser console
4. Verify **environment variables** in `.env`
5. Ensure **MongoDB is running** and accessible
6. Verify **API keys** are valid and have quota

---

**Happy coding! 🚀**


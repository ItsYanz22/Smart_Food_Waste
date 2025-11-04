# 🚀 How to Run and Test the Application

## Prerequisites Checklist

Before starting, make sure you have:
- ✅ Python 3.10+ installed
- ✅ MongoDB installed (local or Atlas account)
- ✅ Google Search API Key (get from Google Cloud Console)
- ✅ Google Search Engine ID (get from Google Programmable Search Engine)

---

## Step-by-Step Instructions

### STEP 1: Open Terminal/Command Prompt

Navigate to your project:
```bash
cd "F:\Code Playground\NitA"
```

### STEP 2: Create Virtual Environment

```bash
python -m venv venv
```

**Activate it:**
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

You should see `(venv)` in your terminal prompt.

### STEP 3: Install Python Packages

```bash
cd backend
pip install -r requirements.txt
```

Wait for installation to complete.

### STEP 4: Create Environment File

1. **Create `.env` file** in `backend/` directory

2. **Copy this template** and fill in your values:

```env
SECRET_KEY=change-this-to-random-string-12345
JWT_SECRET_KEY=change-this-to-random-string-67890
MONGO_URI=mongodb://localhost:27017/smart_waste_db
GOOGLE_SEARCH_API_KEY=YOUR_API_KEY_HERE
GOOGLE_SEARCH_ENGINE_ID=YOUR_ENGINE_ID_HERE
SPOONACULAR_API_KEY=optional-backup-key
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

**How to get API keys:**
- Google Search API: https://console.cloud.google.com/
- Search Engine ID: https://programmablesearchengine.google.com/

### STEP 5: Start MongoDB

**Option A - Local MongoDB:**
```bash
# Make sure MongoDB service is running
mongosh  # Test connection
```

**Option B - MongoDB Atlas (Cloud):**
- Create free account: https://www.mongodb.com/cloud/atlas
- Get connection string
- Update `MONGO_URI` in `.env` file

### STEP 6: Initialize Database

**Open a NEW terminal** (keep virtual environment activated):

```bash
cd "F:\Code Playground\NitA"
python database/init_db.py
python database/seed_data.py
```

You should see success messages.

### STEP 7: Start Backend Server

**In the same terminal:**
```bash
cd backend
python app.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

**✅ Keep this terminal open!**

### STEP 8: Start Frontend Server

**Open ANOTHER NEW terminal:**

```bash
cd "F:\Code Playground\NitA\frontend"
python -m http.server 8000
```

**Expected output:**
```
Serving HTTP on 0.0.0.0 port 8000
```

**✅ Keep this terminal open too!**

### STEP 9: Open in Browser

1. Open your web browser
2. Go to: **http://localhost:8000**
3. You should see the application!

---

## Testing the Application

### Test 1: Register a User

1. Click **"Register"** tab
2. Fill in:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `test123`
   - Household Size: `2`
3. Click **"Register"**
4. ✅ Should automatically log you in

### Test 2: Search for a Dish

1. You should be on the **"Search Dish"** section
2. Enter dish name: `Biryani` (or `Pasta`, `Curry`, `Pizza`)
3. Click **"Search Recipe"**
4. ✅ Should show recipe with ingredients list

### Test 3: Generate Grocery List

1. After recipe is shown, enter household size: `2`
2. Click **"Generate Grocery List"**
3. ✅ Should navigate to "My Lists" and show your grocery list

### Test 4: Download PDF

1. In "My Lists" section
2. Click **"Download PDF"** button
3. ✅ PDF should open/download

### Test 5: Check Profile

1. Click **"Profile"** tab
2. ✅ Should show your household size and preferences

---

## Quick API Test (Using Browser)

Open these URLs in browser to test backend:

1. **Health Check:**
   - http://localhost:5000/api/health
   - Should show: `{"status": "healthy", "api": "running"}`

2. **Root:**
   - http://localhost:5000/
   - Should show API info

---

## Troubleshooting

### ❌ "Module not found" error
**Fix:** Make sure virtual environment is activated and run:
```bash
pip install -r backend/requirements.txt
```

### ❌ "MongoDB connection failed"
**Fix:** 
- Check MongoDB is running: `mongosh`
- Verify `MONGO_URI` in `.env` file
- For Atlas: Check connection string and IP whitelist

### ❌ "Port 5000 already in use"
**Fix:** 
- Close other applications using port 5000
- OR change port in `backend/app.py` line 77:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
  ```

### ❌ "CORS error" in browser
**Fix:**
- Check `CORS_ORIGINS` in `.env` includes `http://localhost:8000`
- Restart Flask server after changing `.env`

### ❌ "Recipe not found"
**Fix:**
- Try common dish names: "Pasta", "Pizza", "Biryani"
- Check Google Search API key is correct
- Check API quota in Google Cloud Console

### ❌ Frontend shows "Failed to fetch"
**Fix:**
- Make sure backend is running on port 5000
- Check browser console (F12) for errors
- Verify `API_BASE_URL` in `frontend/js/api.js` is `http://localhost:5000/api`

---

## Terminal Commands Cheat Sheet

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r backend/requirements.txt

# Initialize database
python database/init_db.py
python database/seed_data.py

# Run backend
cd backend
python app.py

# Run frontend (in separate terminal)
cd frontend
python -m http.server 8000

# Check MongoDB
mongosh
use smart_waste_db
show collections
```

---

## What Should Be Running

When everything is set up correctly, you should have:

1. **Terminal 1:** Backend Flask server running (port 5000)
2. **Terminal 2:** Frontend HTTP server running (port 8000)
3. **Browser:** Application open at http://localhost:8000
4. **MongoDB:** Running locally or connected to Atlas

---

## Next Steps

Once everything is working:

1. ✅ Test all features
2. ✅ Try different dish names
3. ✅ Generate multiple grocery lists
4. ✅ Test PDF downloads
5. ✅ Explore the code to understand how it works

---

## Need More Help?

- **Detailed Setup:** See `SETUP_AND_RUN.md`
- **Quick Reference:** See `QUICK_START.md`
- **How It Works:** See `README.md`

---

**🎉 You're all set! Happy coding!**


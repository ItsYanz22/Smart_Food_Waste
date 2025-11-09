# 🚀 How to Start and Run the Application

## Quick Start Guide

### Step 1: Start MongoDB

**Make sure MongoDB is running:**

**Windows:**
```bash
# Check if MongoDB service is running
net start MongoDB

# OR start it manually
"C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath "C:\data\db"
```

**Test connection:**
```bash
mongosh
# Should connect successfully, type 'exit' to leave
```

### Step 2: Start Backend Server

**Open Terminal 1:**

```bash
# Navigate to project
cd "F:\Code Playground\NitA"

# Activate virtual environment
venv\Scripts\activate

# Go to backend directory
cd backend

# Start the server
python app.py
```

**Expected output:**
```
✓ MongoDB connected successfully
✓ All routes registered successfully
==================================================
Starting AI-Based Smart Food Waste Management API
==================================================
Running from: F:\Code Playground\NitA\backend
Server listening on: 0.0.0.0:5000 (all interfaces)
🌐 Access in browser: http://localhost:5000
📡 API endpoint: http://localhost:5000/api
❤️  Health check: http://localhost:5000/api/health
🔧 CORS enabled for: http://localhost:8000
Debug mode: ON
==================================================

 * Running on http://0.0.0.0:5000
 * Debugger is active!
```

**✅ Keep this terminal open!**

### Step 3: Start Frontend Server

**Open Terminal 2 (NEW terminal):**

**Option A: Using Python HTTP Server (Recommended)**
```bash
# Navigate to frontend
cd "F:\Code Playground\NitA\frontend"

# Start server on port 8000
python -m http.server 8000
```

**Option B: Using VS Code Live Server (if you have it)**
- Right-click on `frontend/index.html`
- Select "Open with Live Server"
- Usually runs on port 5500

**Expected output:**
```
Serving HTTP on 0.0.0.0 port 8000
```

**✅ Keep this terminal open too!**

### Step 4: Open in Browser

**Open your web browser and go to:**

- **If using Python server:** http://localhost:8000
- **If using Live Server:** http://127.0.0.1:5500 (or check the port shown)

---

## ✅ Verify Everything is Working

### Test 1: Backend Health Check
Open: http://localhost:5000/api/health

Should show: `{"status": "healthy", "api": "running"}`

### Test 2: Frontend Loads
- Open frontend URL
- Should see the registration/login page
- No CORS errors in console (F12)

### Test 3: Register a User
1. Click "Register" tab
2. Fill in:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `test123`
   - Household Size: `2`
3. Click "Register"
4. Should see success message and be logged in

---

## 🔧 Troubleshooting

### CORS Error Still Appears?

**If frontend is on port 5500 (Live Server):**
- I've already updated CORS to allow port 5500
- **Restart backend** for changes to take effect

**If frontend is on different port:**
- Update `backend/app.py` line 28-30
- Add your port to the `origins` list

### Backend Won't Start?

1. **Check MongoDB is running:**
   ```bash
   mongosh
   ```

2. **Check port 5000 is free:**
   ```bash
   netstat -ano | findstr :5000
   ```

3. **Check dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

### Frontend Can't Connect?

1. **Check backend is running:**
   - Open: http://localhost:5000/api/health

2. **Check API URL in frontend:**
   - Open `frontend/js/api.js`
   - Line 5 should be: `const API_BASE_URL = 'http://localhost:5000/api';`

3. **Check browser console (F12):**
   - Look for specific error messages

---

## 📝 Complete Startup Checklist

- [ ] MongoDB service is running
- [ ] Virtual environment is activated (`venv` in prompt)
- [ ] Backend server is running (Terminal 1)
- [ ] Frontend server is running (Terminal 2)
- [ ] Browser is open at frontend URL
- [ ] No CORS errors in console
- [ ] Can register/login successfully

---

## 🎯 Quick Commands Reference

**Terminal 1 - Backend:**
```bash
cd "F:\Code Playground\NitA"
venv\Scripts\activate
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd "F:\Code Playground\NitA\frontend"
python -m http.server 8000
```

**Browser:**
- http://localhost:8000 (Python server)
- OR http://127.0.0.1:5500 (Live Server)

---

## 🎉 You're All Set!

Once both servers are running:
1. ✅ Backend on port 5000
2. ✅ Frontend on port 8000 (or 5500)
3. ✅ MongoDB running
4. ✅ Browser open

**You can now use the application!** 🚀

Try registering a user and searching for a dish!


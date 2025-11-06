# 🗄️ MongoDB Setup - Quick Guide

## Step 1: Start MongoDB Service

### On Windows:

**Option A: Using Services (Easiest)**
1. Press `Win + R`
2. Type `services.msc` and press Enter
3. Find "MongoDB" service
4. Right-click → Start (if not running)
5. Set to "Automatic" (so it starts on boot)

**Option B: Using Command Line**
```bash
# Open PowerShell/CMD as Administrator
net start MongoDB
```

**Option C: Manual Start (if service doesn't exist)**
```bash
# Create data directory first
mkdir C:\data\db

# Start MongoDB (adjust path if different)
"C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath "C:\data\db"
```

### Step 2: Verify MongoDB is Running

**Test connection:**
```bash
# Try to connect (if mongosh is in PATH)
mongosh

# OR use full path
"C:\Program Files\MongoDB\Server\7.0\bin\mongosh.exe"
```

If it connects, type `exit` to leave.

### Step 3: Configure Your App

**Check `backend/.env` file exists and has:**
```env
MONGO_URI=mongodb://localhost:27017/smart_waste_db
```

**If `.env` doesn't exist, create it:**
```bash
cd backend
# Create .env file with above content
```

### Step 4: Test Connection from Python

**Activate virtual environment first:**
```bash
cd "F:\Code Playground\NitA"
venv\Scripts\activate
```

**Then test:**
```bash
python database/setup_mongodb.py
```

This will test the connection and show any errors.

### Step 5: Initialize Database

**Once connection works:**
```bash
python database/init_db.py
python database/seed_data.py
```

---

## ✅ Quick Test

**Run this to test everything:**
```bash
cd "F:\Code Playground\NitA"
venv\Scripts\activate
python database/setup_mongodb.py
```

**Expected output:**
```
✓ MongoDB connection successful!
✓ Database write test successful!
✓ Database delete test successful!
✅ MongoDB is working correctly!
```

---

## 🔧 Common Issues

### "MongoDB service not found"
- MongoDB might not be installed as a service
- Use Option C above to start manually
- Or reinstall MongoDB with service option

### "Connection refused"
- MongoDB service not running
- Start it using `net start MongoDB` or Services

### "Port 27017 already in use"
- Another MongoDB instance running
- Kill it or use different port

---

## 🚀 After MongoDB Works

1. ✅ Test: `python database/setup_mongodb.py`
2. ✅ Initialize: `python database/init_db.py`
3. ✅ Seed data: `python database/seed_data.py`
4. ✅ Start backend: `cd backend && python app.py`
5. ✅ Start frontend: `cd frontend && python -m http.server 8000`
6. ✅ Open: http://localhost:8000

**Everything should work now!** 🎉



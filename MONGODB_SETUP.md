# 🗄️ MongoDB Setup Guide

## ✅ You've Installed MongoDB - Now Let's Configure It!

### Step 1: Start MongoDB Service

**On Windows:**

1. **Check if MongoDB service is running:**
   ```bash
   # Open PowerShell/CMD as Administrator
   net start MongoDB
   ```

2. **Or check Services:**
   - Press `Win + R`
   - Type `services.msc`
   - Look for "MongoDB" service
   - Make sure it's "Running"

3. **If service doesn't exist, start MongoDB manually:**
   ```bash
   # Navigate to MongoDB bin directory (usually)
   cd "C:\Program Files\MongoDB\Server\7.0\bin"
   mongod --dbpath "C:\data\db"
   ```
   (Create `C:\data\db` folder first if it doesn't exist)

### Step 2: Test MongoDB Connection

**Test MongoDB is working:**
```bash
mongosh
```

You should see:
```
Current Mongosh Log ID: ...
Connecting to: mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000
```

Type `exit` to leave MongoDB shell.

### Step 3: Configure Your App

**Check your `.env` file in `backend/` directory:**

```env
MONGO_URI=mongodb://localhost:27017/smart_waste_db
```

This is the default - it should work if MongoDB is running locally.

### Step 4: Test Connection from Python

**Run the test script:**
```bash
cd "F:\Code Playground\NitA"
python database/setup_mongodb.py
```

This will:
- Test MongoDB connection
- Create a test document
- Verify read/write operations
- Show any errors if connection fails

### Step 5: Initialize Database

**Once connection works, initialize the database:**
```bash
python database/init_db.py
python database/seed_data.py
```

---

## 🔧 Troubleshooting

### Issue: "MongoDB service not found"

**Solution:**
1. Make sure MongoDB is installed correctly
2. Check installation path: Usually `C:\Program Files\MongoDB\`
3. Start MongoDB manually:
   ```bash
   "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath "C:\data\db"
   ```

### Issue: "Connection refused"

**Solution:**
1. MongoDB service is not running
2. Start it: `net start MongoDB`
3. Or check firewall isn't blocking port 27017

### Issue: "Authentication failed"

**Solution:**
- If using local MongoDB (default), no authentication needed
- If using MongoDB Atlas, check username/password in connection string

### Issue: "Port 27017 already in use"

**Solution:**
- Another MongoDB instance is running
- Kill it or use a different port

---

## ✅ Quick Setup Checklist

- [ ] MongoDB installed
- [ ] MongoDB service running (or started manually)
- [ ] `mongosh` command works
- [ ] `.env` file has correct `MONGO_URI`
- [ ] Connection test passes (`python database/setup_mongodb.py`)
- [ ] Database initialized (`python database/init_db.py`)
- [ ] Database seeded (`python database/seed_data.py`)

---

## 🚀 Once MongoDB is Working

1. **Test connection:**
   ```bash
   python database/setup_mongodb.py
   ```

2. **Initialize database:**
   ```bash
   python database/init_db.py
   python database/seed_data.py
   ```

3. **Start your backend:**
   ```bash
   cd backend
   python app.py
   ```

4. **Everything should work now!** 🎉

---

## 📝 MongoDB Atlas (Cloud) Alternative

If you prefer cloud MongoDB:

1. Create account: https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Update `.env`:
   ```env
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/smart_waste_db
   ```

---

**After MongoDB is set up, your app should work perfectly!** 🎯



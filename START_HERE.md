# 🚀 START HERE - How to Run the App

## ⚡ Quick Start (3 Steps)

### 1️⃣ Start MongoDB
```bash
# Windows - Start MongoDB service
net start MongoDB

# Test it works
mongosh
# Type 'exit' when done
```

### 2️⃣ Start Backend (Terminal 1)
```bash
cd "F:\Code Playground\NitA"
venv\Scripts\activate
cd backend
python app.py
```

**Wait for:** `* Running on http://0.0.0.0:5000`

### 3️⃣ Start Frontend (Terminal 2 - NEW)
```bash
cd "F:\Code Playground\NitA\frontend"
python -m http.server 8000
```

**Wait for:** `Serving HTTP on 0.0.0.0 port 8000`

### 4️⃣ Open Browser
Go to: **http://localhost:8000**

---

## ✅ Test It Works

1. **Backend:** http://localhost:5000/api/health → Should show JSON
2. **Frontend:** http://localhost:8000 → Should show registration page
3. **Register:** Fill form → Click Register → Should work!

---

## 🐛 Common Issues

**CORS Error?**
- Make sure backend is running
- Restart backend after any code changes
- Check frontend is on allowed port (8000 or 5500)

**MongoDB Error?**
- Make sure MongoDB service is running
- Check `backend/.env` has correct `MONGO_URI`

**Port Already in Use?**
- Kill the process or use different port
- Change port in `app.py` line 131

---

**That's it! Both servers must be running at the same time!** 🎯


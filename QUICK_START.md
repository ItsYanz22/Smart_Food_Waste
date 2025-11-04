# Quick Start Guide - 5 Minutes to Running

## ⚡ Fast Setup

### 1. Install Dependencies
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install packages
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy example env file
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux

# Edit .env file with your:
# - MongoDB URI (local or Atlas)
# - Google Search API Key
# - Google Search Engine ID
```

### 3. Start MongoDB
```bash
# Local: Make sure MongoDB is running
mongosh  # Should connect

# OR use MongoDB Atlas (cloud)
# Just update MONGO_URI in .env
```

### 4. Initialize Database
```bash
# From project root
python database/init_db.py
python database/seed_data.py
```

### 5. Run Application

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python -m http.server 8000
```

### 6. Open Browser
- Go to: http://localhost:8000
- Register a new user
- Search for a dish (e.g., "Biryani")
- Generate grocery list!

---

## 🔧 Get API Keys

### Google Search API (Required)
1. Go to: https://console.cloud.google.com/
2. Create project → Enable "Custom Search API"
3. Create API Key
4. Create Search Engine: https://programmablesearchengine.google.com/
5. Get Search Engine ID

### MongoDB
- **Local**: Install from https://www.mongodb.com/try/download/community
- **Cloud**: Free tier at https://www.mongodb.com/cloud/atlas

---

## ✅ Test Checklist

- [ ] Backend running on http://localhost:5000
- [ ] Frontend running on http://localhost:8000
- [ ] Can register new user
- [ ] Can search for dish
- [ ] Can generate grocery list
- [ ] Can download PDF

---

## 🐛 Common Issues

**Port 5000 in use?**
```bash
# Change port in backend/app.py line 77
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

**MongoDB not connecting?**
- Check MongoDB is running: `mongosh`
- Verify MONGO_URI in `.env`

**API errors?**
- Verify API keys in `.env`
- Check Google Search API quota

For detailed setup, see **SETUP_AND_RUN.md**


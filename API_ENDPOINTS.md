# 📡 API Endpoints Reference

## Available Endpoints

### Health Check Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint - API info |
| GET | `/api/health` | Health check |

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login user | No |
| GET | `/api/auth/me` | Get current user | Yes |

### Dish & Recipe Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/dish/search` | Search for dish and fetch recipe | Yes |
| GET | `/api/dish/favorites` | Get favorite dishes | Yes |
| POST | `/api/dish/favorites` | Add dish to favorites | Yes |

### Grocery List Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/grocery/generate` | Generate grocery list | Yes |
| GET | `/api/grocery/lists` | Get all grocery lists | Yes |
| GET | `/api/grocery/lists/<id>` | Get specific grocery list | Yes |
| PUT | `/api/grocery/lists/<id>` | Update grocery list | Yes |
| DELETE | `/api/grocery/lists/<id>` | Delete grocery list | Yes |
| GET | `/api/grocery/lists/<id>/download/pdf` | Download PDF | Yes |
| GET | `/api/grocery/lists/<id>/download/csv` | Download CSV | Yes |

### User Profile Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/user/profile` | Get user profile | Yes |
| PUT | `/api/user/profile` | Update user profile | Yes |

---

## 🧪 Testing Endpoints

### Test 1: Root Endpoint
```
URL: http://localhost:5000/
Method: GET
Expected: {"status": "healthy", "message": "...", "version": "1.0.0"}
```

### Test 2: Health Check
```
URL: http://localhost:5000/api/health
Method: GET
Expected: {"status": "healthy", "api": "running"}
```

### Test 3: Register User
```
URL: http://localhost:5000/api/auth/register
Method: POST
Body: {
  "username": "testuser",
  "email": "test@example.com",
  "password": "test123",
  "household_size": "2"
}
```

### Test 4: Login
```
URL: http://localhost:5000/api/auth/login
Method: POST
Body: {
  "username": "testuser",
  "password": "test123"
}
```

---

## ⚠️ Important Notes

1. **`/api` alone doesn't exist** - it's just a prefix for all API routes
2. **Always use specific endpoints** like `/api/health`, `/api/auth/register`, etc.
3. **Most endpoints require authentication** - get a JWT token from login first
4. **Use `localhost` not `0.0.0.0`** in browser

---

## 🔍 Troubleshooting "Not Found" Errors

If you get "Not Found" at `/api`:
- ✅ This is normal - there's no endpoint at `/api`
- ✅ Try `/api/health` instead
- ✅ Check server is running: `http://localhost:5000/`
- ✅ Check routes are registered (look for "✓ All routes registered successfully" in terminal)



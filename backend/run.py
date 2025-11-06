#!/usr/bin/env python
"""
Simple runner script that ensures proper setup
"""
import os
import sys

# Change to backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = os.getcwd()

print(f"Current directory: {current_dir}")
print(f"Backend directory: {backend_dir}")

if current_dir != backend_dir:
    print(f"⚠️  Changing to backend directory...")
    os.chdir(backend_dir)
    print(f"✓ Now in: {os.getcwd()}")
else:
    print(f"✓ Already in backend directory")

# Add backend to path
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
    print(f"✓ Added {backend_dir} to Python path")

# Check for .env file
env_path = os.path.join(backend_dir, '.env')
if not os.path.exists(env_path):
    print("⚠️  .env file not found. Creating default .env file...")
    with open(env_path, 'w') as f:
        f.write("""# Flask Configuration
SECRET_KEY=dev-secret-key-change-in-production-12345
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production-67890

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/smart_waste_db

# Google Search API Configuration (Required)
GOOGLE_SEARCH_API_KEY=your-api-key-here
GOOGLE_SEARCH_ENGINE_ID=your-engine-id-here

# Spoonacular API (Optional)
SPOONACULAR_API_KEY=

# CORS Configuration
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
""")
    print("✓ Created .env file. Please edit it with your API keys!\n")

# Now import and run the app
if __name__ == '__main__':
    try:
        from app import app
        print("\n🚀 Starting server...\n")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


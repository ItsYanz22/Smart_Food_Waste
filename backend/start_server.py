"""
Simple server startup script with error checking
"""
import os
import sys

# Check if .env file exists
if not os.path.exists('.env'):
    print("⚠️  WARNING: .env file not found!")
    print("Creating .env file with default values...")
    with open('.env', 'w') as f:
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
    print("✓ Created .env file. Please edit it with your API keys!")
    print()

# Try to import and check dependencies
try:
    from flask import Flask
    print("✓ Flask imported successfully")
except ImportError:
    print("❌ Flask not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    import mongoengine
    print("✓ MongoEngine imported successfully")
except ImportError:
    print("❌ MongoEngine not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

# Check MongoDB connection
try:
    from mongoengine import connect
    from dotenv import load_dotenv
    load_dotenv()
    
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/smart_waste_db')
    print(f"Attempting to connect to MongoDB: {mongo_uri.split('@')[-1] if '@' in mongo_uri else mongo_uri}")
    
    connect(host=mongo_uri, serverSelectionTimeoutMS=3000)
    print("✓ MongoDB connection successful")
except Exception as e:
    print(f"⚠️  MongoDB connection failed: {str(e)}")
    print("   Make sure MongoDB is running or check MONGO_URI in .env")
    print("   Continuing anyway... (some features may not work)")
    print()

print("\n" + "="*50)
print("Starting Flask server...")
print("="*50 + "\n")

# Now start the app
if __name__ == '__main__':
    try:
        # Import and run app
        import app
        app.app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check if port 5000 is already in use")
        print("3. Verify MongoDB is running")
        sys.exit(1)



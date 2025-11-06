"""
Main Flask application entry point for AI-Based Smart Food Waste Management
"""
from flask import Flask, request, make_response
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/smart_waste_db')
app.config['GOOGLE_SEARCH_API_KEY'] = os.getenv('GOOGLE_SEARCH_API_KEY', '')
app.config['GOOGLE_SEARCH_ENGINE_ID'] = os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')

# Initialize extensions
# Configure CORS properly
CORS(app, 
     origins=["http://localhost:8000", "http://127.0.0.1:8000"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)
jwt = JWTManager(app)
# Configure rate limiter with in-memory storage (fine for development)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"  # Explicitly set to suppress warning
)

# Add current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Connect to MongoDB (only once, before importing routes)
from mongoengine import connect, disconnect
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/smart_waste_db')
try:
    # Disconnect any existing connection first
    disconnect()
    connect(host=mongo_uri, serverSelectionTimeoutMS=5000)
    print("✓ MongoDB connected successfully")
except Exception as e:
    print(f"⚠️  MongoDB connection warning: {e}")
    print("   Continuing... (some features may not work)")

# Register blueprints
try:
    from routes import auth, dish, grocery, user
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(dish.bp, url_prefix='/api/dish')
    app.register_blueprint(grocery.bp, url_prefix='/api/grocery')
    app.register_blueprint(user.bp, url_prefix='/api/user')
    print("✓ All routes registered successfully")
except ImportError as e:
    print(f"❌ Error: Could not import routes: {e}")
    print(f"Current directory: {os.getcwd()}")
    import traceback
    traceback.print_exc()


# Handle OPTIONS requests for CORS preflight globally
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:8000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

@app.route('/')
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'message': 'AI-Based Smart Food Waste Management API',
        'version': '1.0.0'
    }, 200


@app.route('/api/health')
def api_health():
    """API health check endpoint"""
    return {
        'status': 'healthy',
        'api': 'running'
    }, 200


# Serve static files
from flask import send_from_directory
import os

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Ensure we're in the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != backend_dir:
        print(f"⚠️  Warning: Not in backend directory!")
        print(f"   Current: {os.getcwd()}")
        print(f"   Expected: {backend_dir}")
        print(f"   Changing to backend directory...")
        os.chdir(backend_dir)
        print(f"✓ Changed to: {os.getcwd()}")
        print()
    
    # Create static directories
    static_pdfs_dir = os.path.join(os.path.dirname(__file__), 'static', 'pdfs')
    os.makedirs(static_pdfs_dir, exist_ok=True)
    
    print("\n" + "="*50)
    print("Starting AI-Based Smart Food Waste Management API")
    print("="*50)
    print(f"Running from: {os.getcwd()}")
    print(f"Server listening on: 0.0.0.0:5000 (all interfaces)")
    print(f"🌐 Access in browser: http://localhost:5000")
    print(f"📡 API endpoint: http://localhost:5000/api")
    print(f"❤️  Health check: http://localhost:5000/api/health")
    print(f"🔧 CORS enabled for: http://localhost:8000")
    print(f"Debug mode: ON")
    print("="*50 + "\n")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the backend directory")
        print("2. Check if port 5000 is already in use")
        print("3. Verify all dependencies are installed: pip install -r requirements.txt")
        print("4. Check MongoDB connection")
        import traceback
        traceback.print_exc()



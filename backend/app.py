"""
Main Flask application entry point for AI-Based Smart Food Waste Management
"""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
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
CORS(app)  # Enable CORS for all routes
jwt = JWTManager(app)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Register blueprints
try:
    from backend.routes import auth, dish, grocery, user
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(dish.bp, url_prefix='/api/dish')
    app.register_blueprint(grocery.bp, url_prefix='/api/grocery')
    app.register_blueprint(user.bp, url_prefix='/api/user')
except ImportError as e:
    print(f"Warning: Could not import routes: {e}")


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
    # Create static directories
    os.makedirs('static/pdfs', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)



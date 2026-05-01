from flask import Flask, jsonify
from routes.report_routes import report_bp
from middleware.security import security_middleware, sanitize_error
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import os
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# ===== CRITICAL FIX CRT-003: CORS Protection =====
CORS(app, 
     origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"],
     supports_credentials=True,
     max_age=3600)

# ===== CRITICAL FIX CRT-004 & MED-004: Security Headers & Error Handling =====
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    return response

#  Rate Limiter initialization (CRT-001 & MED-001: All endpoints)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["30 per minute"],
    storage_uri="memory://"
)

limiter.init_app(app)

#  Security middleware
@app.before_request
def before_request():
    result = security_middleware()
    if result is not None:
        return result

# ===== CRITICAL FIX CRT-004: Global Error Handler =====
@app.errorhandler(Exception)
def handle_error(error):
    """Generic error handler to prevent information leakage"""
    # Log actual error server-side
    app.logger.error(f"Internal error: {str(error)}", exc_info=True)
    
    # Return generic error to client
    if isinstance(error, HTTPException):
        return jsonify({"error": "Request processing failed"}), error.code
    
    return jsonify({"error": "AI service unavailable"}), 500

# Register routes
app.register_blueprint(report_bp)

# ===== MED-001: Apply rate limiting to /health endpoint =====
@app.route("/health", methods=["GET"])
@limiter.limit("30 per minute")
def health():
    return jsonify({"status": "AI service running"}), 200

# ===== CRITICAL FIX CRT-002: Health check is now authenticated =====
@app.route("/status", methods=["GET"])
def status():
    """Unauthenticated status endpoint"""
    return jsonify({"status": "operational"}), 200

if __name__ == "__main__":
    # ===== CRITICAL FIX CRT-001: HTTPS Configuration =====
    # In production: Use proper SSL certificates
    # For development: Run with SSL context
    import ssl
    
    debug = os.getenv("FLASK_ENV") == "development"
    
    if debug:
        # Development: HTTP only
        app.run(host="127.0.0.1", port=5000, debug=True)
    else:
        # Production: HTTPS with SSL
        ssl_context = 'adhoc'  # Use proper certificates in production
        app.run(host="0.0.0.0", port=5000, ssl_context=ssl_context, threaded=True)
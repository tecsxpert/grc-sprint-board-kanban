from dotenv import load_dotenv
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.errors import RateLimitExceeded
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import HTTPException

# Safe imports
try:
    from middleware.security import security_middleware
except Exception:
    def security_middleware():
        return None

try:
    from routes.report_routes import report_bp
except Exception:
    report_bp = None

# Load environment variables
load_dotenv()


def api_response(success=True, data=None, message="", status_code=200):
    return {
        "success": success,
        "data": data or {},
        "message": message
    }, status_code


def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    # Rate limiter
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["30 per minute"],
        storage_uri="memory://"
    )
    limiter.init_app(app)

    # Security middleware
    @app.before_request
    def before_request():
        return security_middleware()

    # Security headers
    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; frame-ancestors 'none'; base-uri 'self'"
        )
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    # Home route
    @app.route("/")
    def home():
        return api_response(
            success=True,
            message="Flask AI Service Running"
        )

    # Health route
    @app.route("/health")
    def health():
        return api_response(
            success=True,
            data={
                "status": "healthy",
                "service": "ai-service"
            },
            message="Health check successful"
        )

    # Rate limit handler
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit(error):
        return api_response(
            success=False,
            message="Rate limit exceeded",
            status_code=429
        )

    # HTTP exception handler
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return api_response(
            success=False,
            message=error.description,
            status_code=error.code
        )

    # Global exception handler
    @app.errorhandler(Exception)
    def handle_exception(error):
        print("ERROR:", str(error))
        return api_response(
            success=False,
            message="Internal server error",
            status_code=500
        )

    # Register blueprint safely
    if report_bp:
        app.register_blueprint(report_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
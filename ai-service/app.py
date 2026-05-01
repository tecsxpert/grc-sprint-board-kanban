from flask import Flask
from routes.report_routes import report_bp
from middleware.security import security_middleware
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

#  Correct Limiter initialization
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["30 per minute"]
)

limiter.init_app(app)

#  Register middleware
@app.before_request
def before_request():
    result = security_middleware()
    if result is not None:
        return result

# Register routes
app.register_blueprint(report_bp)

@app.route("/health")
def health():
    return {"status": "AI service running"}


if __name__ == "__main__":
    app.run(port=5000, debug=True)
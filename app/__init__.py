from app.database import init_database
from flask import Flask
import secrets

from flask import request
from app.security.logger import log_request

from app.routes import main_bp, admin_bp


def create_app():

    app = Flask(__name__)
    
    init_database()

    app.secret_key = secrets.token_hex(32)

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    @app.before_request
    def capture_request():

        log_request(
            ip=request.remote_addr,
            method=request.method,
            path=request.full_path,
            user_agent=request.headers.get("User-Agent", "Unknown")
        )

    return app
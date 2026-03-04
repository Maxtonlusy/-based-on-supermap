from flask import Flask
from blueprints.socketio import socketio_all, socketio
from blueprints.home_page import home_page
from blueprints.health_page import health_page
from blueprints.feedback_page import feedback_page
from blueprints.user_information import user_information
from blueprints.ai_task import task
from blueprints.login import login
from blueprints.nlp import nlp
from flask_cors import CORS



def create_app():
    app = Flask(__name__, static_folder='assets')

    app.secret_key = 'liutingtaon'

    app.config.update(
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_PATH='/',
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_HTTPONLY=True
    )

    CORS(app,
         origins="*",
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"])


    app.register_blueprint(home_page)
    app.register_blueprint(health_page)
    app.register_blueprint(feedback_page)
    app.register_blueprint(user_information)
    app.register_blueprint(task)
    app.register_blueprint(login)
    app.register_blueprint(nlp)

    app.register_blueprint(socketio_all)
    socketio.init_app(app, cors_allowed_origins="*")

    return app


if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', port=5137, allow_unsafe_werkzeug=True)

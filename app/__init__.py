from flask import Flask

def create_app():
    from app.api_routes import api
    app = Flask(__name__)
    app.register_blueprint(api)
    return app

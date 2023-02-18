from flask import Flask
from .routes.myroutes import blog
from .extension import mongo


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "we are the champions"
    app.config["MONGO_URI"] = "mongodb://localhost:27017/Blog"

    mongo.init_app(app)

    app.register_blueprint(blog)

    return app

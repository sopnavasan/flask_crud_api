from flask import Flask

from app.config import db
from app.routes.course_routes import course_bp
from app.routes.student_routes import student_bp


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)

    return app

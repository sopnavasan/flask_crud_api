from app import create_app
from app.config import db
from app.models import Course, Student  # noqa: F401

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

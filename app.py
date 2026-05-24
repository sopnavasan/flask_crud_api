from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError, IntegrityError
from datetime import datetime

app = Flask(_name_)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root123@localhost/flask_crud_db2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    joined_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.get_json()
    if not data.get("full_name"):
        return error("Full name is required.")

    if not data.get("email"):
         return error("Email is required.")
    if not data.get("age"):
        return error("Age is required.")

    if not data.get("joined_date"):
        return error("Joined date is required.")


    if Student.query.filter_by(email=data.get("email")).first():
        return error("Email already exists")

    try:
        student = Student(
            full_name=data["full_name"],
            email=data["email"],
            age=int(data["age"]),
            cgpa=float(data.get("cgpa", 0.0)),
            is_active=data.get("is_active", True),
            joined_date=datetime.strptime(data["joined_date"], "%Y-%m-%d").date()
        )

        if student.age <= 0:
            return error("Age must be positive")

        db.session.add(student)
        db.session.commit()

        return jsonify({"message": "Student created", "id": student.id}), 201

    except Exception:
        return error("Invalid input data")   
 
@app.route("/api/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([{
        "id": s.id,
        "name": s.full_name,
        "email": s.email,
        "age": s.age
    } for s in students]) 

@app.route("/api/students/<int:id>", methods=["GET"])
def get_student(id):
    s = Student.query.get(id)
    if not s:
        return error("Student not found", 404)

    return jsonify({
        "id": s.id,
        "name": s.full_name,
        "email": s.email,
        "age": s.age
    })

@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):
    s = Student.query.get(id)
    if not s:
        return error("Student not found", 404)

    data = request.get_json()
    if not data:
        return error("Missing data")

    s.full_name = data.get("full_name", s.full_name)
    s.email = data.get("email", s.email)
    s.age = int(data.get("age", s.age))

    db.session.commit()
    return jsonify({"message": "Updated"})


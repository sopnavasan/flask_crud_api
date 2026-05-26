from datetime import datetime

from flask import jsonify, request

from app.config import db
from app.models.student_model import Student


def error(msg, code=400):
    return jsonify({"error": msg}), code


def create_student():
    data = request.get_json()

    if not data.get("full_name"):
        return error("Full name is required")

    if not data.get("email"):
        return error("Email is required")

    if Student.query.filter_by(email=data["email"]).first():
        return error("Email already exists")

    try:
        student = Student(
            full_name=data["full_name"],
            email=data["email"],
            age=int(data["age"]),
            cgpa=float(data.get("cgpa", 0.0)),
            joined_date=datetime.strptime(
                data["joined_date"], "%Y-%m-%d"
            ).date(),
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({
            "message": "Student created",
            "id": student.id,
        }), 201

    except (KeyError, TypeError, ValueError):
        return error("Invalid data")


def get_students():
    students = Student.query.all()

    return jsonify([{
        "id": s.id,
        "name": s.full_name,
        "email": s.email,
        "age": s.age,
    } for s in students])


def get_student(id):
    s = Student.query.get(id)

    if not s:
        return error("Student not found", 404)

    return jsonify({
        "id": s.id,
        "name": s.full_name,
        "email": s.email,
        "age": s.age,
    })


def update_student(id):
    s = Student.query.get(id)

    if not s:
        return error("Student not found", 404)

    data = request.get_json()

    s.full_name = data.get("full_name", s.full_name)
    s.email = data.get("email", s.email)
    s.age = data.get("age", s.age)

    db.session.commit()

    return jsonify({"message": "Updated"})


def delete_student(id):
    s = Student.query.get(id)

    if not s:
        return error("Student not found", 404)

    db.session.delete(s)
    db.session.commit()

    return jsonify({"message": "Deleted"})

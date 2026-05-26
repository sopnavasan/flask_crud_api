from flask import jsonify, request

from app.config import db
from app.models.course_model import Course


def error(msg, code=400):
    return jsonify({"error": msg}), code


def create_course():
    data = request.get_json()

    if not data.get("course_title"):
        return error("Course title is required")

    if Course.query.filter_by(course_title=data["course_title"]).first():
        return error("Course title already exists")

    try:
        course = Course(
            course_title=data["course_title"],
            course_fee=float(data["course_fee"]),
            duration_months=int(data["duration_months"]),
            description=data.get("description"),
            is_available=data.get("is_available", True),
        )

        db.session.add(course)
        db.session.commit()

        return jsonify({
            "message": "Course created",
            "id": course.id,
        }), 201

    except (KeyError, TypeError, ValueError):
        return error("Invalid data")


def get_courses():
    courses = Course.query.all()

    return jsonify([{
        "id": c.id,
        "course_title": c.course_title,
        "course_fee": c.course_fee,
        "duration_months": c.duration_months,
        "is_available": c.is_available,
    } for c in courses])


def get_course(id):
    c = Course.query.get(id)

    if not c:
        return error("Course not found", 404)

    return jsonify({
        "id": c.id,
        "course_title": c.course_title,
        "course_fee": c.course_fee,
        "duration_months": c.duration_months,
        "description": c.description,
        "is_available": c.is_available,
    })


def update_course(id):
    c = Course.query.get(id)

    if not c:
        return error("Course not found", 404)

    data = request.get_json()

    c.course_title = data.get("course_title", c.course_title)
    c.course_fee = data.get("course_fee", c.course_fee)
    c.duration_months = data.get("duration_months", c.duration_months)
    c.description = data.get("description", c.description)
    if "is_available" in data:
        c.is_available = data["is_available"]

    db.session.commit()

    return jsonify({"message": "Updated"})


def delete_course(id):
    c = Course.query.get(id)

    if not c:
        return error("Course not found", 404)

    db.session.delete(c)
    db.session.commit()

    return jsonify({"message": "Deleted"})

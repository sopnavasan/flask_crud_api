from flask import Blueprint

from app.controllers.student_controller import (
    create_student,
    delete_student,
    get_student,
    get_students,
    update_student,
)

student_bp = Blueprint("student_bp", __name__)


@student_bp.route("/api/students", methods=["POST"])
def create():
    return create_student()


@student_bp.route("/api/students", methods=["GET"])
def get_all():
    return get_students()


@student_bp.route("/api/students/<int:id>", methods=["GET"])
def get_one(id):
    return get_student(id)


@student_bp.route("/api/students/<int:id>", methods=["PUT"])
def update(id):
    return update_student(id)


@student_bp.route("/api/students/<int:id>", methods=["DELETE"])
def delete(id):
    return delete_student(id)

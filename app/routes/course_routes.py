from flask import Blueprint

from app.controllers.course_controller import (
    create_course,
    delete_course,
    get_course,
    get_courses,
    update_course,
)

course_bp = Blueprint("course_bp", __name__)


@course_bp.route("/api/courses", methods=["POST"])
def create():
    return create_course()


@course_bp.route("/api/courses", methods=["GET"])
def get_all():
    return get_courses()


@course_bp.route("/api/courses/<int:id>", methods=["GET"])
def get_one(id):
    return get_course(id)


@course_bp.route("/api/courses/<int:id>", methods=["PUT"])
def update(id):
    return update_course(id)


@course_bp.route("/api/courses/<int:id>", methods=["DELETE"])
def delete(id):
    return delete_course(id)

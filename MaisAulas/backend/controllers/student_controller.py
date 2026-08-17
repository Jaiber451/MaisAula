from flask import Blueprint, jsonify, request
from services.student_service import StudentService

student_bp = Blueprint("students", __name__)

@student_bp.get("")
def list_students():
    return jsonify(StudentService.list_all())

@student_bp.get("/<int:item_id>")
def get_student(item_id):
    item = StudentService.get(item_id)
    return jsonify(item.to_dict() if item else {"error": "Aluno não encontrado"}), (200 if item else 404)

@student_bp.post("")
def create_student():
    data = request.get_json() or {}
    for field in ("name", "email"):
        if not data.get(field):
            return jsonify({"error": f"Campo obrigatório: {field}"}), 400
    return jsonify(StudentService.create(data)), 201

@student_bp.put("/<int:item_id>")
def update_student(item_id):
    item = StudentService.update(item_id, request.get_json() or {})
    return jsonify(item or {"error": "Aluno não encontrado"}), (200 if item else 404)

@student_bp.delete("/<int:item_id>")
def delete_student(item_id):
    return jsonify({"deleted": StudentService.delete(item_id)})

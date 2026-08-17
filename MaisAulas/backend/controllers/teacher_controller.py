from flask import Blueprint, jsonify, request
from services.teacher_service import TeacherService

teacher_bp = Blueprint("teachers", __name__)

@teacher_bp.get("")
def list_teachers(): return jsonify(TeacherService.list_all())

@teacher_bp.get("/<int:item_id>")
def get_teacher(item_id):
    item = TeacherService.get(item_id)
    return jsonify(item.to_dict() if item else {"error": "Professor não encontrado"}), (200 if item else 404)

@teacher_bp.post("")
def create_teacher():
    data = request.get_json() or {}
    if not all(data.get(x) for x in ("name", "email", "specialty")):
        return jsonify({"error": "name, email e specialty são obrigatórios"}), 400
    return jsonify(TeacherService.create(data)), 201

@teacher_bp.put("/<int:item_id>")
def update_teacher(item_id):
    item = TeacherService.update(item_id, request.get_json() or {})
    return jsonify(item or {"error": "Professor não encontrado"}), (200 if item else 404)

@teacher_bp.delete("/<int:item_id>")
def delete_teacher(item_id):
    return jsonify({"deleted": TeacherService.delete(item_id)})

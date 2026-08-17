from flask import Blueprint, jsonify, request
from services.subject_service import SubjectService

subject_bp = Blueprint("subjects", __name__)

@subject_bp.get("")
def list_subjects(): return jsonify(SubjectService.list_all())

@subject_bp.get("/<int:item_id>")
def get_subject(item_id):
    item = SubjectService.get(item_id)
    return jsonify(item.to_dict() if item else {"error": "Disciplina não encontrada"}), (200 if item else 404)

@subject_bp.post("")
def create_subject():
    data = request.get_json() or {}
    if not data.get("name"):
        return jsonify({"error": "name é obrigatório"}), 400
    return jsonify(SubjectService.create(data)), 201

@subject_bp.put("/<int:item_id>")
def update_subject(item_id):
    item = SubjectService.update(item_id, request.get_json() or {})
    return jsonify(item or {"error": "Disciplina não encontrada"}), (200 if item else 404)

@subject_bp.delete("/<int:item_id>")
def delete_subject(item_id):
    return jsonify({"deleted": SubjectService.delete(item_id)})

from flask import Blueprint, jsonify, request
from services.class_service import ClassService

class_bp = Blueprint("classes", __name__)

@class_bp.get("")
def list_classes(): return jsonify(ClassService.list_all())

@class_bp.get("/<int:item_id>")
def get_class(item_id):
    item = ClassService.get(item_id)
    return jsonify(item.to_dict() if item else {"error": "Turma não encontrada"}), (200 if item else 404)

@class_bp.post("")
def create_class():
    data = request.get_json() or {}
    if not data.get("name") or not data.get("grade"):
        return jsonify({"error": "name e grade são obrigatórios"}), 400
    return jsonify(ClassService.create(data)), 201

@class_bp.put("/<int:item_id>")
def update_class(item_id):
    item = ClassService.update(item_id, request.get_json() or {})
    return jsonify(item or {"error": "Turma não encontrada"}), (200 if item else 404)

@class_bp.delete("/<int:item_id>")
def delete_class(item_id):
    return jsonify({"deleted": ClassService.delete(item_id)})

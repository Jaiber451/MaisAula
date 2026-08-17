from flask import Blueprint, jsonify, request
from services.activity_service import ActivityService

activity_bp = Blueprint("activities", __name__)

@activity_bp.get("")
def list_activities():
    if any(key in request.args for key in ("subject_id", "status", "search", "sort", "direction")):
        return jsonify(ActivityService.filtered(request.args))
    return jsonify(ActivityService.list_all())

@activity_bp.get("/<int:item_id>")
def get_activity(item_id):
    item = ActivityService.get(item_id)
    return jsonify(item.to_dict() if item else {"error": "Atividade não encontrada"}), (200 if item else 404)

@activity_bp.post("")
def create_activity():
    data = request.get_json() or {}
    required = ("title", "subject_id", "class_id", "due_date")
    if not all(data.get(x) is not None and data.get(x) != "" for x in required):
        return jsonify({"error": "title, subject_id, class_id e due_date são obrigatórios"}), 400
    return jsonify(ActivityService.create(data)), 201

@activity_bp.put("/<int:item_id>")
def update_activity(item_id):
    item = ActivityService.update(item_id, request.get_json() or {})
    return jsonify(item or {"error": "Atividade não encontrada"}), (200 if item else 404)

@activity_bp.delete("/<int:item_id>")
def delete_activity(item_id):
    return jsonify({"deleted": ActivityService.delete(item_id)})

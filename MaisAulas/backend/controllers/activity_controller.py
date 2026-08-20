from flask import Blueprint, jsonify, request
from services.activity_service import ActivityService

activity_bp = Blueprint("activities", __name__)

class ActivityController:
    def list(self):
        if any(key in request.args for key in ("subject_id", "status", "search", "sort", "direction")):
            return jsonify(ActivityService.filtered(request.args))
        return jsonify(ActivityService("list").execute())

    def get(self, item_id):
        item = ActivityService("get", item_id=item_id).execute()
        return jsonify(item.to_dict() if item else {"error": "Atividade não encontrado"}), (200 if item else 404)

    def create(self):
        data = request.get_json() or {}
        required = ("title", "subject_id", "class_id", "due_date")
        if not all(data.get(field) is not None and data.get(field) != "" for field in required):
            return jsonify({"error": "title, subject_id, class_id e due_date são obrigatórios"}), 400
        return jsonify(ActivityService("create", data=data).execute()), 201

    def update(self, item_id):
        item = ActivityService("update", item_id=item_id, data=request.get_json() or {}).execute()
        return jsonify(item or {"error": "Atividade não encontrado"}), (200 if item else 404)

    def delete(self, item_id):
        deleted = ActivityService("delete", item_id=item_id).execute()
        return jsonify({"deleted": deleted}), (200 if deleted else 404)

controller = ActivityController()
activity_bp.add_url_rule("", view_func=controller.list, methods=["GET"])
activity_bp.add_url_rule("/<int:item_id>", view_func=controller.get, methods=["GET"])
activity_bp.add_url_rule("", view_func=controller.create, methods=["POST"])
activity_bp.add_url_rule("/<int:item_id>", view_func=controller.update, methods=["PUT"])
activity_bp.add_url_rule("/<int:item_id>", view_func=controller.delete, methods=["DELETE"])

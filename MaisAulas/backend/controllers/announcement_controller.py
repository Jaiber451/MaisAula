from flask import Blueprint, jsonify, request
from services.announcement_service import AnnouncementService

announcement_bp = Blueprint("announcements", __name__)

class AnnouncementController:
    def list(self):
        return jsonify(AnnouncementService("list").execute())

    def get(self, item_id):
        item = AnnouncementService("get", item_id=item_id).execute()
        return jsonify(item.to_dict() if item else {"error": "Aviso não encontrado"}), (200 if item else 404)

    def create(self):
        data = request.get_json() or {}
        if not all(data.get(field) for field in ('title', 'message')):
            return jsonify({"error": "title, message são obrigatórios"}), 400
        return jsonify(AnnouncementService("create", data=data).execute()), 201

    def update(self, item_id):
        item = AnnouncementService("update", item_id=item_id, data=request.get_json() or {}).execute()
        return jsonify(item or {"error": "Aviso não encontrado"}), (200 if item else 404)

    def delete(self, item_id):
        deleted = AnnouncementService("delete", item_id=item_id).execute()
        return jsonify({"deleted": deleted}), (200 if deleted else 404)

controller = AnnouncementController()
announcement_bp.add_url_rule("", view_func=controller.list, methods=["GET"])
announcement_bp.add_url_rule("/<int:item_id>", view_func=controller.get, methods=["GET"])
announcement_bp.add_url_rule("", view_func=controller.create, methods=["POST"])
announcement_bp.add_url_rule("/<int:item_id>", view_func=controller.update, methods=["PUT"])
announcement_bp.add_url_rule("/<int:item_id>", view_func=controller.delete, methods=["DELETE"])

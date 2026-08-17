from flask import Blueprint, jsonify, request
from services.announcement_service import AnnouncementService

announcement_bp = Blueprint("announcements", __name__)

@announcement_bp.get("")
def list_announcements(): return jsonify(AnnouncementService.list_all())

@announcement_bp.get("/<int:item_id>")
def get_announcement(item_id):
    item = AnnouncementService.get(item_id)
    return jsonify(item.to_dict() if item else {"error": "Aviso não encontrado"}), (200 if item else 404)

@announcement_bp.post("")
def create_announcement():
    data = request.get_json() or {}
    if not data.get("title") or not data.get("message"):
        return jsonify({"error": "title e message são obrigatórios"}), 400
    return jsonify(AnnouncementService.create(data)), 201

@announcement_bp.put("/<int:item_id>")
def update_announcement(item_id):
    item = AnnouncementService.update(item_id, request.get_json() or {})
    return jsonify(item or {"error": "Aviso não encontrado"}), (200 if item else 404)

@announcement_bp.delete("/<int:item_id>")
def delete_announcement(item_id):
    return jsonify({"deleted": AnnouncementService.delete(item_id)})

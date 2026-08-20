from flask import Blueprint, jsonify, request
from services.teacher_service import TeacherService

teacher_bp = Blueprint("teachers", __name__)

class TeacherController:
    def list(self):
        return jsonify(TeacherService("list").execute())

    def get(self, item_id):
        item = TeacherService("get", item_id=item_id).execute()
        return jsonify(item.to_dict() if item else {"error": "Professor não encontrado"}), (200 if item else 404)

    def create(self):
        data = request.get_json() or {}
        if not all(data.get(field) for field in ('name', 'email', 'specialty')):
            return jsonify({"error": "name, email, specialty são obrigatórios"}), 400
        return jsonify(TeacherService("create", data=data).execute()), 201

    def update(self, item_id):
        item = TeacherService("update", item_id=item_id, data=request.get_json() or {}).execute()
        return jsonify(item or {"error": "Professor não encontrado"}), (200 if item else 404)

    def delete(self, item_id):
        deleted = TeacherService("delete", item_id=item_id).execute()
        return jsonify({"deleted": deleted}), (200 if deleted else 404)

controller = TeacherController()
teacher_bp.add_url_rule("", view_func=controller.list, methods=["GET"])
teacher_bp.add_url_rule("/<int:item_id>", view_func=controller.get, methods=["GET"])
teacher_bp.add_url_rule("", view_func=controller.create, methods=["POST"])
teacher_bp.add_url_rule("/<int:item_id>", view_func=controller.update, methods=["PUT"])
teacher_bp.add_url_rule("/<int:item_id>", view_func=controller.delete, methods=["DELETE"])

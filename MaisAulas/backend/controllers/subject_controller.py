from flask import Blueprint, jsonify, request
from services.subject_service import SubjectService

subject_bp = Blueprint("subjects", __name__)

class SubjectController:
    def list(self):
        return jsonify(SubjectService("list").execute())

    def get(self, item_id):
        item = SubjectService("get", item_id=item_id).execute()
        return jsonify(item.to_dict() if item else {"error": "Disciplina não encontrado"}), (200 if item else 404)

    def create(self):
        data = request.get_json() or {}
        if not data.get("name"):
            return jsonify({"error": "name é obrigatório"}), 400
        return jsonify(SubjectService("create", data=data).execute()), 201

    def update(self, item_id):
        item = SubjectService("update", item_id=item_id, data=request.get_json() or {}).execute()
        return jsonify(item or {"error": "Disciplina não encontrado"}), (200 if item else 404)

    def delete(self, item_id):
        deleted = SubjectService("delete", item_id=item_id).execute()
        return jsonify({"deleted": deleted}), (200 if deleted else 404)

controller = SubjectController()
subject_bp.add_url_rule("", view_func=controller.list, methods=["GET"])
subject_bp.add_url_rule("/<int:item_id>", view_func=controller.get, methods=["GET"])
subject_bp.add_url_rule("", view_func=controller.create, methods=["POST"])
subject_bp.add_url_rule("/<int:item_id>", view_func=controller.update, methods=["PUT"])
subject_bp.add_url_rule("/<int:item_id>", view_func=controller.delete, methods=["DELETE"])

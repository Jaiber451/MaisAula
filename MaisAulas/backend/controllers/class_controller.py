from flask import Blueprint, jsonify, request
from services.class_service import ClassService

class_bp = Blueprint("classes", __name__)

class ClassController:
    def list(self):
        return jsonify(ClassService("list").execute())

    def get(self, item_id):
        item = ClassService("get", item_id=item_id).execute()
        return jsonify(item.to_dict() if item else {"error": "Turma não encontrado"}), (200 if item else 404)

    def create(self):
        data = request.get_json() or {}
        if not all(data.get(field) for field in ('name', 'grade')):
            return jsonify({"error": "name, grade são obrigatórios"}), 400
        return jsonify(ClassService("create", data=data).execute()), 201

    def update(self, item_id):
        item = ClassService("update", item_id=item_id, data=request.get_json() or {}).execute()
        return jsonify(item or {"error": "Turma não encontrado"}), (200 if item else 404)

    def delete(self, item_id):
        deleted = ClassService("delete", item_id=item_id).execute()
        return jsonify({"deleted": deleted}), (200 if deleted else 404)

controller = ClassController()
class_bp.add_url_rule("", view_func=controller.list, methods=["GET"])
class_bp.add_url_rule("/<int:item_id>", view_func=controller.get, methods=["GET"])
class_bp.add_url_rule("", view_func=controller.create, methods=["POST"])
class_bp.add_url_rule("/<int:item_id>", view_func=controller.update, methods=["PUT"])
class_bp.add_url_rule("/<int:item_id>", view_func=controller.delete, methods=["DELETE"])

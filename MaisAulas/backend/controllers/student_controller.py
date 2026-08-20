from flask import Blueprint, jsonify, request
from services.student_service import StudentService

student_bp = Blueprint("students", __name__)

class StudentController:
    def list(self):
        return jsonify(StudentService("list").execute())

    def get(self, item_id):
        item = StudentService("get", item_id=item_id).execute()
        return jsonify(item.to_dict() if item else {"error": "Aluno não encontrado"}), (200 if item else 404)

    def create(self):
        data = request.get_json() or {}
        if not all(data.get(field) for field in ('name', 'email')):
            return jsonify({"error": "name, email são obrigatórios"}), 400
        return jsonify(StudentService("create", data=data).execute()), 201

    def update(self, item_id):
        item = StudentService("update", item_id=item_id, data=request.get_json() or {}).execute()
        return jsonify(item or {"error": "Aluno não encontrado"}), (200 if item else 404)

    def delete(self, item_id):
        deleted = StudentService("delete", item_id=item_id).execute()
        return jsonify({"deleted": deleted}), (200 if deleted else 404)

controller = StudentController()
student_bp.add_url_rule("", view_func=controller.list, methods=["GET"])
student_bp.add_url_rule("/<int:item_id>", view_func=controller.get, methods=["GET"])
student_bp.add_url_rule("", view_func=controller.create, methods=["POST"])
student_bp.add_url_rule("/<int:item_id>", view_func=controller.update, methods=["PUT"])
student_bp.add_url_rule("/<int:item_id>", view_func=controller.delete, methods=["DELETE"])

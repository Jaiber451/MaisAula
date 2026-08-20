from flask import Blueprint, jsonify, request
from services.dashboard_service import DashboardService
from services.activity_service import ActivityService

dashboard_bp = Blueprint("dashboard", __name__)

class DashboardController:
    def dashboard(self):
        student_id = request.args.get("student_id", default=1, type=int)
        return jsonify(DashboardService("summary", student_id).execute())

    def student_performance(self, student_id):
        return jsonify(DashboardService("performance", student_id).execute())

    def filtered_activities(self):
        return jsonify(ActivityService.filtered(request.args))

controller = DashboardController()
dashboard_bp.add_url_rule("/dashboard", view_func=controller.dashboard, methods=["GET"])
dashboard_bp.add_url_rule("/reports/students/<int:student_id>/performance", view_func=controller.student_performance, methods=["GET"])
dashboard_bp.add_url_rule("/reports/activities", view_func=controller.filtered_activities, methods=["GET"])

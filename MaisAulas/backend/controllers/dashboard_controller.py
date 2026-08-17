from flask import Blueprint, jsonify, request
from services.dashboard_service import DashboardService

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.get("/dashboard")
def dashboard():
    student_id = request.args.get("student_id", default=1, type=int)
    return jsonify(DashboardService.summary(student_id))

@dashboard_bp.get("/reports/students/<int:student_id>/performance")
def student_performance(student_id):
    return jsonify(DashboardService.performance(student_id))

@dashboard_bp.get("/reports/activities")
def filtered_activities():
    from services.activity_service import ActivityService
    return jsonify(ActivityService.filtered(request.args))

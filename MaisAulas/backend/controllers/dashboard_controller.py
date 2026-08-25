from flask import Blueprint, jsonify
from services.dashboard_summary_service import DashboardSummaryService
dashboard_bp=Blueprint("dashboard",__name__)
class DashboardController:
    def summary(self): return jsonify(DashboardSummaryService().execute())
controller=DashboardController()
dashboard_bp.add_url_rule("/dashboard",view_func=controller.summary,methods=["GET"])

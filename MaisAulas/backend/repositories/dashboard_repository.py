from sqlalchemy import text
from extensions import db

class DashboardRepository:
    @staticmethod
    def summary(student_id=1):
        result = db.session.execute(
            text("CALL sp_dashboard_summary(:student_id)"),
            {"student_id": student_id},
        )
        row = result.mappings().first()
        return dict(row) if row else {}

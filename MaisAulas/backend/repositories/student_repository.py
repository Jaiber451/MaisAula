from sqlalchemy import text
from extensions import db

class StudentRepository:
    @staticmethod
    def performance(student_id):
        result = db.session.execute(
            text("CALL sp_student_performance(:student_id)"),
            {"student_id": student_id},
        )
        return [dict(row) for row in result.mappings().all()]

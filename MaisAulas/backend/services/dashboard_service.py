from repositories.dashboard_repository import DashboardRepository
from repositories.student_repository import StudentRepository

class DashboardService:
    @staticmethod
    def summary(student_id=1):
        return DashboardRepository.summary(student_id)

    @staticmethod
    def performance(student_id):
        return StudentRepository.performance(student_id)

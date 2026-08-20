from repositories.dashboard_repository import DashboardRepository
from repositories.student_repository import StudentRepository

class DashboardService:
    def __init__(self, operation, student_id=None):
        self.operation = operation
        self.student_id = student_id

    def execute(self):
        if self.operation == "summary":
            return DashboardRepository.summary(self.student_id or 1)
        if self.operation == "performance":
            return StudentRepository.performance(self.student_id)
        raise ValueError("Operação inválida")

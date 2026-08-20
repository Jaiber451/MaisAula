from models.student import Student

class StudentService:
    def __init__(self, operation, item_id=None, data=None):
        self.operation = operation
        self.item_id = item_id
        self.data = data or {}

    def execute(self):
        if self.operation == "list":
            return [item.to_dict() for item in Student.list_all()]

        if self.operation == "get":
            return Student.get_by_id(self.item_id)

        if self.operation == "create":
            data = dict(self.data)
            for field, value in {'status': 'active'}.items():
                data.setdefault(field, value)
            return Student.create(data).to_dict()

        item = Student.get_by_id(self.item_id)
        if not item:
            return None if self.operation == "update" else False

        if self.operation == "update":
            return item.update(self.data).to_dict()

        if self.operation == "delete":
            return item.delete()

        raise ValueError("Operação inválida")


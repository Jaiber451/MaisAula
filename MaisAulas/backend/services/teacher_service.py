from models.teacher import Teacher

class TeacherService:
    def __init__(self, operation, item_id=None, data=None):
        self.operation = operation
        self.item_id = item_id
        self.data = data or {}

    def execute(self):
        if self.operation == "list":
            return [item.to_dict() for item in Teacher.list_all()]

        if self.operation == "get":
            return Teacher.get_by_id(self.item_id)

        if self.operation == "create":
            data = dict(self.data)
            for field, value in {}.items():
                data.setdefault(field, value)
            return Teacher.create(data).to_dict()

        item = Teacher.get_by_id(self.item_id)
        if not item:
            return None if self.operation == "update" else False

        if self.operation == "update":
            return item.update(self.data).to_dict()

        if self.operation == "delete":
            return item.delete()

        raise ValueError("Operação inválida")


from models.activity import Activity
from repositories.activity_repository import ActivityRepository

class ActivityService:
    def __init__(self, operation, item_id=None, data=None):
        self.operation = operation
        self.item_id = item_id
        self.data = data or {}

    def execute(self):
        if self.operation == "list":
            return [item.to_dict() for item in Activity.list_all()]

        if self.operation == "get":
            return Activity.get_by_id(self.item_id)

        if self.operation == "create":
            data = dict(self.data)
            for field, value in {'status': 'pending', 'max_score': 10}.items():
                data.setdefault(field, value)
            return Activity.create(data).to_dict()

        item = Activity.get_by_id(self.item_id)
        if not item:
            return None if self.operation == "update" else False

        if self.operation == "update":
            return item.update(self.data).to_dict()

        if self.operation == "delete":
            return item.delete()

        raise ValueError("Operação inválida")

    @staticmethod
    def filtered(args):
        return ActivityRepository.filtered(
            subject_id=args.get("subject_id", type=int),
            status=args.get("status"),
            search=args.get("search"),
            sort=args.get("sort", "due_date"),
            direction=args.get("direction", "asc"),
        )


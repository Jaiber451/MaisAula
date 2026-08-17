from extensions import db
from models.activity import Activity
from repositories.activity_repository import ActivityRepository

class ActivityService:
    @staticmethod
    def list_all():
        return [item.to_dict() for item in Activity.query.order_by(Activity.due_date).all()]

    @staticmethod
    def get(item_id):
        return db.session.get(Activity, item_id)

    @staticmethod
    def create(data):
        item = Activity(
            title=data["title"],
            description=data.get("description"),
            subject_id=data["subject_id"],
            class_id=data["class_id"],
            due_date=data["due_date"],
            status=data.get("status", "pending"),
            max_score=data.get("max_score", 10),
        )
        db.session.add(item); db.session.commit()
        return item.to_dict()

    @staticmethod
    def update(item_id, data):
        item = ActivityService.get(item_id)
        if not item: return None
        for field in ("title", "description", "subject_id", "class_id", "due_date", "status", "max_score"):
            if field in data: setattr(item, field, data[field])
        db.session.commit()
        return item.to_dict()

    @staticmethod
    def delete(item_id):
        item = ActivityService.get(item_id)
        if not item: return False
        db.session.delete(item); db.session.commit()
        return True

    @staticmethod
    def filtered(args):
        return ActivityRepository.filtered(
            subject_id=args.get("subject_id", type=int),
            status=args.get("status"),
            search=args.get("search"),
            sort=args.get("sort", "due_date"),
            direction=args.get("direction", "asc"),
        )

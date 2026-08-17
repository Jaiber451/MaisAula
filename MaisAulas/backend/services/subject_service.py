from extensions import db
from models.subject import Subject

class SubjectService:
    @staticmethod
    def list_all():
        return [item.to_dict() for item in Subject.query.order_by(Subject.name).all()]

    @staticmethod
    def get(item_id):
        return db.session.get(Subject, item_id)

    @staticmethod
    def create(data):
        item = Subject(name=data["name"], color=data.get("color", "#5b6ff5"), teacher_id=data.get("teacher_id"))
        db.session.add(item); db.session.commit()
        return item.to_dict()

    @staticmethod
    def update(item_id, data):
        item = SubjectService.get(item_id)
        if not item: return None
        for field in ("name", "color", "teacher_id"):
            if field in data: setattr(item, field, data[field])
        db.session.commit()
        return item.to_dict()

    @staticmethod
    def delete(item_id):
        item = SubjectService.get(item_id)
        if not item: return False
        db.session.delete(item); db.session.commit()
        return True

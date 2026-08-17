from extensions import db
from models.teacher import Teacher

class TeacherService:
    @staticmethod
    def list_all():
        return [item.to_dict() for item in Teacher.query.order_by(Teacher.name).all()]

    @staticmethod
    def get(item_id):
        return db.session.get(Teacher, item_id)

    @staticmethod
    def create(data):
        item = Teacher(name=data["name"], email=data["email"], specialty=data["specialty"])
        db.session.add(item); db.session.commit()
        return item.to_dict()

    @staticmethod
    def update(item_id, data):
        item = TeacherService.get(item_id)
        if not item: return None
        for field in ("name", "email", "specialty"):
            if field in data: setattr(item, field, data[field])
        db.session.commit()
        return item.to_dict()

    @staticmethod
    def delete(item_id):
        item = TeacherService.get(item_id)
        if not item: return False
        db.session.delete(item); db.session.commit()
        return True

from extensions import db
from models.student import Student

class StudentService:
    @staticmethod
    def list_all():
        return [item.to_dict() for item in Student.query.order_by(Student.name).all()]

    @staticmethod
    def get(item_id):
        item = db.session.get(Student, item_id)
        return item

    @staticmethod
    def create(data):
        item = Student(
            name=data["name"],
            email=data["email"],
            class_id=data.get("class_id"),
            status=data.get("status", "active"),
        )
        db.session.add(item)
        db.session.commit()
        return item.to_dict()

    @staticmethod
    def update(item_id, data):
        item = StudentService.get(item_id)
        if not item:
            return None
        for field in ("name", "email", "class_id", "status"):
            if field in data:
                setattr(item, field, data[field])
        db.session.commit()
        return item.to_dict()

    @staticmethod
    def delete(item_id):
        item = StudentService.get(item_id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

from extensions import db
from models.school_class import SchoolClass

class ClassService:
    @staticmethod
    def list_all():
        return [item.to_dict() for item in SchoolClass.query.order_by(SchoolClass.name).all()]

    @staticmethod
    def get(item_id):
        return db.session.get(SchoolClass, item_id)

    @staticmethod
    def create(data):
        item = SchoolClass(name=data["name"], grade=data["grade"], shift=data.get("shift", "Manhã"))
        db.session.add(item); db.session.commit()
        return item.to_dict()

    @staticmethod
    def update(item_id, data):
        item = ClassService.get(item_id)
        if not item: return None
        for field in ("name", "grade", "shift"):
            if field in data: setattr(item, field, data[field])
        db.session.commit()
        return item.to_dict()

    @staticmethod
    def delete(item_id):
        item = ClassService.get(item_id)
        if not item: return False
        db.session.delete(item); db.session.commit()
        return True

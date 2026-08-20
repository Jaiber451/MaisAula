from extensions import db

class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), nullable=False, default="#5b6ff5")
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id", ondelete="SET NULL"))
    teacher = db.relationship("Teacher")

    @classmethod
    def list_all(cls):
        return cls.query.order_by(cls.name).all()

    @classmethod
    def get_by_id(cls, item_id):
        return db.session.get(cls, item_id)

    @classmethod
    def create(cls, data):
        item = cls(**{field: data[field] for field in ['name', 'color', 'teacher_id'] if field in data})
        db.session.add(item)
        db.session.commit()
        return item

    def update(self, data):
        for field in ['name', 'color', 'teacher_id']:
            if field in data:
                setattr(self, field, data[field])
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "teacher_id": self.teacher_id,
            "teacher_name": self.teacher.name if self.teacher else None,
        }

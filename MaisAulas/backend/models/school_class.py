from extensions import db

class SchoolClass(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    grade = db.Column(db.String(40), nullable=False)
    shift = db.Column(db.String(30), nullable=False, default="Manhã")

    students = db.relationship("Student", back_populates="school_class")

    @classmethod
    def list_all(cls):
        return cls.query.order_by(cls.name).all()

    @classmethod
    def get_by_id(cls, item_id):
        return db.session.get(cls, item_id)

    @classmethod
    def create(cls, data):
        item = cls(**{field: data[field] for field in ['name', 'grade', 'shift'] if field in data})
        db.session.add(item)
        db.session.commit()
        return item

    def update(self, data):
        for field in ['name', 'grade', 'shift']:
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
            "grade": self.grade,
            "shift": self.shift,
            "student_count": len(self.students),
        }

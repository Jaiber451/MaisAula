from datetime import datetime
from extensions import db

class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    max_score = db.Column(db.Numeric(5, 2), nullable=False, default=10)

    subject = db.relationship("Subject")
    school_class = db.relationship("SchoolClass")

    @classmethod
    def list_all(cls):
        return cls.query.order_by(cls.due_date).all()

    @classmethod
    def get_by_id(cls, item_id):
        return db.session.get(cls, item_id)

    @classmethod
    def create(cls, data):
        item = cls(**{field: data[field] for field in ['title', 'description', 'subject_id', 'class_id', 'due_date', 'status', 'max_score'] if field in data})
        db.session.add(item)
        db.session.commit()
        return item

    def update(self, data):
        for field in ['title', 'description', 'subject_id', 'class_id', 'due_date', 'status', 'max_score']:
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
            "title": self.title,
            "description": self.description,
            "subject_id": self.subject_id,
            "subject_name": self.subject.name if self.subject else None,
            "class_id": self.class_id,
            "class_name": self.school_class.name if self.school_class else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status,
            "max_score": float(self.max_score),
        }

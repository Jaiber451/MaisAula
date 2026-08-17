from datetime import datetime
from extensions import db

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False, unique=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id", ondelete="SET NULL"))
    status = db.Column(db.String(20), nullable=False, default="active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    school_class = db.relationship("SchoolClass", back_populates="students")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "class_id": self.class_id,
            "class_name": self.school_class.name if self.school_class else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

from datetime import datetime
from extensions import db

class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False, unique=True)
    specialty = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "specialty": self.specialty,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

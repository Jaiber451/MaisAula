from datetime import datetime
from extensions import db

class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False, unique=True)
    specialty = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @classmethod
    def list_all(cls):
        return cls.query.order_by(cls.name).all()

    @classmethod
    def get_by_id(cls, item_id):
        return db.session.get(cls, item_id)

    @classmethod
    def create(cls, data):
        item = cls(**{field: data[field] for field in ['name', 'email', 'specialty'] if field in data})
        db.session.add(item)
        db.session.commit()
        return item

    def update(self, data):
        for field in ['name', 'email', 'specialty']:
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
            "email": self.email,
            "specialty": self.specialty,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

from extensions import db

class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), nullable=False, default="#5b6ff5")
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id", ondelete="SET NULL"))
    teacher = db.relationship("Teacher")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "teacher_id": self.teacher_id,
            "teacher_name": self.teacher.name if self.teacher else None,
        }

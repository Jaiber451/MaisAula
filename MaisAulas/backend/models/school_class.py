from extensions import db

class SchoolClass(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    grade = db.Column(db.String(40), nullable=False)
    shift = db.Column(db.String(30), nullable=False, default="Manhã")

    students = db.relationship("Student", back_populates="school_class")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "grade": self.grade,
            "shift": self.shift,
            "student_count": len(self.students),
        }

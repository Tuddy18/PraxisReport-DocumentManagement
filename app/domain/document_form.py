from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from app.domain.json_serializable import JsonSerializable


class DocumentForm(db.Model, JsonSerializable):
    __tablename__ = 'DocumentForm'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    student_id = Column(Integer)

    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'DocumentForm',
        'polymorphic_on': type
    }

    def __repr__(self):
        return '<DocumentForm[%r] for student %r>' % (self.type, self.student_id)
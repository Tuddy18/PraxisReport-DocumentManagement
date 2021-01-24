from sqlalchemy.orm import relationship

from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Date
from app.domain.json_serializable import JsonSerializable


class Praxis(db.Model, JsonSerializable):
    __tablename__ = 'Praxis'
    id = Column(Integer, primary_key=True)

    start_date = Column(Date())
    end_date = Column(Date())

    student_form_id = Column(Integer, ForeignKey('StudentForm.id'), nullable=True)
    student_form = relationship("StudentForm", back_populates="praxis", lazy='joined')


    def __repr__(self):
        return '<Praxis %r - %r>' % (self.start_date, self.end_date)
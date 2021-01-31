import enum
from sqlalchemy.orm import relationship, validates

from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Date, Enum
from app.domain.json_serializable import JsonSerializable

class Praxis(db.Model, JsonSerializable):
    __tablename__ = 'Praxis'
    id = Column(Integer, primary_key=True)

    start_date = Column(Date())
    end_date = Column(Date())
    nr_credite = Column(Integer(), default=6)
    status = Column(String(120), default='in_progress')

    student_form_id = Column(Integer, ForeignKey('StudentForm.id'), nullable=True)
    student_form = relationship("StudentForm", back_populates="praxis", lazy='joined')

    mentor_form_id = Column(Integer, ForeignKey('MentorForm.id'), nullable=True)
    mentor_form = relationship("MentorForm", back_populates="praxis", lazy='joined')

    professor_form_id = Column(Integer, ForeignKey('ProfessorForm.id'), nullable=True)
    professor_form = relationship("ProfessorForm", back_populates="praxis", lazy='joined')

    @validates('status')
    def validate_status(self, key, status):
        possible_statues = ['in_progress', 'documented', 'completed', 'incorrect']
        assert status in possible_statues
        return status

    def __repr__(self):
        return '<Praxis %r - %r>' % (self.start_date, self.end_date)
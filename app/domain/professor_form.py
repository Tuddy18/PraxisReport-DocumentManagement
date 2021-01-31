from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.domain.praxis import *


class ProfessorForm(db.Model, JsonSerializable):
    __tablename__ = 'ProfessorForm'
    id = Column(Integer, primary_key=True)
    professor_profile_id = Column(Integer)
    praxis = relationship("Praxis", back_populates="professor_form")

    email = Column(String(120), nullable=True)
    name = Column(String(120), nullable=True)
    phone = Column(String(120), nullable=True)

    functie = Column(String(120), nullable=True)
    fax = Column(String(120), nullable=True)


    def __repr__(self):
        return '<ProfessorForm %r - %r>' % (self.email, self.name)
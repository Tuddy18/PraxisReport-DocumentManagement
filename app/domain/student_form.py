from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.domain.praxis import *


class StudentForm(db.Model, JsonSerializable):
    __tablename__ = 'StudentForm'
    id = Column(Integer, primary_key=True)
    student_profile_id = Column(Integer)
    praxis = relationship("Praxis", back_populates="student_form")

    email = Column(String(120), nullable=True)
    name = Column(String(120), nullable=True)
    phone = Column(String(120), nullable=True)
    cetatenie = Column(String(120), nullable=True)
    oras = Column(String(120), nullable=True)
    strada = Column(String(120), nullable=True)
    nr_cladire = Column(String(120), nullable=True)
    apartament = Column(String(120), nullable=True)
    judet = Column(String(120), nullable=True)
    cnp = Column(String(120), nullable=True)
    serie_ci = Column(String(120), nullable=True)
    nr_ci = Column(String(120), nullable=True)
    data_nasterii = Column(String(120), nullable=True)
    locul_nasterii = Column(String(120), nullable=True)
    an_studiu = Column(String(120), nullable=True)
    grupa = Column(String(120), nullable=True)
    specializare = Column(String(120), nullable=True)
    linie_studiu = Column(String(120), nullable=True)


    def __repr__(self):
        return '<StudentForm %r - %r>' % (self.email, self.name)
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.domain.praxis import *


class MentorForm(db.Model, JsonSerializable):
    __tablename__ = 'MentorForm'
    id = Column(Integer, primary_key=True)
    mentor_profile_id = Column(Integer)
    praxis = relationship("Praxis", back_populates="mentor_form")

    email = Column(String(120), nullable=True)
    name = Column(String(120), nullable=True)
    phone = Column(String(120), nullable=True)

    societate = Column(String(120), nullable=True)
    oras_sediu = Column(String(120), nullable=True)
    strada_sediu = Column(String(120), nullable=True)
    nr_sediu = Column(String(120), nullable=True)
    telefon_sediu = Column(String(120), nullable=True)
    fax_sediu = Column(String(120), nullable=True)
    email_sediu = Column(String(120), nullable=True)
    cod_fiscal = Column(String(120), nullable=True)
    cont = Column(String(120), nullable=True)
    banca_cont = Column(String(120), nullable=True)
    profesie_mentor = Column(String(120), nullable=True)
    reprezentant_legal = Column(String(120), nullable=True)
    adresa_stagiu_practica = Column(String(120), nullable=True)


    def __repr__(self):
        return '<MentorForm %r - %r>' % (self.email, self.name)
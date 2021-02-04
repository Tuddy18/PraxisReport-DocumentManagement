from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.domain.praxis import *


class ReportForm(db.Model, JsonSerializable):
    __tablename__ = 'ReportForm'
    id = Column(Integer, primary_key=True)

    praxis = relationship("Praxis", back_populates="report_form")

    perioada1 = Column(String(120), nullable=True)
    descriere1 = Column(String(120), nullable=True)
    perioada2 = Column(String(120), nullable=True)
    descriere2 = Column(String(120), nullable=True)
    perioada3 = Column(String(120), nullable=True)
    descriere3 = Column(String(120), nullable=True)
    perioada4 = Column(String(120), nullable=True)
    descriere4 = Column(String(120), nullable=True)
    perioada5 = Column(String(120), nullable=True)
    descriere5 = Column(String(120), nullable=True)
    perioada6 = Column(String(120), nullable=True)
    descriere6 = Column(String(120), nullable=True)


    def __repr__(self):
        return '<StudentForm %r - %r>' % (self.email, self.name)
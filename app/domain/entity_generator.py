import sqlalchemy as sqAl
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import xml.etree.ElementTree as ET

from app.domain.document_form import *

def generate_dict_from_xml(xml_el):
    dict = {}
    dict["tablename"] = xml_el.attrib['table']

    type_map = {'java.lang.String': sqAl.String,
                'java.util.Date': sqAl.Date,
                'java.lang.Double': sqAl.Float,
                'java.lang.Long': sqAl.Integer}

    for i, field_el in enumerate(xml_el.findall('property')):
        field = field_el.attrib
        dict['property' + str(i)] = field

    return dict

def generate_class(class_el, superclass=declarative_base(sqAl.MetaData())):
    type_map = {'java.lang.String': sqAl.String(120),
                'java.util.Date': sqAl.Date,
                'java.lang.Double': sqAl.Float,
                'java.lang.Long': sqAl.Integer}


    dynclass_dict = {
        'id': sqAl.Column(sqAl.Integer, primary_key=True),
        '__tablename__': class_el.attrib['table'],
        '__mapper_args__': {
                'polymorphic_identity': class_el.attrib['table']
            }
        }
    if superclass == declarative_base(sqAl.MetaData()):
        dynclass_dict['id'] = sqAl.Column(sqAl.Integer, primary_key=True)
    else:
        dynclass_dict['id'] = sqAl.Column(sqAl.Integer, ForeignKey(str(superclass.__table__) + '.id'), primary_key=True)

    for field_el in class_el.findall('property'):
        field = field_el.attrib
        if field['type'] in type_map:
            dynclass_dict[field['name']] = sqAl.Column(type_map[field['type']])

    return type(class_el.attrib['table'].capitalize(), (superclass,), dynclass_dict)


classe = ET.parse('../resources/student_convention_form.hbm.xml').getroot().find('class')
dict = generate_dict_from_xml(classe)
StudentConventionForm = generate_class(classe, DocumentForm)

if __name__ == '__main__':
    # the two following lines create the table (if not already existing)
    engine = sqAl.create_engine('sqlite:///data.db', echo=True)
    StudentConventionForm.__base__.metadata.create_all(engine, checkfirst=True)

    session = sessionmaker(bind=engine)()
    s = StudentConventionForm(firstname="John F.", lastname="Kennicknich")
    session.add(s)
    session.commit()
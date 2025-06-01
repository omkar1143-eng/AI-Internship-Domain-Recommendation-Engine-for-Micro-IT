from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///students.db')
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gpa = Column(Float)
    skills = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def save_student(name, gpa, skills):
    skill_str = ";".join(skills)
    student = Student(name=name, gpa=gpa, skills=skill_str)
    session.add(student)
    session.commit()

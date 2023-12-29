from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from config.database import sessionmaker

session_db = sessionmaker()

Base = declarative_base()

class Profile(Base):
    __tablename__ = 'profile'
    
    id = Column(Integer, primary_key=True)
    job = Column(String(150))
    company = Column(String(150))
    ssn = Column(String(250))
    residence = Column(String(150))
    current_location = Column(String(250))
    blood_group = Column(String(150))
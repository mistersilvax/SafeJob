from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    lang = Column(String)
    name = Column(String)
    age = Column(String)
    nationality = Column(String)
    experience = Column(Text)
    languages = Column(String)
    location = Column(String)
    fines = Column(String)
    work_visa = Column(String)
    relocate = Column(String)
    need_passport_help = Column(String)
    need_police_help = Column(String)
    resume_path = Column(String)
    video_path = Column(String)
    notes = Column(Text)

# create tables
Base.metadata.create_all(engine)

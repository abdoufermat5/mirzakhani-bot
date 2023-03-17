import os

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

DB = os.getenv("DB")
DATABASE_NAME = os.getenv("DATABASE_NAME")
# Create the database engine
engine = create_engine(f"sqlite:///{DB}", echo=True)

# Create a session factory
Session = sessionmaker(bind=engine)

# Define the base class for our database models
Base = declarative_base()


# Define the model for our OpenAI responses table
class OpenAIPrompt(Base):
    __tablename__ = DATABASE_NAME

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    answer_role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<OpenAIResponse(id={self.id}, question='{self.question}', answer='{self.answer}', created_at='{self.created_at}')>"


# Create the tables in the database
Base.metadata.create_all(engine)
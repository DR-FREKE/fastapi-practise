import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DB_URL = os.environ.get("DATABASE_URL")

# tell sqlite to allow multiple thread to interact with it. ## echo is used to see whatever sql transaction or operation is carried out
engine = create_engine(SQLALCHEMY_DB_URL, connect_args={'check_same_thread': False}, echo=True) # open up a connect by creating an engine

# create a sessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base to use to create database tables and columns and rows
Base: object = declarative_base()

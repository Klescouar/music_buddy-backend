import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_password = os.getenv("AIVEN_PASSWORD")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://avnadmin:{database_password}@music-buddy-lescouarneckevin-d0d0.l.aivencloud.com:21952/defaultdb?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

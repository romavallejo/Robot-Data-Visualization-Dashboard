
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Replace with your actual MySQL credentials
# DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/dbname"
DATABASE_URL = "mysql+pymysql://api:2024@localhost:3306/proyecto"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
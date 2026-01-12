from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
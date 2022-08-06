import os
import sqlalchemy as sa
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB')}"

engine = sa.create_engine(DATABASE_URL)
session = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative.declarative_base()

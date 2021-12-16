import os
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy.ext.automap import automap_base
from config import USERNAME, PASSWORD, DB_URL, DB_PORT, DB_NAME

db_manager = SQLAlchemy()

conn_str = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{DB_URL}:{DB_PORT}/{DB_NAME}"
engine = sqlalchemy.create_engine(conn_str)

metadata = sqlalchemy.MetaData(engine)
metadata.reflect()

Base = automap_base(metadata=metadata)
Base.prepare(engine)

Session = sqlalchemy.orm.sessionmaker(engine)

print("\nDB up and running!\n")

Users = Base.classes.users
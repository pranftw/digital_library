import os
import sqlalchemy
import pymysql
from sqlalchemy.ext.automap import automap_base
from config import USERNAME, PASSWORD, DB_URL, DB_PORT, DB_NAME

conn_str = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{DB_URL}:{DB_PORT}/{DB_NAME}"
engine = sqlalchemy.create_engine(conn_str)

metadata = sqlalchemy.MetaData(engine)
metadata.reflect()

Base = automap_base(metadata=metadata)
Base.prepare(engine)

Session = sqlalchemy.orm.sessionmaker(engine)

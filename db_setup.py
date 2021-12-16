from config import USERNAME, PASSWORD, DB_URL, DB_PORT, DB_NAME

conn_str = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{DB_URL}:{DB_PORT}/{DB_NAME}"
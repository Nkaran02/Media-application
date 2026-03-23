import psycopg2
import time 
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Newpassword%40123@localhost/media'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()



# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost', 
#             database='media', user='postgres', 
#             password='Newpassword@123', 
#             cursor_factory=RealDictCursor
#             )
#         cursor = conn.cursor()
#         print("Database connections was successfull")
#         break
#     except Exception as error:
#         print("Connection failed ", error)
#         time.sleep(2)

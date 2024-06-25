from sqlalchemy import create_engine, Integer, String, Column, inspect
from sqlalchemy.orm import sessionmaker, declarative_base

# Параметры подключения к PostgreSQL
DB_HOST = "127.0.0.1"  # Или IP-адрес Docker контейнера
DB_PORT = "5432"
DB_NAME = "vacans_db"
DB_USER = "vest1ter"
DB_PASSWORD = "vacans_pass"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

Base = declarative_base()

class Test(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    count = Column(Integer)



engine = create_engine(DATABASE_URL)

Session = sessionmaker(engine)

session = Session()

response = session.query(Test.name, Test.count)
print(response.all())
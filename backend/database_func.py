from sqlalchemy import create_engine, Integer, String, Column, inspect, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

# Параметры подключения к PostgreSQL
DB_HOST = "127.0.0.1"  # Или IP-адрес Docker контейнера
DB_PORT = "5432"
DB_NAME = "vacans_db"
DB_USER = "vest1ter"
DB_PASSWORD = "vacans_pass"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(engine)

session = Session()


Base = declarative_base()


class Search(Base):
    __tablename__ = 'search'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(String(255), nullable=False)
    experience = Column(String(255), nullable=False)
    employment = Column(String(255), nullable=False)
    
    vacancies = relationship('Vacancy', back_populates='search')

class Vacancy(Base):
    __tablename__ = 'vacancy'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    offer_link = Column(Text, nullable=False)
    search_id = Column(Integer, ForeignKey('search.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    
    search = relationship('Search', back_populates='vacancies')


Base.metadata.create_all(engine)


def search_vacancies(job_title, experience, employment):
    



def add_search_and_vacancies(job_title, experience, employment):

    new_search = Search(
        job_title=job_title,
        experience=experience,
        employment=employment
    )
    print(job_title, experience, employment)
    try:

        query = session.query(Vacancy).join(Search)
        
        if job_title:
            query = query.filter(Search.job_title == job_title)
        if experience:
            query = query.filter(Search.experience == experience)
        if employment:
            query = query.filter(Search.employment == employment)
        
        all_vacancy = query.all()

        
    except:
        print('database error')
        return ['database error']

    if not all_vacancy:
        try:
            #---
        except:
            return["api error"]

    else:
        return all_vacancy

    # Получаем данные вакансий
    #vacancies_data = search_vacancies(job_title, experience, employment)
    print(all_vacancy)
    

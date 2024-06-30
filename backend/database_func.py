from sqlalchemy import create_engine, Integer, String, Column, inspect, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime, timedelta
from hh_pars import get_vacancies_from_api


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

class Item():
    position_name_: str
    company_name_: str
    offer_link_: str

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

class TestTable(Base):
    __tablename__ = 'test_table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)


def save_vacancies_to_db(searched_vacancy_from_api, params_for_search):

    session.add(params_for_search)
    session.commit()
    
    for this_vacancy in searched_vacancy_from_api:
        new_vacancy = Vacancy(
            title=this_vacancy.get("name"),
            company_name=this_vacancy.get("employer", {}).get("name"),
            offer_link=this_vacancy.get("alternate_url"),
            search_id=params_for_search.id,
            created_at=datetime.utcnow()
        )
        session.add(new_vacancy)
        
    session.commit()

    return 'ok'


def search_vacancies(job_title, experience, employment):

    new_search = Search(
        job_title=job_title,
        experience=experience,
        employment=employment
    )
    print(new_search)
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
        
    except Exception as e:
        print('database error', e)
        return 'database error'

    if not all_vacancy:
        try:
            all_vacancy = get_vacancies_from_api(job_title, experience, employment)
            save_vacancies_to_db(all_vacancy, new_search)
            
            return all_vacancy
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        return all_vacancy


def get_vacancies_from_db(job_title, experience, employment):
    try:

        query = session.query(Vacancy).join(Search)
        
        if job_title:
            query = query.filter(Search.job_title == job_title)
        if experience:
            query = query.filter(Search.experience == experience)
        if employment:
            query = query.filter(Search.employment == employment)
        
        all_vacancy = query.all()

        

        return all_vacancy
        
    except Exception as e:
        print('database error', e)
        return 'database error'

def delete_old_vacancies():
    try:
        # Вычисляем временную метку для проверки
        cutoff_time = datetime.utcnow() - timedelta(seconds=3)
        
        # Находим все записи, которые старше 3 часов
        old_vacancies = session.query(Vacancy).filter(Vacancy.created_at < cutoff_time).all()
        
        # Удаляем найденные записи
        for vacancy in old_vacancies:
            session.delete(vacancy)
        
        # Фиксируем изменения в базе данных
        session.commit()
        
        print(f"Deleted {len(old_vacancies)} old vacancies.")
    except Exception as e:
        print(f"An error occurred while deleting old vacancies: {e}")
        session.rollback()




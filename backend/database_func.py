from sqlalchemy import create_engine, Integer, String, Column, inspect, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
from hh_pars import get_vacancies

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
        
    
    # Сохраняем изменения
    session.commit()


def search_vacancies(job_title, experience, employment):

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
        print('api')
        try:
            all_vacancy = get_vacancies(job_title, experience, employment)
            print(all_vacancy)
            save_vacancies_to_db(all_vacancy, new_search)
            for vacancy in all_vacancy:
            # Extract relevant information from the vacancy object
                vacancy_id = vacancy.get("id")
                vacancy_title = vacancy.get("name")
                vacancy_url = vacancy.get("alternate_url")
                company_name = vacancy.get("employer", {}).get("name")
                print(f"ID: {vacancy_id}\nTitle: {vacancy_title}\nCompany: {company_name}\nURL: {vacancy_url}\n")
        except Exception as e:
            print(f"An error occurred: {e}")
            return["api error"]

    else:
        return all_vacancy

    # Получаем данные вакансий
    #vacancies_data = search_vacancies(job_title, experience, employment)
    #print(all_vacancy)
    

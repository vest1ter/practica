
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from hh_pars import get_vacancies_from_api
from database_func import search_vacancies, get_vacancies_from_db, return_all_vacancies
from jobscheduler import scheduler

app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class SearchRequest(BaseModel):
    position_name: Optional[str]
    employment: Optional[str]
    experience: Optional[int] = None
    city: Optional[str] = None

class Item(BaseModel):
    position_name: str
    company_name: str
    salary: str
    offer_link: str
    

@app.on_event("startup")
def startup_event():
    print("Starting up...")
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    print("Shutting down...")
    scheduler.shutdown()

@app.post("/search/", response_model=List[Item])
async def search_items(search_request: SearchRequest):
    experience_dict = {
        0: "noExperience",
        1: "between1And3",
        2: "between1And3",
        3: "between1And3",
        4: "between3And6",
        5: "between3And6",
        6: "between3And6",
    }
    if search_request.experience == None:
        experience = None
    elif search_request.experience > 6:
        experience = "moreThan6"
    else:
        experience = experience_dict.get(search_request.experience)
    items = get_vacancies_from_db(search_request.position_name, experience, search_request.employment, search_request.city)
    
    vacancy_for_table =[]
    for item in items:
        vacanc_for_table = Item(
            position_name = item.title,
            company_name = item.company_name,
            offer_link = item.offer_link,
            salary = item.salary
        )
        print(vacanc_for_table)
        vacancy_for_table.append(vacanc_for_table)
        
    if not vacancy_for_table:
        raise HTTPException(status_code=404, detail="No items found")
    return vacancy_for_table

@app.post("/count/")
async def count_items(search_request: SearchRequest):
    experience_dict = {
        0: "noExperience",
        1: "between1And3",
        2: "between1And3",
        3: "between1And3",
        4: "between3And6",
        5: "between3And6",
        6: "between3And6",
    }
    if search_request.experience == None:
        experience = None
    elif search_request.experience > 6:
        experience = "moreThan6"
    else:
        experience = experience_dict.get(search_request.experience)
    answer = search_vacancies(search_request.position_name, experience,  search_request.employment, search_request.city)
    print(search_request.position_name, experience,  search_request.employment, search_request.city)
    return len(answer)

@app.get("/vacancies/", response_model=List[Item])
def get_vacancies():
    print("////////")
    all_vacancies_for_wind = return_all_vacancies()
    print(all_vacancies_for_wind)
    return [Item(
        position_name=vacancy_for_wind.position_name,
        company_name=vacancy_for_wind.company_name,
        salary=vacancy_for_wind.salary,
        offer_link=vacancy_for_wind.offer_link
    ) for vacancy_for_wind in all_vacancies_for_wind]


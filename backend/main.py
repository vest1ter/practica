
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from hh_pars import get_vacancies_from_api
from database_func import search_vacancies, get_vacancies_from_db

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
    experience: Optional[int]
    city: Optional[str]

class Item(BaseModel):
    position_name: str
    company_name: str
    offer_link: str



@app.post("/search/", response_model=List[Item])
async def search_items(search_request: SearchRequest):
    items = get_vacancies_from_db(search_request.position_name, f"between{search_request.experience}And3", search_request.employment)
    '''
    results = [item for item in items if 
               (search_request.position_name is None or search_request.position_name in item['position_name']) and
               (search_request.skills is None or search_request.skills in item['skills']) and
               (search_request.experience is None or item['experience'] >= search_request.experience)]
    '''
    vacancy_for_table =[]
    for item in items:
        vacanc_for_table = Item(
            position_name = item.title,
            company_name = item.company_name,
            offer_link = item.offer_link
        )
        print(vacanc_for_table)
        vacancy_for_table.append(vacanc_for_table)
            
    if not vacancy_for_table:
        raise HTTPException(status_code=404, detail="No items found")
    return vacancy_for_table

@app.post("/count/")
async def count_items(search_request: SearchRequest):
    answer = search_vacancies(search_request.position_name,f"between{search_request.experience}And3",  search_request.employment)
    return len(answer)

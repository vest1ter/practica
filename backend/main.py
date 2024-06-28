
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from hh_pars import get_vacancies
from database_func import add_search_and_vacancies

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
    skills: Optional[str]
    experience: Optional[int]

class Item(BaseModel):
    position_name: str
    skills: str
    experience: int

# Пример данных
items = [
    {"position_name": "Backend devoleper", "skills": "Junior", "experience": 2},
    {"position_name": "Frontend devoleper", "skills": "Middle", "experience": 3},
    {"position_name": "ML devoleper", "skills": "Middle", "experience": 2},
    # Добавьте остальные элементы до 20 строк
]

@app.post("/search/", response_model=List[Item])
async def search_items(search_request: SearchRequest):
    results = [item for item in items if 
               (search_request.position_name is None or search_request.position_name in item['position_name']) and
               (search_request.skills is None or search_request.skills in item['skills']) and
               (search_request.experience is None or item['experience'] >= search_request.experience)]
    if not results:
        raise HTTPException(status_code=404, detail="No items found")
    return results

@app.post("/count/", response_model=int)
async def count_items(search_request: SearchRequest):
    '''
    results = [item for item in items if 
               (search_request.position_name is None or search_request.position_name in item['position_name']) and
               (search_request.skills is None or search_request.skills in item['skills']) and
               (search_request.experience is None or item['experience'] >= search_request.experience)]
    '''
    add_search_and_vacancies(str(search_request.position_name),f"between{search_request.experience}And3",  str(search_request.skills))
    
    return 1

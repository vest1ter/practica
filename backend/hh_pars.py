import requests




def get_city_id(city_name):
    url = "https://api.hh.ru/suggests/areas"
    params = {"text": city_name}
    headers = {
        "User-Agent": "application",  # Replace with your User-Agent header
        "Authorization": "Bearer APPLI68BV3G5NE61NV2B51KHSFEDAGHH50DSEHAA1N4Q5LURUVB99NJCTBNJVG19",
    }
    response = requests.get(url, params=params, headers = headers)
    response_data = response.json()
    for item in response_data.get("items", []):
        if item["text"].lower() == city_name.lower():
            return item["id"]
    return None
    

def get_vacancies_from_api(title, experience, employment, area, page=0, per_page=25):
    null = None
    url = "https://api.hh.ru/vacancies"
    area = get_city_id(area)
    params = {
        "text": title,
        "experience": experience,
        "employment": employment,
        "area": area,
        "page": page,
        "per_page": per_page
    }
    headers = {
        "User-Agent": "application",  # Replace with your User-Agent header
        "Authorization": "Bearer APPLI68BV3G5NE61NV2B51KHSFEDAGHH50DSEHAA1N4Q5LURUVB99NJCTBNJVG19",
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        vacancies = data.get("items", [])
        return vacancies
        
    else:
        return [0]


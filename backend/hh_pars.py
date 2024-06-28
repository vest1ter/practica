import requests


def get_vacancies(title, experience, employment, area=1, page=0, per_page=5):
    null = None
    url = "https://api.hh.ru/vacancies"
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
        '''
        for vacancy in vacancies:
            # Extract relevant information from the vacancy object
            vacancy_id = vacancy.get("id")
            vacancy_title = vacancy.get("name")
            vacancy_url = vacancy.get("alternate_url")
            company_name = vacancy.get("employer", {}).get("name")
            print(f"ID: {vacancy_id}\nTitle: {vacancy_title}\nCompany: {company_name}\nURL: {vacancy_url}\n")
        '''
    else:
        return [0]
        #print(f"Request failed with status code: {response.status_code}")
        #print(params)



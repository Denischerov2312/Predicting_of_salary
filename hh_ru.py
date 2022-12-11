import requests


def get_vacancies(language='python'):
    page = 0
    total_pages = 1
    vacancies = []
    while page < total_pages:
        params = {
            'text': f'программист {language}',
            'area': 1,
            'page': page
        }
        url = 'https://api.hh.ru/vacancies/'
        page_response = requests.get(url, params=params)
        page_response.raise_for_status()

        total_pages = page_response.json()['pages']
        page += 1

        for vanancy in page_response.json()['items']:
            vacancies.append(vanancy)
    return vacancies


def predict_rub_salary_for_hh(vacancy):
    salary = vacancy['salary']
    if salary is None or salary['currency'] != 'RUR':
        return None
    salary_from = salary['from']
    salary_to = salary['to']
    if salary_from and salary_to:
        return (salary_to + salary_from) // 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8


def get_vacancies_features(vacancies):
    vacancies_processed = 0
    vacancies_salary_sum = 0
    for vacancy in vacancies:
        if predict_rub_salary_for_hh(vacancy):
            vacancies_salary_sum += predict_rub_salary_for_hh(vacancy)
            vacancies_processed += 1
    average_salary = vacancies_salary_sum // vacancies_processed
    vacancies_features = {
        'found': len(vacancies),
        'processed': vacancies_processed,
        'average_salary': int(average_salary), 
    }
    return vacancies_features


def get_hh_vacancies_features_by_languages():
    languages = ['python', 'JavaScript', 'Java', 'Ruby', 'PHP', 'C++', 'C#', 'Go']
    vacancies_features_by_languages = {}
    for language in languages:
        vacancies = get_vacancies(language)
        vacancies_features = get_vacancies_features(vacancies)
        vacancies_features_by_languages[language] = vacancies_features
    return vacancies_features_by_languages

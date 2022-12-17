import requests

from api_vacancies import predict_rub_salary


def get_vacancies(language='python'):
    page = 0
    total_pages = 1
    vacancies = []
    while page < total_pages:
        Moscow_index = 1
        params = {
            'text': f'программист {language}',
            'area': Moscow_index,
            'page': page
        }
        url = 'https://api.hh.ru/vacancies/'
        page_response = requests.get(url, params=params)
        page_response.raise_for_status()

        response_json = page_response.json()
        total_pages = response_json['pages']
        page += 1

        for vanancy in response_json['items']:
            vacancies.append(vanancy)
    return vacancies


def predict_rub_salary_for_hh(vacancy):
    salary = vacancy['salary']
    if salary and salary['currency'] == 'RUR':
        salary_from = salary['from']
        salary_to = salary['to']
        return predict_rub_salary(salary_from, salary_to)


def calculate_average(sum, processed):
    average_salary = sum // processed if processed > 0 else sum
    return average_salary


def get_vacancies_features(vacancies):
    vacancies_processed = 0
    vacancies_salary_sum = 0
    for vacancy in vacancies:
        predictable_salary = predict_rub_salary_for_hh(vacancy)
        if predictable_salary:
            vacancies_salary_sum += predictable_salary
            vacancies_processed += 1
    average_salary = calculate_average(vacancies_salary_sum, vacancies_processed)
    vacancies_features = {
        'found': len(vacancies),
        'processed': vacancies_processed,
        'average_salary': int(average_salary),
    }
    return vacancies_features


def get_hh_vacancies_features_by_languages():
    languages = [
        'python',
        'JavaScript',
        'Java',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'Go'
        ]
    vacancies_features_by_languages = {}
    for language in languages:
        vacancies = get_vacancies(language)
        vacancies_features = get_vacancies_features(vacancies)
        vacancies_features_by_languages[language] = vacancies_features
    return vacancies_features_by_languages

import requests

from api_vacancies import predict_rub_salary


VERSION = 2.0


def predict_rub_salary_for_superjob(vacancy):
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    if vacancy['currency'] == 'rub':
        return predict_rub_salary(salary_from, salary_to)


def get_vacancies_features(vacancies):
    processed = 0
    salary_sum = 0
    for vacancy in vacancies:
        average_salary = 0
        predictable_salary = predict_rub_salary_for_superjob(vacancy)
        if predictable_salary:
            salary_sum += predictable_salary
            processed += 1
            average_salary = salary_sum // processed
    vacancies_features = {
        'found': len(vacancies),
        'processed': processed,
        'average_salary': average_salary,
    }
    return vacancies_features


def get_superjob_vacancies_features_by_languages(secret_key):
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
        vacancies = get_vacancies(secret_key, language)
        vacancies_features = get_vacancies_features(vacancies)
        vacancies_features_by_languages[language] = vacancies_features
    return vacancies_features_by_languages


def get_vacancies(secret_key, language='python'):
    page = 0
    total_page = 1
    total_vacancies = []
    while page < total_page:
        url = f'https://api.superjob.ru/{VERSION}/vacancies/'
        development_and_programming_index = 48
        params = {
            'count': 100,
            'page': page,
            'catalogues': development_and_programming_index,
            'town': 'Москва',
            'keyword': language,
        }
        headers = {
            'X-Api-App-Id': secret_key,
        }
        page_response = requests.get(url, params=params, headers=headers)
        page_response.raise_for_status()

        vacancies = page_response.json()
        total_page = vacancies['total']
        page += 1
        for vacancy in vacancies['objects']:
            total_vacancies.append(vacancy)
    return total_vacancies

import requests


VERSION = 2.0


def predict_rub_salary_for_superjob(vacancy):
    if vacancy['currency'] == 'rub':
        salary_from = vacancy['payment_from']
        salary_to = vacancy['payment_to']
        if salary_from > 0 and salary_to > 0:
            return (salary_to + salary_from) // 2
        elif salary_from > 0:
            return salary_from * 1.2
        elif salary_to > 0:
            return salary_to * 0.8


def get_vacancies_features(vacancies):
    vacancies_processed = 0
    vacancies_salary_sum = 0
    for vacancy in vacancies:
        average_salary = 0
        if predict_rub_salary_for_superjob(vacancy):
            vacancies_salary_sum += predict_rub_salary_for_superjob(vacancy)
            vacancies_processed += 1
            average_salary = vacancies_salary_sum // vacancies_processed
    vacancies_features = {
        'found': len(vacancies),
        'processed': vacancies_processed,
        'average_salary': int(average_salary),
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
    vacancies = []
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

        total_page = page_response.json()['total']
        page += 1
        for vacancy in page_response.json()['objects']:
            vacancies.append(vacancy)
    return vacancies

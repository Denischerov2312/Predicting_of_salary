import os

from terminaltables import AsciiTable
from dotenv import load_dotenv

from super_Job_ru import get_superjob_vacancies_features_by_languages
from hh_ru import get_hh_vacancies_features_by_languages


def get_table_data(vacancies_features):
    table_data = [
        [
            'Язык программирования',
            'Найдено вакансий',
            'Обработано вакансий',
            'Средняя зарплата'
        ],
    ]
    for language, features in vacancies_features.items():
        line = [
            language,
            features['found'],
            features['processed'],
            features['average_salary']]
        table_data.append(line)
    return table_data


def create_table(table_data, title='Vacancies Moscow'):
    table = AsciiTable(table_data, title)
    return table.table


def show_hh_table():
    vacancies_features = get_hh_vacancies_features_by_languages()
    table_data = get_table_data(vacancies_features)
    print(create_table(table_data, 'HeadHunter Moscow'))


def show_superjob_table(secret_key):
    vacancies_features = get_superjob_vacancies_features_by_languages(secret_key)
    table_data = get_table_data(vacancies_features)
    print(create_table(table_data, 'SuperJob Moscow'))


def main():
    load_dotenv()
    super_job_secret_key = os.environ['SUPERJOB_SECRET_KEY']
    show_superjob_table(super_job_secret_key)
    show_hh_table()


if __name__ == '__main__':
    main()

import json

from src.file_manager import FileManager
from src.vacancy import Vacancy


class JSONFileManager(FileManager):
    '''
    Класс для работы с JSON-файлами
    '''

    def save_to_file(self, filename):
        '''
        Функция сохраняет созданные вакансии на основе
        класса Vacancy в файл
        :param filename: название файла
        '''
        with open(f'files/{filename}.json', 'w', encoding='UTF-8') as file:
            json_data = []
            for vacancy in Vacancy.vacancies:
                data = {}
                data['name'] = vacancy.name
                data['description'] = vacancy.description
                data['area'] = vacancy.area
                data['salary_from'] = vacancy.salary_from
                data['salary_to'] = vacancy.salary_to
                data['salary'] = vacancy.salary
                data['experience'] = vacancy.experience
                data['employer'] = vacancy.employer
                data['employment'] = vacancy.employment
                data['address'] = vacancy.adress

                json_data.append(data)

            file.write(json.dumps(json_data, ensure_ascii=False))

    def load_from_file(self, filename):
        '''
        Функция загружает вакансии из файла, создавая
        объекты на основе класса Vacancy
        :param filename: название файла
        '''
        Vacancy.vacancies.clear()
        with open(f'files/{filename}.json', 'r', encoding='UTF-8') as file:
            json_data = json.load(file)

            # цикл перебирает данные каждой вакансии
            for vacancy in json_data:
                if  vacancy['salary'] == 'Зарплата не указана':
                    currency = 'RUR'
                else:
                    currency = vacancy['salary'].split()[1]
                Vacancy(
                    vacancy['name'],
                    vacancy['description'],
                    vacancy['area'],
                    vacancy['salary_from'],
                    vacancy['salary_to'],
                    currency,
                    vacancy['experience'],
                    vacancy['employer'],
                    vacancy['employment'],
                    vacancy['address']
                )

    def load_vacancies_by_salary(self, filename, value):
        '''
        Функция загружает вакансии из файла по переданой
        пользователем зарплата, создавая объекты на основе
        класса Vacancy
        :param value: зарплата
        :param filename: название файла
        :return: вакансии
        '''
        Vacancy.vacancies.clear()
        with open(f'files/{filename}.json', 'r', encoding='UTF-8') as file:
            json_data = json.load(file)
            user_salary = value.split('-')

            if len(user_salary) == 2 and user_salary[0].isdigit() and user_salary[1].isdigit():

                # цикл перебирает данные каждой вакансии
                for vacancy in json_data:
                    if vacancy['salary'] == 'Зарплата не указана':
                        continue

                    currency = vacancy['salary'].split()[1]

                    # проверка, что зарплата вакансии находится в указаном диапозоне
                    if int(user_salary[0]) <= int(vacancy['salary'].split()[0]) <= int(user_salary[1]):
                        Vacancy(
                            vacancy['name'],
                            vacancy['description'],
                            vacancy['area'],
                            vacancy['salary_from'],
                            vacancy['salary_to'],
                            currency,
                            vacancy['experience'],
                            vacancy['employer'],
                            vacancy['employment'],
                            vacancy['address']
                        )
            else:
                print('Вы ввели неверные данные')

    def load_vacancies_by_area(self, filename, value):
        '''
        Функция загружает вакансии из файла по переданой
        пользователем области поиска, создавая объекты на основе
        класса Vacancy
        :param value: область поиска
        :param filename: название файла
        :return: вакансии
        '''
        Vacancy.vacancies.clear()
        with open(f'files/{filename}.json', 'r', encoding='UTF-8') as file:
            json_data = json.load(file)
            user_area = value

            # цикл перебирает данные каждой вакансии
            for vacancy in json_data:
                if vacancy['salary'] == 'Зарплата не указана':
                    currency = 'RUR'
                else:
                    currency = vacancy['salary'].split()[1]

                # проверка, что город вакансии совпадает с переданным
                if vacancy['area'].lower() == user_area.lower():
                    Vacancy(
                        vacancy['name'],
                        vacancy['description'],
                        vacancy['area'],
                        vacancy['salary_from'],
                        vacancy['salary_to'],
                        currency,
                        vacancy['experience'],
                        vacancy['employer'],
                        vacancy['employment'],
                        vacancy['address']
                    )

    def delete_vacancy(self, filename, value):
        '''
        Удаляет вакансию из файла по переданому
        номеру вакансии
        :param value: номер вакансии
        :param filename: название файла
        '''
        with open(f'files/{filename}.json', 'r+', encoding='UTF-8') as file:
            try:
                json_data = json.load(file)
                del json_data[value - 1]
                file.seek(0)
                file.truncate()
                file.write(json.dumps(json_data, ensure_ascii=False))
            except IndexError:
                print('Вакансии с таким номером не существует')

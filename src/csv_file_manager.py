import csv

from src.file_manager import FileManager
from src.vacancy import Vacancy


class CSVFileManager(FileManager):
    '''
    Класс для работы с CSV-файлами
    '''

    def save_to_file(self, filename):
        '''
        Функция сохраняет созданные вакансии на основе
        класса Vacancy в файл
        :param filename: название файла
        '''
        with open(f'files/{filename}.csv', 'w', encoding='UTF-8') as file:
            writer = csv.writer(file, lineterminator="\r")
            writer.writerow([
                'название', 'описание', 'место', 'мин.зарплата', 'макс.зарплата',
                'зарплата', 'опыт', 'работадатель', 'занятость', 'адрес'
            ])

            for vacancy in Vacancy.vacancies:
                writer.writerow([
                    vacancy.name, vacancy.description, vacancy.area,
                    vacancy.salary_from, vacancy.salary_to, vacancy.salary,
                    vacancy.experience, vacancy.employer, vacancy.employment,
                    vacancy.adress
                ])

    def load_from_file(self, filename):
        '''
        Функция загружает вакансии из файла, создавая
        объекты на основе класса Vacancy
        :param filename: название файла
        '''
        try:
            with open(f'files/{filename}.csv', 'r', encoding='UTF-8') as file:
                reader = csv.reader(file)
                for row in reader:

                    # проверяет является ли ряд названием колонок
                    if row[0] == 'название':
                        continue

                    # проверяет указана ли зарплата для установки валюты
                    if row[5] != 'Зарплата не указана':
                        row[5] = row[5].split()[1]
                    else:
                        row[5] = 'RUR'

                    Vacancy(
                        row[0],
                        row[1],
                        row[2],
                        int(row[3]),
                        int(row[4]),
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                        row[9]
                    )
        except FileNotFoundError:
            print("Такого файла не существует!")

    def load_vacancies_by_salary(self, filename, value):
        '''
        Функция загружает вакансии из файла по переданой
        пользователем зарплата, создавая объекты на основе
        класса Vacancy
        :param value: зарплата
        :param filename: название файла
        :return: вакансии
        '''
        try:
            with open(f'files/{filename}.csv', 'r', encoding='UTF-8') as file:
                reader = csv.reader(file)
                user_salary = value.split('-')

                if len(user_salary) == 2 and user_salary[0].isdigit() and user_salary[1].isdigit():
                    for row in reader:

                        # проверяет является ли ряд названием колонок
                        if row[0] == 'название':
                            continue

                        # проверяет указана ли зарплата для установки валюты
                        if row[5] == 'Зарплата не указана':
                            continue
                        else:
                            salary = row[5].split()[0]
                            row[5] = row[5].split()[1]

                        if int(user_salary[0]) <= int(salary) <= int(user_salary[1]):
                            Vacancy(
                                row[0],
                                row[1],
                                row[2],
                                int(row[3]),
                                int(row[4]),
                                row[5],
                                row[6],
                                row[7],
                                row[8],
                                row[9]
                            )
                else:
                    print('Вы ввели некоректные данные')
        except FileNotFoundError:
            print('Такого файла не существует!')

    def load_vacancies_by_area(self, filename, value):
        '''
        Функция загружает вакансии из файла по переданой
        пользователем области поиска, создавая объекты на основе
        класса Vacancy
        :param value: область поиска
        :param filename: название файла
        :return: вакансии
        '''
        try:
            with open(f'files/{filename}.csv', 'r', encoding='UTF-8') as file:
                reader = csv.reader(file)
                user_area = value

                for row in reader:

                    # проверяет является ли ряд названием колонок
                    if row[0] == 'название':
                        continue

                    # проверяет указана ли зарплата для установки валюты
                    if row[5] != 'Зарплата не указана':
                        row[5] = row[5].split()[1]
                    else:
                        row[5] = 'RUR'

                    if row[2].lower() == user_area.lower():
                        Vacancy(
                            row[0],
                            row[1],
                            row[2],
                            int(row[3]),
                            int(row[4]),
                            row[5],
                            row[6],
                            row[7],
                            row[8],
                            row[9]
                        )
        except FileNotFoundError:
            print('Такого файла не существует!')

    def delete_vacancy(self, filename, value):
        '''
        Удаляет вакансию из файла по переданому
        номеру вакансии
        :param value: номер вакансии
        :param filename: название файла
        '''
        try:
            with open(f'files/{filename}.csv', 'r+', encoding='UTF-8') as file:
                reader = csv.reader(file)
                writer = csv.writer(file, lineterminator="\r")
                rows = []
                for row in reader:
                    rows.append(row)
                if int(value) > 0 and int(value) <= len(rows):
                    del rows[int(value)]
                    file.seek(0)
                    file.truncate()
                    for row in rows:
                        writer.writerow(row)
                else:
                    print('Вы ввели некоректные данные')
        except FileNotFoundError:
            print('Такого файла не существует!')

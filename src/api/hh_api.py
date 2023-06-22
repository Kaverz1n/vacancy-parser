import requests

from src.api.api import API
from src.vacancy import Vacancy


class HHAPI(API):
    '''
    Класс для работы с API сайта
    https://hh.ru/
    '''

    def __init__(self):
        '''
        Параметры для поиска вакансий
        '''
        self.__api = 'https://api.hh.ru'
        self.search_params = None
        self.__area = None
        self.__experience = None
        self.__currency = None
        self.__only_with_salary = False
        self.__salary = None
        self.__page = 0
        self.__per_page = 100

    def __str__(self):
        return 'API сайта https://hh.ru/'

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def __get_all_vacancies(self):
        '''
        Возвращает список всех найденных вакансий
        :return: список найденных вакансий
        '''
        vacancies = []

        # цикл, перебирающий все вакансии по переданным параметрам
        while True:
            response = requests.get(
                url=f'{self.__api}/vacancies',
                params={
                    "text": self.search_params,
                    "experience": self.__experience,
                    "area": self.__area,
                    "only_with_salary": self.__only_with_salary,
                    "currency": self.__currency,
                    "salary": self.__salary,
                    "page": self.__page,
                    "per_page": self.__per_page
                }
            ).json()

            # выход из цикла, если вакансии закончились
            try:
                if self.__page == response['pages']:
                    break
            except KeyError:
                break

            self.__page += 1

            vacancies.append(response['items'])

        return vacancies

    def get_vacancies(self):
        '''
        Cоздаёт объекты (вакансии) на
        основе класса Vacancy по переданным параметрам
        пользователя
        '''

        vacancies = self.__get_all_vacancies()

        # цикл, перебирающий все вакансии
        for obj in vacancies:
            # цикл, перебирающий все элементы вакансии
            for item in obj:

                vacancy_name = item['name']

                try:
                    # удаление лишних хайлайтов
                    requirement = item['snippet']['requirement']
                    vacancy_requirement = requirement.replace('<highlighttext>', '').replace('</highlighttext>', '')
                except AttributeError:
                    vacancy_requirement = 'Отсутсвует'

                try:
                    vacancy_responsibility = item['snippet']['responsibility']
                except AttributeError:
                    vacancy_responsibility = 'Отсутствует'

                vacancy_description = f'{vacancy_requirement} {vacancy_responsibility}'
                vacancy_area = item['area']['name']

                # проверка на то, что у вакансии указана зарплата
                if item['salary'] is None:
                    vacancy_salary_from = 0
                    vacancy_salary_to = 0
                    vacancy_currency = ''
                else:
                    vacancy_salary_from = item['salary']['from']
                    vacancy_salary_to = item['salary']['to']
                    vacancy_currency = item['salary']['currency']

                vacancy_experience = item['experience']['name']
                vacancy_employer = item['employer']['name']
                vacancy_employment = item['employment']['name']
                vacancy_address = item['address']

                # проверка на то, что у вакансии указан адрес
                if vacancy_address is None:
                    vacancy_address = 'Адресс не указан'
                else:
                    if item['address']['raw'] is None:
                        vacancy_address = 'Адресс не указан'
                    else:
                        vacancy_address = item['address']['raw']

                # устанавливает мин. зарплату 0, если её значение None
                if vacancy_salary_from is None:
                    vacancy_salary_from = 0

                # устанавливает макс. зарплату 0, если её значение None
                if vacancy_salary_to is None:
                    vacancy_salary_to = 0

                # проверяет соответсвует ли валюта указаной, если тип зарплаты True(зарплата указана)
                if vacancy_currency != self.__currency and self.__only_with_salary is True:
                    continue

                # создание вакансии на основе экземпляра класса Vacancy
                Vacancy(
                    vacancy_name,
                    vacancy_description,
                    vacancy_area,
                    vacancy_salary_from,
                    vacancy_salary_to,
                    vacancy_currency,
                    vacancy_experience,
                    vacancy_employer,
                    vacancy_employment,
                    vacancy_address
                )

    @property
    def experience(self):
        '''
        Возвращает значение необходимого
        опыта для получения вакансии
        :return: опыт
        '''
        experiences = requests.get(url=f'{self.__api}/dictionaries').json()['experience']

        # перебирает словарь с опытом для получения вакансии
        for experience in experiences:
            if experience['id'] == self.__experience:
                return experience['name']
        return None

    @experience.setter
    def experience(self, value):
        '''
        Устанавливает id опыта для получения
        вакансии
        :param value: номер опыта из списка
        '''
        experiences = requests.get(url=f'{self.__api}/dictionaries').json()['experience']

        try:
            # перебирает словарь с опытом для получения вакансии
            for experience in experiences:
                if experiences.index(experience) + 1 == int(value):
                    self.__experience = experience['id']
        except ValueError:
            self.__currency = None

    @property
    def area(self):
        '''
        Возвращает значение области поиска
        вакансий
        :return: область поиска
        '''
        countries = requests.get(url=f'{self.__api}/areas').json()

        # цикл перебирает регионы страны Россия
        for country in countries[0]['areas']:
            if country['id'] == self.__area:
                return country['name']

            # цикл перебирает города в областях
            for city in country['areas']:
                if city['id'] == self.__area:
                    return city['name']
        return self.__area

    @area.setter
    def area(self, value):
        '''
        Устанавливает id области
        поиска вакансий
        :param value: область поиска
        '''
        countries = requests.get(url=f'{self.__api}/areas').json()

        # цикл перебирает регионы страны Россия
        for country in countries[0]['areas']:
            if country['name'] == value.title():
                self.__area = country['id']
                break
            # цикл перебирает города в регионах
            for city in country['areas']:
                if city['name'] == value.title():
                    self.__area = city['id']
                    break

    @property
    def only_with_salary(self):
        '''
        Возвращает значение типа зарплаты вакансии
        (True - зарплата указана, False - зарплата не указана)
        :return: bool-тип зарплаты
        '''
        if self.__only_with_salary:
            return 'Зарплата указана'
        return 'Зарплата не указана'

    @only_with_salary.setter
    def only_with_salary(self, value):
        '''
        Устанавливает значения типа зарплаты вакансии,
        взависимости от ответа пользователя(Если "да", то
        True, иначе деффолтное значение False)
        :param value: ответ пользователя
        '''
        if value.lower() == 'да':
            self.__only_with_salary = True

    @property
    def currency(self):
        '''
        Выводит значение выбранной пользователем
        валюты
        :return: аббревиатура валюты
        '''
        return self.__currency

    @currency.setter
    def currency(self, value):
        '''
        Устанавливает валюту, относительно выбраного числа
        :param value: выбранное число пользователем
        '''
        currencies = requests.get(url=f'{self.__api}/dictionaries').json()['currency']

        try:
            # перебирает словарь с валютами
            for currency in currencies:
                if currencies.index(currency) + 1 == int(value):
                    self.__currency = currency['code']
                    break
                else:
                    self.__currency = 'RUR'
        except ValueError:
            self.__currency = 'RUR'

    @property
    def salary(self):
        '''
        Возвращает значение желаемой зарплаты,
        переданной пользователем
        :return: значение зарплаты
        '''
        return self.__salary

    @salary.setter
    def salary(self, value):
        '''
        Устанавливает значение желаемой зарплаты,
        если оно больше 0 и является числом
        :param value: значение желаемой зарплаты
        '''
        try:
            if int(value) > 0:
                self.__salary = value
        except ValueError:
            self.__salary = None



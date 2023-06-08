import requests

from src.api import API


class HHAPI(API):
    '''
    Класс для работы с API сайта
    https://hh.ru/
    '''

    def __init__(self):
        '''
        Параметры для поиска вакансий
        '''
        self.__api = 'https://api.hh.ru/vacancies'
        self.search_params = None
        self.__experience = None
        self.__area = None
        self.__currency = None
        self.__only_with_salary = False
        self.__salary = None

    def __str__(self):
        return 'API сайта https://hh.ru/'

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def get_vacancies(self):
        '''
        Возвращает список вакансий, созданных на
        основе класса Vacancy по переданным параметрам
        пользователя
        :return: список объектов класса Vacancy
        '''
        vacancies = requests.get(
            url=self.__api,
            params={
                "text": self.search_params,
                "experience": self.__experience,
                "area": self.__area,
                "only_with_salary": self.__only_with_salary,
                "currency": self.__currency,
                "salary": self.__salary
            }
        ).json()

        return vacancies

    @property
    def experience(self):
        '''
        Возвращает значение необходимого
        опыта для получения вакансии
        :return: опыт
        '''
        experiences = requests.get(url='https://api.hh.ru/dictionaries').json()['experience']

        # перебирает словарь с опытом для получения вакансии
        for experience in experiences:
            if experience['id'] == self.__experience:
                return experience['name']

    @experience.setter
    def experience(self, value):
        '''
        Устанавливает id опыта для получения
        вакансии
        :param value: номер опыта из списка
        '''
        experiences = requests.get(url='https://api.hh.ru/dictionaries').json()['experience']

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
        countries = requests.get(url='https://api.hh.ru/areas').json()

        # цикл перебирает регионы страны Россия
        for country in countries[0]['areas']:
            if country['id'] == self.__area:
                return country['name']

            # цикл перебирает города в областях
            for city in country['areas']:
                if city['id'] == self.__area:
                    return city['name']

    @area.setter
    def area(self, value):
        '''
        Устанавливает id области
        поиска вакансий
        :param value: область поиска
        '''
        countries = requests.get(url='https://api.hh.ru/areas').json()

        # цикл перебирает регионы страны Россия
        for country in countries[0]['areas']:
            if country['name'] == value.title():
                self.__area = country['id']

            # цикл перебирает города в регионах
            for city in country['areas']:
                if city['name'] == value.title():
                    self.__area = city['id']

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
        currencies = requests.get(url='https://api.hh.ru/dictionaries').json()['currency']

        try:
            # перебирает словарь с валютами
            for currency in currencies:
                if currencies.index(currency) + 1 == int(value):
                    self.__currency = currency['code']
        except ValueError:
            self.__currency = None

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
        except:
            self.__salary = 0
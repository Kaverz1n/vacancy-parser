import requests

from abc import ABC, abstractmethod


class API(ABC):
    '''
    Абстрактный класс для работы с api
    сайтов с вакансиями
    '''

    @abstractmethod
    def __init__(self):
        '''
        Параметры для поиска вакансий
        '''
        self.__api = None
        self.search_params = None
        self.__experience = None
        self.__area = None
        self.currency = None
        self.__only_with_salary = False
        self.salary = None

    @abstractmethod
    def get_vacancies(self):
        '''
        Возвращает список вакансий, созданных на
        основе класса Vacancy по переданным параметрам
        пользователя
        :return: список объектов класса Vacancy
        '''
        pass

    @property
    @abstractmethod
    def experience(self):
        '''
        Возвращает значение необходимого
        опыта для получения вакансии
        :return: опыт
        '''
        pass

    @experience.setter
    @abstractmethod
    def experience(self, value):
        '''
        Устанавливает значение опыта для
        получения вакансии
        :param value: 'id' опыта
        '''
        pass

    @property
    @abstractmethod
    def area(self):
        '''
        Возвращает значение области поиска
        вакансий
        :return: область поиска
        '''
        pass

    @area.setter
    @abstractmethod
    def area(self, value):
        '''
        Устанавливает значения области поиска
        вакансий
        :param value: 'id' области поиска
        '''
        pass

    @property
    @abstractmethod
    def only_with_salary(self):
        '''
        Возвращает значение типа зарплаты вакансии
        (True - зарплата указана, False - зарплата не указана)
        :return: bool-тип зарплаты
        '''
        pass

    @only_with_salary.setter
    @abstractmethod
    def only_with_salary(self, value):
        pass


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
        self.currency = None
        self.__only_with_salary = False
        self.salary = None

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
                "currency": self.currency,
                "only_with_salary": self.only_with_salary,
                "salary": self.salary
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
        Устанавливает значение опыта для
        получения вакансии
        :param value: номер опыта
        '''
        experiences = requests.get(url='https://api.hh.ru/dictionaries').json()['experience']

        # перебирает словарь с опытом для получения вакансии
        for experience in experiences:
            if experiences.index(experience) + 1 == value:
                self.__experience = experience['id']

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
        return self.__only_with_salary

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

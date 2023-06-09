import requests

from src.api.api import API
from src.vacancy import Vacancy
from src.api.tokens import token_SJ


class SJAPI(API):
    '''
    Класс для работы с API сайта
    https://superjob.ru/
    '''

    def __init__(self):
        '''
        Параметры для поиска вакансий
        '''
        self.token = token_SJ
        self.__api = 'https://api.superjob.ru/2.0'
        self.search_params = None
        self.__area = None
        self.__experience = None
        self.__only_with_salary = 0
        self.__salary = None
        self.__page = 0
        self.__count = 100

    def __str__(self):
        return 'API сайта https://superjob.ru/'

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def __get_all_vacancies(self):
        '''
        Возвращает список всех найденных вакансий
        :return: список найденных вакансий
        '''
        vacancies = []

        while True:
            response = requests.get(
                url=f'{self.__api}/vacancies',
                headers=self.token,
                params={
                    "keyword": self.search_params,
                    "experience": self.__experience,
                    "town": self.__area,
                    "no_agreement": self.__only_with_salary,
                    "payment_from": self.__salary,
                    "page": self.__page,
                    "count": self.__count
                }
            ).json()

            if len(response['objects']) == 0:
                break

            self.__page += 1
            vacancies.append(response['objects'])

        return vacancies

    def get_vacancies(self):
        '''
        Возвращает список вакансий, созданных на
        основе класса Vacancy по переданным параметрам
        пользователя
        :return: список объектов класса Vacancy
        '''
        vacancies = self.__get_all_vacancies()

        # цикл, перебирающий все вакансии
        for obj in vacancies:
            # цикл, перебирающий все элементы вакансии
            for item in obj:

                vacancy_name = item['profession']
                try:
                    vacancy_description = item['candidat']
                except AttributeError:
                    vacancy_description = 'Отсутсвует'

                vacancy_area = item['town']['title']
                vacancy_salary_from = item['payment_from']
                vacancy_salary_to = item['payment_to']
                vacancy_currency = 'RUR'
                vacancy_experience = item['experience']['title']

                try:
                    vacancy_employer = item['client']['title']
                except KeyError:
                    vacancy_employer = 'Неизвестно'

                vacancy_employment = item['type_of_work']['title']
                vacancy_address = item['address']

                # проверка на то, что у вакансии указан адрес
                if vacancy_address is None:
                    vacancy_address = 'Адресс не указан'
                else:
                    vacancy_address = item['address']

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

        return Vacancy.vacancies

    @property
    def experience(self):
        '''
        Возвращает значение необходимого
        опыта для получения вакансии
        :return: опыт
        '''
        experiences = requests.get(url=f'{self.__api}/references').json()['experience']

        if self.__experience in experiences:
            return experiences[self.__experience]
        else:
            return self.__experience


    @experience.setter
    def experience(self, value):
        '''
        Устанавливает id опыта для
        получения вакансии
        :param value: номер опыта
        '''
        experiences = requests.get(url=f'{self.__api}/references').json()['experience']

        if value in experiences:
            self.__experience = value

    @property
    def area(self):
        '''
        Возвращает значение области поиска
        вакансий
        :return: область поиска
        '''
        return self.__area

    @area.setter
    def area(self, value):
        '''
        Устанавливает область поиска
        вакансий
        :param value: область поиска
        '''
        self.__area = value.title()

    @property
    def only_with_salary(self):
        '''
        Возвращает значение типа зарплаты вакансии
        (1 - зарплата указана, иное число - зарплата не указана)
        :return: str-тип зарплаты
        '''
        if self.__only_with_salary == 1:
            return 'Зарплата указана'
        return 'Зарплата не указана'

    @only_with_salary.setter
    def only_with_salary(self, value):
        '''
        Устанавливает значение типа зарплаты вакансии
        (1 - зарплата указана, иное число - зарплата не указана)
        :param value: str-тип
        '''
        if value.lower() == 'да':
            self.__only_with_salary = 1

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



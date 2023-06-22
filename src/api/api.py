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
        self.__only_with_salary = False
        self.__salary = None
        self.__page = 0
        self.__per_page = 20

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
        Устанавливает id опыта для
        получения вакансии
        :param value: опыт
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
        Устанавливает id области поиска
        вакансий
        :param value: область поиска
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
        '''
        Устанавливает значение типа зарплаты вакансии
        (True - зарплата указана, False - зарплата не указана)
        :param value: bool-тип
        '''
        pass

    @property
    @abstractmethod
    def salary(self):
        '''
        Возвращает значение желаемой зарплаты,
        переданной пользователем
        :return: значение зарплаты
        '''
        pass

    @salary.setter
    @abstractmethod
    def salary(self, value):
        '''
        Устанавливает значение желаемой зарплаты,
        если оно больше 0 и является числом
        :param value: значение желаемой зарплаты
        '''
        pass



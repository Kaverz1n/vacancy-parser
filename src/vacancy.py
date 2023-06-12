class Vacancy:
    '''
    Класс вакансий
    '''

    def __init__(
            self, name, requirement, responsibility,
            area, salary_from, salary_to,
            currency, experience, employer,
            employment, address,
    ):
        '''
        Информация по вакансии
        :param name: название вакансии
        :param requirement: требования
        :param responsibility: обязаности
        :param area: местоположение
        :param salary_from: минимальная зарплата
        :param salary_to: максимальная зарплата
        :param currency: валюта
        :param experience: опыт
        :param employer: работадатель
        :param employment: занятость
        :param address: адрес
        '''
        self.name = name
        self.__requirement = requirement
        self.__responsibility = responsibility
        self.__area = area
        self.__salary_from = salary_from
        self.__salary_to = salary_to
        self.__currency = currency
        self.__experience = experience
        self.employer = employer
        self.__employment = employment
        self.__address = address

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.__requirement},' \
               f'{self.__responsibility}, {self.__area}, {self.__salary_from},' \
               f'{self.__salary_to}, {self.__currency}, {self.experience},' \
               f'{self.employer}, {self.__employment}, {self.adress}'

    def __str__(self):
        return f'Вакансия {self.name}'

    @property
    def description(self):
        '''
        Возвращает информацию о вакансии
        :return: информация вакансии
        '''
        return f'ТРЕБОВАНИЯ:\n{self.__requirement}\nИНФОРМАЦИЯ:\n{self.__responsibility}'

    @property
    def area(self):
        '''
        Возвращает местоположение вакансии
        :return: местоположение
        '''
        return self.__area

    @property
    def salary(self):
        '''
        Возвращает среднюю зарплату вакансии
        :return: средняя зарплата
        '''
        if (self.__salary_from + self.__salary_to) == 0:
            return 'Зарплата не указана'

        if self.__salary_from == 0:
            return f'{self.__salary_to} {self.__currency}'

        if self.__salary_to == 0:
            return f'{self.__salary_from} {self.__currency}'

        salary = int((self.__salary_from + self.__salary_to) / 2)
        return f'{salary} {self.__currency}'

    @property
    def experience(self):
        '''
        Возвращает требуемый опыт вакансии
        :return: требуемый опыт
        '''
        return self.__experience

    @property
    def employment(self):
        '''
        Возвращает занятость вакансии
        :return: занятость
        '''
        return self.__employment

    @property
    def adress(self):
        '''
        Возвращает адрес вакансии
        :return: адрес вакансии
        '''
        return self.__address

    def get_information(self):
        '''
        Возвращает полную информацию о вакансии
        :return:
        '''
        return f'Вакансия {self.name}, с зарплатой {self.salary}\n' \
               f'{self.description}\nНаходится в городе: ' \
               f'{self.area} по адресу: {self.adress}\nТребует опыт: ' \
               f'{self.experience} и занятость: {self.employment}\n' \
               f'Работадатель: {self.employer}'

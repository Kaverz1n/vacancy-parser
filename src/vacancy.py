class Vacancy:
    '''
    Класс вакансий
    '''
    vacancies = []

    def __init__(
            self, name, description, area,
            salary_from, salary_to, currency,
            experience, employer, employment,
            address
    ):
        '''
        Информация по вакансии
        :param name: название вакансии
        :param description: описание вакансии
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
        self.__description = description
        self.__area = area
        self.__salary_from = salary_from
        self.__salary_to = salary_to
        self.__currency = currency
        self.__experience = experience
        self.employer = employer
        self.__employment = employment
        self.__address = address

        Vacancy.vacancies.append(self)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.__description},' \
               f'{self.__area}, {self.__salary_from},' \
               f'{self.__salary_to}, {self.__currency}, {self.experience},' \
               f'{self.employer}, {self.__employment}, {self.adress}'

    def __str__(self):
        return f'Вакансия {self.name}'

    def __eq__(self, other):
        '''
        Метод сравнивает зарплаты двух вакансий
        :param other: вакансия с которой сравнивают
        :return: результат
        '''
        try:
            if self.salary.split()[0] == other.salary.split()[0]:
                return 'Зарплаты одинаковы'
            else:
                return 'Зарплаты не равны'
        except ValueError:
            return 'Указаны неверные объекты или у одного из объектов отсутсвует зарплата'

    def __lt__(self, other):
        '''
        Метод проверяет является ли зарплата первой вакансии
        меньше, чем зарплата второй вакансии
        :param other: вакансия с которой сравнивают
        :return: результат
        '''
        try:
            first_salary = int(self.salary.split()[0])
            second_salary = int(other.salary.split()[0])

            if first_salary < second_salary:
                difference = second_salary - first_salary
                return f'{other.name} больше на {difference} {other.salary.split()[1]}'
            else:
                difference = first_salary - second_salary
                return f'{self.name} больше на {difference} {self.salary.split()[1]}'
        except ValueError:
            return 'Указаны неверные объекты или у одного из объектовотсутсвует зарплата'

    def __le__(self, other):
        '''
        Метод проверяет является ли зарплата первой вакансии
        меньше или равна, чем зарплата второй вакансии
        :param other: вакансия с которой сравнивают
        :return: результат
        '''
        try:
            first_salary = int(self.salary.split()[0])
            second_salary = int(other.salary.split()[0])

            if first_salary == second_salary:
                return 'Зарплаты равны'
            else:
                return self.__lt__(other)
        except ValueError:
            return 'Указаны неверные объекты или у одного из объектовотсутсвует зарплата'

    def __gt__(self, other):
        '''
        Метод проверяет является ли зарплата первой вакансии
        больше, чем зарплата второй вакансии
        :param other: вакансия с которой сравнивают
        :return: результат
        '''
        try:
            first_salary = int(self.salary.split()[0])
            second_salary = int(other.salary.split()[0])

            if first_salary > second_salary:
                difference = first_salary - second_salary
                return f'{other.name} больше на {difference} {other.salary.split()[1]}'
            else:
                difference = second_salary - first_salary
                return f'{self.name} больше на {difference} {self.salary.split()[1]}'
        except ValueError:
            return 'Указаны неверные объекты или у одного из объектовотсутсвует зарплата'

    def __ge__(self, other):
        try:
            first_salary = int(self.salary.split()[0])
            second_salary = int(other.salary.split()[0])

            if first_salary == second_salary:
                return 'Зарплаты равны'
            else:
                return self.__gt__(other)

        except ValueError:
            return 'Указаны неверные объекты или у одного из объектовотсутсвует зарплата'

    @property
    def description(self):
        '''
        Возвращает информацию о вакансии
        :return: информация вакансии
        '''
        return f'Информация: {self.__description}'

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
    def salary_from(self):
        '''
        Возвращает минимальную зарплату вакансии
        :return: минимальная зарплата вакансии
        '''
        return self.__salary_from

    @property
    def salary_to(self):
        '''
        Возвращает максимальную зарплату вакансии
        :return: максимальная зарплата вакансии
        '''
        return self.__salary_to

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

    @classmethod
    def get_min_salary_vacancy(cls):
        '''
        Метод выводит минимальную зарплату. Использовать, если
        у всех вакансий одинаковая валюта и указана зарплата
        :return:
        '''
        min_salary = int(cls.vacancies[0].salary.split()[0]) if cls.vacancies else None
        min_vacancy = cls.vacancies[0] if cls.vacancies else None
        for vacancy in cls.vacancies:
            try:
                if int(vacancy.salary.split()[0]) < min_salary:
                    min_salary = int(vacancy.salary.split()[0])
                    min_vacancy = vacancy
            except ValueError:
                continue

        return min_vacancy

    @classmethod
    def get_max_salary_vacancy(cls):
        '''
        Метод выводит максимальную зарплату. Использовать, если
        у всех вакансий одинаковая валюта и указана зарплата
        :return:
        '''
        max_salary = int(cls.vacancies[0].salary.split()[0]) if cls.vacancies else None
        min_vacancy = cls.vacancies[0] if cls.vacancies else None
        for vacancy in cls.vacancies:
            try:
                if int(vacancy.salary.split()[0]) > max_salary:
                    max_salary = int(vacancy.salary.split()[0])
                    min_vacancy = vacancy
            except ValueError:
                continue

        return min_vacancy

    @classmethod
    def get_all_vacancies(cls):
        '''
        Возвращает пронумерованный список всех вакансий
        :return: пронумерованный список всех вакансий
        '''
        all_vacancies = ''
        for num, vacancy in enumerate(cls.vacancies, start=1):
            all_vacancies += f'{num} - {vacancy.name}, {vacancy.salary}\n'

        return all_vacancies

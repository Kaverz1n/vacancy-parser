from abc import ABC, abstractmethod


class FileManager(ABC):
    '''
    Класс для работы с файлами
    '''

    @abstractmethod
    def save_to_file(self, filename):
        '''
        Функция сохраняет созданные вакансии на основе
        класса Vacancy в файл
        :param filename: название файла
        '''
        pass

    @abstractmethod
    def load_from_file(self, filename):
        '''
        Функция загружает вакансии из файла, создавая
        объекты на основе класса Vacancy
        :param filename: название файла
        '''
        pass

    @abstractmethod
    def load_vacancies_by_salary(self, filename, value):
        '''
        Функция загружает вакансии из файла по переданой
        пользователем зарплата, создавая объекты на основе
        класса Vacancy
        :param filename: название файла
        :param value: зарплата
        :return: вакансии
        '''
        pass

    @abstractmethod
    def load_vacancies_by_area(self, filename, value):
        '''
        Функция загружает вакансии из файла по переданой
        пользователем области поиска, создавая объекты на основе
        класса Vacancy
        :param filename: название файла
        :param value: область поиска
        :return: вакансии
        '''
        pass

    @abstractmethod
    def delete_vacancy(self, filename, value):
        '''
        Удаляет вакансию из файла по переданому
        номеру вакансии
        :param value: номер вакансии
        :param filename: название файла
        '''
        pass

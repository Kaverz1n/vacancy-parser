import requests

from src.api.hh_api import HHAPI
from src.api.sj_api import SJAPI
from src.file_managers.json_file_manager import JSONFileManager
from src.file_managers.excel_file_manager import ExcelFileManager
from src.file_managers.csv_file_manager import CSVFileManager
from src.vacancy import Vacancy


def menu():
    '''
    Функция запускает стартовое меню программы
    '''
    while True:
        try:
            answer = int(input(
                'Добрый день, что желаете сделать?\n'
                '0 - Выход\n'
                '1 - Найти вакансии\n'
                '2 - Получить вакансии из файла\n'
            ))
            if answer == 0:
                quit()
            elif answer == 1:
                find_vacancy_menu()
            elif answer == 2:
                load_file_menu()
            else:
                print('Вы указали неверное значение!')
        except ValueError:
            print('Вы указали неверное значение!')


def find_vacancy_menu():
    '''
    Функция выводит найденные вакансии, по переданным
    параметрам пользователя, на экран
    '''
    api_list = [HHAPI(), SJAPI()]
    while True:
        try:
            answer = int(input(
                'На какой платформе желаете искать вакансии?\n'
                '0 - Назад\n'
                '1 - HeadHunter\n'
                '2 - SuperJob\n'
            ))
            if answer == 0:
                menu()

            if 1 <= answer <= 2:
                api = api_list[answer - 1]
                break
            else:
                print('Вы указали неверное значение!')
        except ValueError:
            print('Вы указали неверное значение!')

    print(
        'Сейчас вам необходимо заполнить все данные. Если вы НЕ хотите заполнять '
        'какой-либо пункт, то просто оставьте его пустым, нажав ENTER.\n'
        'Если вы укажите какое-либо неверное или неизвестное значение, то параметру '
        'будет присвоено стандартное значение.'
    )

    api.search_params = input('Введите название вакансии: ')
    api.area = input('Введите город: ')
    api.experience = input(
        'Укажите опыт вакансии:\n'
        '1 - Нет опыта\n'
        '2 - От 1 до 3 лет\n'
        '3 - От 3 до 6\n'
        '4 - От 6 лет\n'
    )

    if isinstance(api, HHAPI):
        print('Укажите номер валюты: ')
        currencies = requests.get(url='https://api.hh.ru/dictionaries').json()['currency']
        for num, currency in enumerate(currencies, start=1):
            print(f'{num} - {currency["abbr"]}')
        api.currency = input()

    api.only_with_salary = input('Показывать вакансии с указаной зарплатой?(Да/Нет): ')
    api.salary = input(
        'Укажите желаемую зарплату (Вам будут представлены вакансии со средней зарплатой, если '
        'переданое значение входит в диапазон зарплаты вакансии): '
    )
    api.get_vacancies()
    print(f'Найденные вакансии:\n{Vacancy.get_all_vacancies()}')
    if Vacancy.get_all_vacancies() == 'Вакансий не найдено!':
        menu()
    save_vacancies_menu()


def load_file_menu():
    '''
    Функция для работы с тремя видами файловых менеджеров
    Позволяет получать данные из файлов JSON, Excel, CSV
    '''
    file_managers = [JSONFileManager(), ExcelFileManager(), CSVFileManager()]
    while True:
        while True:
            try:
                answer = int(input(
                    'В каком формате у вас хранятся файлы?\n'
                    '0 - Назад\n'
                    '1 - JSON\n'
                    '2 - Excel\n'
                    '3 - CSV\n'
                ))
                if answer == 0:
                    menu()
                if 1 <= answer <= 3:
                    file_manager = file_managers[answer - 1]
                    break
                else:
                    print("Вы указали неверное значение")
            except ValueError:
                print('Вы указали неверное значение!')

        user_file_name = input('Укажите имя файла, из которого желаете получить данные: ')
        result = file_manager.load_from_file(user_file_name)

        print(result)
        if result != 'Такого файла не существует!':
            get_info_from_file(file_manager, user_file_name)


def get_info_from_file(f_manager, f_name):
    '''
    ИСПОЛЬЗОВАТЬ ВМЕСТЕ С ФУНКЦИЕЙ load_file_menu
    Получает всю необходимую информацию из файл по
    определённым критериям
    :param f_manager: выбранный файловый менеджер
    :param f_name: имя файла
    '''
    file_manager = f_manager
    file_name = f_name
    user_decision = None
    while True:
        try:
            answer = int(input(
                'Что вы хотите сделать с файлом?\n'
                '0 - Назад\n'
                '1 - Вывести вакансии по переданной зарплате\n'
                '2 - Вывести вакансии по переданому городу\n'
                '3 - Сортировать вакансии по зарплате и вывести\n'
                '4 - Удалить вакансию из файла\n'
            ))
            if answer == 0:
                menu()
            if 1 <= answer <= 4:
                user_decision = answer
                break
            else:
                print("Вы указали неверное значение")
        except ValueError:
            print('Вы указали неверное значение!')

    if user_decision == 1:
        while True:
            user_salary = input('Укажите зарплату через знак "-" (напр. 13000-1000000): ')
            result = file_manager.load_vacancies_by_salary(file_name, user_salary)
            print(result)
            if result != 'Вы ввели неверные данные!':
                break

    elif user_decision == 2:
        user_area = input('Введите название города: ')
        result = file_manager.load_vacancies_by_area(file_name, user_area)
        print(result)

    elif user_decision == 3:
        Vacancy.sort_vacancies()
        print(Vacancy.get_all_vacancies())

    elif user_decision == 4:
        while True:
            vacancy_num = int(input('Укажите номер вакансии: '))
            result = file_manager.delete_vacancy(file_name, vacancy_num)
            print(result)
            if result != 'Вакансии с таким номером не существует' and result != 'Вы ввели некоректные данные':
                break

    if 1 <= user_decision <= 3:
        user_input = input('Желаете сохранить изменения в файл?(Да/Нет): ')
        if user_input.lower() == 'да':
            save_vacancies_menu()


def save_vacancies_menu():
    '''
    Сохраняет данные найденных вакансий в файл определенного
    формата - JSON, Excel, CSV
    '''
    file_managers = [JSONFileManager(), ExcelFileManager(), CSVFileManager()]
    while True:
        try:
            answer = int(input(
                'В какой формат вы хотите сохранить данные?\n'
                '0 - Назад\n'
                '1 - JSON\n'
                '2 - Excel\n'
                '3 - CSV\n'
            ))
            if answer == 0:
                menu()
            if 1 <= answer <= 3:
                file_manager = file_managers[answer - 1]
                break
            else:
                print("Вы указали неверное значение")
        except ValueError:
            print('Вы указали неверное значение!')

    user_file_name = input('Придумайте имя файла: ')
    file_manager.save_to_file(user_file_name)
    print('Данные успешно сохранены и находятся в папке files!')
    menu()




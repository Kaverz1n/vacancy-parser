# ПРОЕКТ ПАРСЕР ВАКАНСИЙ
___
## ОПИСАНИЕ
Программное решение на языке Python для сбора и систематизации информации о вакансиях с различных платформ в России. 
Проект основан на использовании API и включает разработку абстрактного класса для работы с API сайтов с вакансиями, 
класса для представления вакансий, а также классов для сохранения информации в различных форматах 
файлов (JSON, CSV, Excel). Пользователь имеет возможность взаимодействовать с программой через консоль, 
выполняя различные операции с вакансиями, такие как фильтрация, сортировка, добавление и удаление. Реализация проекта 
осуществляется в парадигме ООП и удовлетворяет принципам SOLID. Для сбора 
вакансий используются API платформ hh.ru и superjob.ru. Информация о вакансиях сохраняется в JSON-файл и отображается 
пользователю через консоль.

## Используются API сайтов
+ https://hh.ru/
+ https://superjob.ru/

## Поддерживаемые форматы файлов
+ JSON
+ EXCEL
+ CSV

## Принцип работы

1. Запустить файла **main.py**
2. Выбрать действие (1 - Поиск вакансий, 2 - Загрузка вакансий из файла)
3. Получить данные 
4. Сохранить их в удобный формат


## Данные для поиска вакансий

Каждый параметр является **необязательным**, т.е. его **можно** пропустить, и тогда значение параметра 
выставиться стандартное.

| Номер | Параметры вакансии                 |
|------:|------------------------------------|
|     1 | Название                           |
|     2 | Город                              |
|     3 | Опыт                               |
|     4 | Валюта (если выбран HH.ru)         |
|     5 | Только с зарплатой ("Да" или "Нет") |
|     6 | Желаемая зарплата                  |


## Сохранение данных
После успешного поиска вакансий, полученные данные можно сохранить в удобный формат (**JSON**,
**EXCEL**, **CSV**). При загрузки данных из файла, пользователь вправе перезаписать данные в 
другой вышесказанный формат. 

Все сохранённые данные хранятся в папке **src/files**



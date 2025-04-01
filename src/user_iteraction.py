from typing import Any

from src.dbmanager import DBManager


def user_iteraction() -> Any:
    """Функция взаимодействия с пользователем."""
    db_manager = DBManager()
    try:
        user_answer = int(
            input(
                "Какие данные о работодателях и их вакансиях вы хотите получить? Введите необходимую цифру из меню.\n"
                "1. Получить список всех компаний и количество вакансий у каждой компании.\n"
                "2. Получить список всех вакансий.\n"
                "3. Получить среднюю зарплату по вакансиям.\n"
                "4. Получить список вакансий с зарплатой выше средней.\n"
                "5. Получить список всех вакансий по ключевому слову.\n"
                "6. Выйти\n"
            )
        )
        if user_answer == 1:
            companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print("Список всех компаний и количество вакансий у каждой компании:")
            for i in companies_and_vacancies_count:
                print(i)
        elif user_answer == 2:
            all_vacancies = db_manager.get_all_vacancies()
            print("Список всех вакансий:")
            for i in all_vacancies:
                print(i)
        elif user_answer == 3:
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакасиям: {avg_salary}")
        elif user_answer == 4:
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print("Список всех вакансий с зарплатой выше средней:")
            for i in vacancies_with_higher_salary:
                print(i)
        elif user_answer == 5:
            keyword = input("Введите ключевое слово для поиска вакансий: \n")
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
            print("Список всех вакансий по ключевому слову:")
            for i in vacancies_with_keyword:
                print(i)
        elif user_answer == 6:
            print("Выход из меню.")
        else:
            print("Некорректный запрос.")
    except ValueError:
        print("Некорректный запрос.")

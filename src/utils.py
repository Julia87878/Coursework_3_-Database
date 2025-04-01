import os

import psycopg2
from dotenv import load_dotenv


def create_db() -> str:
    """Создание базы данных для хранения информации о работодателях и их вакансиях."""
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv("host"), port=os.getenv("port"), user=os.getenv("user"), password=os.getenv("password")
    )
    conn.autocommit = True
    cur = conn.cursor()

    load_dotenv()
    name = os.getenv("database")
    cur.execute(f"DROP DATABASE IF EXISTS {name}")
    cur.execute(f"CREATE DATABASE {name}")
    conn.commit()
    conn.close()
    return "База данных создана."


def create_tables() -> str:
    """Проектирование таблиц в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях."""
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv("host"),
        port=os.getenv("port"),
        database=os.getenv("database"),
        user=os.getenv("user"),
        password=os.getenv("password"),
    )
    with conn.cursor() as cur:
        cur.execute(
            """
             DROP TABLE IF EXISTS employers CASCADE;
             CREATE TABLE employers(
                employer_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                employer_url TEXT NOT NULL,
                open_vacancies_count INT
           )
         """
        )
        conn.commit()
    conn.close()

    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv("host"),
        port=os.getenv("port"),
        database=os.getenv("database"),
        user=os.getenv("user"),
        password=os.getenv("password"),
    )
    with conn.cursor() as cur:
        cur.execute(
            """
             DROP TABLE IF EXISTS vacancies;
             CREATE TABLE vacancies (
                 vacancy_id SERIAL PRIMARY KEY,
                 name VARCHAR NOT NULL,
                 salary_from INT,
                 salary_to INT,
                 vacancy_url TEXT,
                 employer_id INT REFERENCES employers(employer_id)
             )
        """
        )
        conn.commit()
    conn.close()
    return "Таблицы спроектированы в базе данных."


def load_data_in_employers(my_employers: list[dict]) -> str:
    """Заполнение данных о работодателях в таблицу employers."""
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv("host"),
        port=os.getenv("port"),
        database=os.getenv("database"),
        user=os.getenv("user"),
        password=os.getenv("password"),
    )

    with conn.cursor() as cur:
        for emp in my_employers:
            emp_id = emp.get("id")
            emp_name = emp.get("name")
            emp_url = emp.get("url")
            emp_open_vacancies = emp.get("open vacancies", 0)
            cur.execute(
                """
                    INSERT INTO employers (employer_id, name, employer_url, open_vacancies_count)
                    VALUES (%s, %s, %s, %s)""",
                (int(emp_id), str(emp_name), str(emp_url), int(emp_open_vacancies)),
            )

            conn.commit()
    conn.close()
    return "Таблица employers в базе данных заполнена."


def load_data_in_vacancies(my_vacancies: list[dict]) -> str:
    """Заполнение данных о вакансиях в таблицу vacancies."""
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv("host"),
        port=os.getenv("port"),
        database=os.getenv("database"),
        user=os.getenv("user"),
        password=os.getenv("password"),
    )
    with conn.cursor() as cur:
        for vacancy in my_vacancies:
            vacancy_id = vacancy.get("vacancy_id")
            name = vacancy.get("name")
            salary_from = vacancy.get("salary").get("from", 0)
            salary_to = vacancy.get("salary").get("to", 0)
            vacancy_url = vacancy.get("url")
            employer_id = vacancy.get("employer_id")
            cur.execute(
                """
                    INSERT INTO vacancies (vacancy_id, name, salary_from, salary_to, vacancy_url, employer_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (vacancy_id, name, salary_from, salary_to, vacancy_url, employer_id),
            )
            conn.commit()
    conn.close()
    return "Таблица vacancies в базе данных заполнена."

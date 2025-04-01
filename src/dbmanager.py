import os

import psycopg2
from dotenv import load_dotenv


class DBManager:
    """Класс, который будет подключаться к БД PostgreSQL"""

    def __init__(self) -> None:
        load_dotenv()
        self.conn = psycopg2.connect(
            host=os.getenv("host"),
            port=os.getenv("port"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password"),
        )

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Метод, который получает список всех компаний и количество вакансий у каждой компании."""
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                """SELECT employers.employer_id, employers.name, COUNT(vacancies.vacancy_id) AS vacancy_count FROM 
                employers LEFT JOIN vacancies ON employers.employer_id=vacancies.employer_id GROUP BY 
                employers.employer_id, employers.name ORDER BY employers.name"""
            )
            result = cur.fetchall()
            conn.commit()
        conn.close()
        return result

    def get_all_vacancies(self) -> list[tuple]:
        """Метод, который получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и
        ссылки на вакансию."""
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                """SELECT employers.name, vacancies.name, salary_from, vacancy_url FROM vacancies
                            LEFT JOIN employers ON vacancies.employer_id=employers.employer_id"""
            )
            result = cur.fetchall()
            conn.commit()
        conn.close()
        return result

    def get_avg_salary(self) -> float:
        """Метод, который получает среднюю зарплату по вакансиям."""
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary_from) FROM vacancies""")
            avg_salary = cur.fetchall()
            conn.commit()
        conn.close()
        return avg_salary

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Метод, который получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                """SELECT employers.name, vacancies.name, salary_from, vacancy_url FROM vacancies
                LEFT JOIN employers ON vacancies.employer_id=employers.employer_id
                WHERE salary_from > (SELECT avg(salary_from) FROM vacancies WHERE salary_from != 0)"""
            )
            vacancies = cur.fetchall()
            conn.commit()
        conn.close()
        return vacancies

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Метод, который получает список всех вакансий, в названии которых содержатся переданные в метод слова,
        например менеджер."""
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                f"""SELECT employers.name, vacancies.name, salary_from, vacancy_url FROM vacancies
        LEFT JOIN employers ON vacancies.employer_id=employers.employer_id WHERE vacancies.name ILIKE '%{keyword}%'"""
            )
            result = cur.fetchall()
            conn.commit()
        conn.close()
        return result

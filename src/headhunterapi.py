import json
from typing import Any

import requests


class HeadHunterAPI:
    """Класс для работы с платформой hh.ru, подключается к API и получает данные о работодателях и их вакансиях."""

    def __init__(self) -> None:
        """Инициализирует класс HeadHunterAPI и задает начальные параметры."""
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {}
        self.__employers = []
        self.__vacancies = []

    def _connect_to_api(self, url: str) -> Any:
        """Метод, который подключается к API(HeadHunter)."""
        response = requests.get(url, headers=self.__headers, params=self.__params)
        if response.status_code != 200:
            raise ValueError("Ошибка.")
        else:
            return response.json()

    def get_employers(self, filepath) -> list:
        """Метод, который получает данные о работодателях с сайта hh.ru."""
        employers_url = "https://api.hh.ru/employers"
        self.__params = {
            "sort_by": "by_vacancies_open",
            "text": "",
            "page": 0,
            "per_page": 100,
            "only_with_vacancies": "only_with_vacancies",
        }
        employers = []
        response = self._connect_to_api(employers_url)
        for employer in response["items"]:
            employer = {
                "id": int(employer["id"]),
                "name": employer["name"],
                "url": employer["url"],
                "open_vacancies": employer.get("open_vacancies", 0),
            }
            employers.append(employer)
        employers_2 = []
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for i in data:
                for emp in employers:
                    if i == emp.get("id", 0):
                        employers_2.append(emp)
            self.__employers.extend(employers_2)
            my_employers = self.__employers
            return my_employers

    def get_employer_vacancies(self, my_employers: list) -> list:
        """Метод, который получает данные о вакансиях работодателей с сайта hh.ru."""
        vacancies_url = "https://api.hh.ru/vacancies"
        employer_ids = [employer.get("id") for employer in my_employers]
        self.__params = {"page": 0, "per_page": 100, "text": "", "employer_id": employer_ids}
        vacancies = []
        response = self._connect_to_api(vacancies_url)
        for v in response["items"]:
            if v["salary"] and v["salary"]["currency"] == "RUR":
                vacancy = {
                    "vacancy_id": v["id"],
                    "name": v["name"],
                    "salary": v["salary"],
                    "url": v["alternate_url"],
                    "employer_id": v["employer"]["id"],
                }
                vacancies.append(vacancy)
        self.__vacancies.extend(vacancies)
        my_vacancies = self.__vacancies
        return my_vacancies

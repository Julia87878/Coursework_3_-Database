from typing import Any

from src import settings
from src.headhunterapi import HeadHunterAPI
from src.user_iteraction import user_iteraction
from src.utils import create_db, create_tables, load_data_in_employers, load_data_in_vacancies


def main() -> Any:
    """Главная функция для запуска работы всего проекта."""
    hh = HeadHunterAPI()
    my_employers = hh.get_employers(filepath=settings.BASE_DIR.joinpath("data", "employers_id_list.json"))
    my_vacancies = hh.get_employer_vacancies(my_employers)
    create_db()
    create_tables()
    load_data_in_employers(my_employers)
    load_data_in_vacancies(my_vacancies)
    user_iteraction()


if __name__ == "__main__":
    main()

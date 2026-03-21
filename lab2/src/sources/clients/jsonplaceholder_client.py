import requests
from typing import Iterable
from datetime import datetime


class JsonPlaceholderClient:
    """
    Клиент для API JsonPlaceholder.
    Получает todos и приводит к универсальному формату.
    """

    def __init__(self, url: str):
        """
        Инициализация.
        :param url: URL API JsonPlaceholder
        """

        if not isinstance(url, str):
            raise TypeError('URL должен являться строкой.')
        self.url = url

    def get_raw_tasks(self) -> Iterable[tuple[int, str, str, str, datetime]]:
        """
        Преобразует данные из API JsonPlaceholder в универсальный формат.
        :return: Итерируемая коллекция с данными для задач.
        """

        try:
            resp = requests.get(self.url)
            resp.raise_for_status()
        except requests.RequestException:
            raise RuntimeError("Ошибка при запросе к API")

        json_tasks = resp.json()
        if not isinstance(json_tasks, list):
            raise TypeError('API вернул некорректные данные')

        for t in json_tasks:
            if not isinstance(t, dict):
                raise TypeError('Некорректный элемент в ответе API')
            yield (
                t['id'],
                t['title'],
                'medium',
                'done' if t['completed'] else 'new',
                datetime.now()
            )

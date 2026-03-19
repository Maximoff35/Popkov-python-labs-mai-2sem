from typing import Iterable
from src.task import Task
import requests

class ApiSource:
    """
    Источник задач.
    Получает задачи из реального внешнего API.
    """

    def __init__(self, url: str):
        """
        Инициализация.
        :param url: URL внешнего API
        """
        self.url = url

    def get_tasks(self) -> Iterable[Task]:
        """
        Получает данные из API и преобразует их в объекты Task.
        :return: Итерируемая коллекция объектов Task
        """

        resp = requests.get(self.url, timeout=5)
        resp.raise_for_status()
        api_tasks = resp.json()

        for t in api_tasks:
            yield Task(t['id'], {
                "userId": t["userId"],
                "title": t["title"],
                "completed": t["completed"]
            })
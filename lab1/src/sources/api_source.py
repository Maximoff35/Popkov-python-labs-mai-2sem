from typing import Iterable
from src.task import Task

class ApiSource:
    """
    Источник задач.
    Эмулирует получение задач из внешнего API.
    """

    def __init__(self):
        self._api_response = [
            {'id': 1515, 'payload': {'from': 'api', 'type': 'test', 'priority': 'high'}},
            {'id': 1516, 'payload': {'from': 'api', 'type': 'test', 'priority': 'mid'}},
            {'id': 1517, 'payload': {'from': 'api', 'type': 'test', 'priority': 'low'}},
        ]

    def get_tasks(self) -> Iterable[Task]:
        """
        Возвращает задачи из API-заглушки.
        :return: Итерируемая коллекция объектов Task
        """
        for t in self._api_response:
            yield Task(t['id'], t['payload'])
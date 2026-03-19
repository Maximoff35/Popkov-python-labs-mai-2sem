from src.task import Task
from typing import Iterable

class GeneratorSource:
    """
    Класс для генерации задач
    """
    def __init__(self, count: int):
        """
        Инициализация.
        :param count: Количество задач
        """
        self.count = count

    def get_tasks(self) -> Iterable[Task]:
        """
        Метод для генерации задач, соответствующий протоколу TaskSource
        :return: Генератор с задачами
        """
        for i in range(self.count):
            yield Task(i, {'базовая информация': f'сгенерированная задача {i}'})


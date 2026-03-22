from src.task import Task, constants
from typing import Iterable
from random import choice
from datetime import datetime


class GeneratorSource:
    """
    Класс для генерации задач
    """

    def __init__(self, count: int):
        """
        Инициализация.
        :param count: Количество задач
        """

        if not isinstance(count, int) or count <= 0:
            raise ValueError('Количество задач должно быть целым числом.')
        self.count = count

    def get_tasks(self) -> Iterable[Task]:
        """
        Метод для генерации задач, соответствующий протоколу TaskSource
        :return: Генератор с задачами
        """

        for i in range(self.count):
            yield Task(
                i + 1,
                f'Описание задачи №{i + 1}',
                choice(constants.ALLOWED_PRIORITIES),
                choice(constants.ALLOWED_STATUSES),
                datetime.now()
            )

from typing import Iterable
from src.task import Task
from src.contracts import ApiClient


class ApiSource:
    """
    Источник задач.
    Получает задачи из реального внешнего API.
    """

    def __init__(self, client: ApiClient):
        """
        Инициализация.
        :param client: Клиент API
        """

        if isinstance(client, ApiClient):
            self.client = client
        else:
            raise TypeError('Клиент API не соответствует формату.')

    def get_tasks(self) -> Iterable[Task]:
        """
        Получает данные от клиента и преобразует их в объекты Task.
        :return: Итерируемая коллекция объектов Task
        """

        for task_data in self.client.get_raw_tasks():
            if not isinstance(task_data, tuple) or len(task_data) != 5:
                raise TypeError('Невозможно создать задачу из данных клиента API.')
            yield Task(*task_data)

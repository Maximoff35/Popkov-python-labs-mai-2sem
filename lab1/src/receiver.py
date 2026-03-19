from src.task import Task
from src.contracts import TaskSource
from typing import List

def collect_tasks(source: TaskSource) -> List[Task]:
    """
    Функция для приема задач. Проверяет источник на соответствие протоколу TaskSource
    :param source: Источник задач
    :return: Список с задачами
    """
    if not isinstance(source, TaskSource):
        raise TypeError('Объект не реализует протокол TaskSource')

    tasks = source.get_tasks()
    try:
        return list(tasks)
    except TypeError:
        raise TypeError("get_tasks должен возвращать Iterable")
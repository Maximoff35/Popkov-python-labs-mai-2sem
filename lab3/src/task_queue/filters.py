from collections.abc import Iterable, Iterator
from src.task import Task


def filter_by_status(tasks: Iterable[Task], status: str) -> Iterator[Task]:
    """
    Лениво фильтрует задачи по статусу.
    :param tasks: Итерируемая коллекция задач.
    :param status: Статус для фильтрации.
    :return: Итератор по задачам с указанным статусом.
    """

    for task in tasks:
        if task.status == status:
            yield task


def filter_by_priority(tasks: Iterable[Task], priority: str) -> Iterator[Task]:
    """
    Лениво фильтрует задачи по приоритету.
    :param tasks: Итерируемая коллекция задач.
    :param priority: Приоритет для фильтрации.
    :return: Итератор по задачам с указанным приоритетом.
    """

    for task in tasks:
        if task.priority == priority:
            yield task


def filter_ready_tasks(tasks: Iterable[Task]) -> Iterator[Task]:
    """
    Лениво фильтрует готовые к выполнению задачи.
    :param tasks: Итерируемая коллекция задач.
    :return: Итератор по готовым к выполнению задачам.
    """

    for task in tasks:
        if task.is_ready:
            yield task


def filter_completed_tasks(tasks: Iterable[Task]) -> Iterator[Task]:
    """
    Лениво фильтрует выполненные задачи.
    :param tasks: Итерируемая коллекция задач.
    :return: Итератор по выполненным задачам.
    """

    for task in tasks:
        if task.is_completed:
            yield task
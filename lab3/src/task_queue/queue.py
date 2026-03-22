from src.task import Task
from src.task_queue.queue_exceptions import InvalidTaskError
from src.task_queue.filters import (
    filter_by_status,
    filter_by_priority,
    filter_ready_tasks,
    filter_completed_tasks
)
from collections.abc import Iterable, Iterator


class TaskQueue:
    """
    Очередь задач.
    Хранит объекты Task, поддерживает повторяемую итерацию,
    базовые операции добавления задач.
    """

    def __init__(self, tasks: Iterable[Task] | None = None) -> None:
        """
        Инициализирует очередь задач.
        :param tasks: Итерируемая коллекция задач.
        :raises InvalidTaskError: Если среди переданных элементов есть не Task.
        """

        self._tasks: list[Task] = []

        if tasks is not None:
            self.extend(tasks)

    def __iter__(self) -> Iterator[Task]:
        """
        Возвращает итератор по задачам очереди.
        :return: Итератор по объектам Task.
        """

        return iter(self._tasks)

    def __len__(self) -> int:
        """
        Возвращает количество задач в очереди.
        :return: Целое число - длина очереди.
        """

        return len(self._tasks)

    def __repr__(self) -> str:
        """
        Возвращает строковое представление очереди.
        :return: Строка вида TaskQueue(size=...).
        """

        return f'TaskQueue(size={len(self)})'

    def add_task(self, task: Task) -> None:
        """
        Добавляет одну задачу в очередь.
        :param task: Объект задачи.
        :raises InvalidTaskError: Если переданный объект не является Task.
        """

        self._validate_task(task)
        self._tasks.append(task)

    def extend(self, tasks: Iterable[Task]) -> None:
        """
        Добавляет в очередь несколько задач.
        :param tasks: Итерируемая коллекция задач.
        :raises InvalidTaskError: Если хотя бы один элемент коллекции не является Task.
        """

        for task in tasks:
            self.add_task(task)

    def __contains__(self, item: object) -> bool:
        """
        Проверяет наличие задачи в очереди.
        Можно передать объект Task или id задачи.
        :param item: Объект Task или id задачи.
        :return: True, если задача есть в очереди, иначе - False.
        """

        if isinstance(item, Task):
            return item in self._tasks
        if isinstance(item, int):
            return any(task.id == item for task in self)
        return False

    @staticmethod
    def _validate_task(task: object) -> None:
        """
        Проверяет, что задача является объектом Task.
        :param task: Проверяемый объект
        :raises InvalidTaskError: Если переданный объект не является Task.
        """

        if not isinstance(task, Task):
            raise InvalidTaskError('Очередь может содержать только объекты Task.')

    def filter_by_status(self, status: str) -> Iterator[Task]:
        """
        Лениво фильтрует задачи по статусу.
        :param status: Статус для фильтрации.
        :return: Итератор по задачам с указанным статусом.
        """

        return filter_by_status(self, status)

    def filter_by_priority(self, priority: str) -> Iterator[Task]:
        """
        Лениво фильтрует задачи по приоритету.
        :param priority: Приоритет для фильтрации.
        :return: Итератор по задачам с указанным приоритетом.
        """

        return filter_by_priority(self, priority)

    def filter_ready_tasks(self) -> Iterator[Task]:
        """
        Лениво фильтрует готовые к выполнению задачи.
        :return: Итератор по готовым к выполнению задачам.
        """

        return filter_ready_tasks(self)

    def filter_completed_tasks(self) -> Iterator[Task]:
        """
        Лениво фильтрует выполненные задачи.
        :return: Итератор по выполненным задачам.
        """

        return filter_completed_tasks(self)
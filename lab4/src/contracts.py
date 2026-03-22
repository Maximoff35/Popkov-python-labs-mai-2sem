from typing import Protocol, runtime_checkable, Iterable
from datetime import datetime
from src.task import Task

@runtime_checkable
class TaskSource(Protocol):
    """
    Контракт источника задач.
    Источником задач считаем любой объект, реализующий метод get_tasks(),
    который возвращает итерируемый объект с задачами Task.
    """
    def get_tasks(self) -> Iterable[Task]:
        """
        Метод, возвращающий задачи в виде итерируемого объекта
        """
        ...


@runtime_checkable
class ApiClient(Protocol):
    """
    Контракт для клиента API.
    """
    def get_raw_tasks(self) -> Iterable[tuple[int, str, str, str, datetime]]:
        """
        Метод, который возвращает необходимые для задач данные из API
        """
        ...


@runtime_checkable
class TaskHandler(Protocol):
    """
    Контракт для обработчика задач.
    Любой обработчик должен уметь асинхронно обработать одну задачу.
    """

    async def handle(self, task: Task) -> None:
        """
        Обрабатывает одну задачу.
        :param task: Задача - объект Task
        """
        ...
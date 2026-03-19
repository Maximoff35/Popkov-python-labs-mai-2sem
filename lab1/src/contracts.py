from typing import Protocol, runtime_checkable, Iterable
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

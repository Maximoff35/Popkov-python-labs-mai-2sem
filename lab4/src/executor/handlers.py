import asyncio
from src.task import Task
from src.executor.executor_exceptions import TaskAlreadyInProgressError


class LowPriorityTaskHandler:
    """
    Обработчик задач с низким приоритетом.
    """

    async def handle(self, task: Task) -> None:
        """
        Асинхронно обрабатывает задачу с низким приоритетом
        :param task: Объект задачи.
        """
        if task.is_completed:
            return
        if not task.is_ready:
            raise TaskAlreadyInProgressError(
                f'Задача id={task.id} уже находится в обработке.'
            )
        task.status = 'in_progress'
        await asyncio.sleep(0.5)
        task.status = 'done'


class MediumPriorityTaskHandler:
    """
    Обработчик задач со средним приоритетом.
    """

    async def handle(self, task: Task) -> None:
        """
        Асинхронно обрабатывает задачу со средним приоритетом
        :param task: Объект задачи.
        """
        if task.is_completed:
            return
        if not task.is_ready:
            raise TaskAlreadyInProgressError(
                f'Задача id={task.id} уже находится в обработке.'
            )
        task.status = 'in_progress'
        await asyncio.sleep(1)
        task.status = 'done'


class HighPriorityTaskHandler:
    """
    Обработчик задач с высоким приоритетом.
    """

    async def handle(self, task: Task) -> None:
        """
        Асинхронно обрабатывает задачу с высоким приоритетом
        :param task: Объект задачи.
        """
        if task.is_completed:
            return
        if not task.is_ready:
            raise TaskAlreadyInProgressError(
                f'Задача id={task.id} уже находится в обработке.'
            )
        task.status = 'in_progress'
        await asyncio.sleep(1.5)
        task.status = 'done'
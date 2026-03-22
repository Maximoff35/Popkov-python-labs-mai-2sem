import asyncio
from src.task import Task
from src.executor.executor_exceptions import TaskAlreadyInProgressError
from src.executor.constants import TASK_PROCESSED, TASK_SKIPPED


class LowPriorityTaskHandler:
    """
    Обработчик задач с низким приоритетом.
    """

    async def handle(self, task: Task) -> str:
        """
        Асинхронно обрабатывает задачу с низким приоритетом
        :param task: Объект задачи.
        """
        if task.is_completed:
            return TASK_SKIPPED
        if not task.is_ready:
            raise TaskAlreadyInProgressError(
                f'Задача id={task.id} уже находится в обработке.'
            )
        task.status = 'in_progress'
        await asyncio.sleep(0.5)
        task.status = 'done'
        return TASK_PROCESSED


class MediumPriorityTaskHandler:
    """
    Обработчик задач со средним приоритетом.
    """

    async def handle(self, task: Task) -> str:
        """
        Асинхронно обрабатывает задачу со средним приоритетом
        :param task: Объект задачи.
        """
        if task.is_completed:
            return TASK_SKIPPED
        if not task.is_ready:
            raise TaskAlreadyInProgressError(
                f'Задача id={task.id} уже находится в обработке.'
            )
        task.status = 'in_progress'
        await asyncio.sleep(1)
        task.status = 'done'
        return TASK_PROCESSED


class HighPriorityTaskHandler:
    """
    Обработчик задач с высоким приоритетом.
    """

    async def handle(self, task: Task) -> str:
        """
        Асинхронно обрабатывает задачу с высоким приоритетом
        :param task: Объект задачи.
        """
        if task.is_completed:
            return TASK_SKIPPED
        if not task.is_ready:
            raise TaskAlreadyInProgressError(
                f'Задача id={task.id} уже находится в обработке.'
            )
        task.status = 'in_progress'
        await asyncio.sleep(1.5)
        task.status = 'done'
        return TASK_PROCESSED
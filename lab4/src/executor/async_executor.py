from src.contracts import TaskHandler
from src.task import Task
from typing import Iterable
from src.executor.executor_exceptions import (
    HandlerNotFoundError,
    InvalidHandlerError,
    TaskExecutionError,
    InvalidTaskError
)
from src.executor.logger import get_logger
from src.executor.constants import TASK_PROCESSED, TASK_SKIPPED


logger = get_logger(__name__)


class TaskExecutor:
    """
    Асинхронный исполнитель задач.
    Выбирает подходящий обработчик по приоритету задачи, запускает ее обработку.
    """

    def __init__(self, queue: Iterable[Task], handlers: dict[str, TaskHandler]) -> None:
        """
        Инициализация.
        :param queue: Очередь задач.
        :param handlers: Словарь обработчиков по приоритету.
        """
        self.queue = queue
        self.handlers = handlers

    def _get_handler(self, task: Task) -> TaskHandler:
        """
        Возвращает обработчик для задачи по ее приоритету.
        :param task: Объект Task.
        :raises HandlerNotFoundError: Если обработчик не найден.
        :raises InvalidHandlerError: Если обработчик не соответствует контракту.
        """
        handler = self.handlers.get(task.priority)
        if handler is None:
            raise HandlerNotFoundError(f'Для приоритета {task.priority} обработчик не найден.')
        if not isinstance(handler, TaskHandler):
            raise InvalidHandlerError(f'Обработчик для приоритета {task.priority} не соответствует контракту.')
        return handler

    async def run(self) -> None:
        """
        Асинхронно запускает обработку всех задач из очереди.
        """
        for t in self.queue:
            try:
                if not isinstance(t, Task):
                    raise InvalidTaskError('Невалидная задача.')
                handler = self._get_handler(t)
                logger.info(f'Начата обработка задачи id={t.id}, priority={t.priority}.')
                result = await handler.handle(t)
                if result == TASK_PROCESSED:
                    logger.info(f'Завершена обработка задачи id={t.id}, status={t.status}.')
                elif result == TASK_SKIPPED:
                    logger.warning(f'Задача id={t.id} пропущена, status={t.status}.')
                else:
                    logger.warning(f'Задача id={t.id} вернула неизвестный результат: {result}.')
            except TaskExecutionError as error:
                logger.error(f'Ошибка обработки задачи id={t.id}: {error}')
            except Exception:
                logger.exception(f'Непредвиденная ошибка при обработке задачи id={t.id}')


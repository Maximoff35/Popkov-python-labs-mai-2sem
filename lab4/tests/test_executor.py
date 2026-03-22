import asyncio
import logging
from datetime import datetime
import pytest
from src.task import Task
from src.executor import TaskExecutor
from src.executor.handlers import (
    LowPriorityTaskHandler,
    MediumPriorityTaskHandler,
    HighPriorityTaskHandler,
)
from src.executor.resources import TaskExecutionContext
from src.executor.logger import get_logger
from src.executor.executor_exceptions import (
    HandlerNotFoundError,
    InvalidHandlerError,
)
from src.executor.constants import TASK_PROCESSED, TASK_SKIPPED
import src.executor.handlers as handlers_module
import src.executor.async_executor as async_executor_module


def make_task(
        task_id: int = 1,
        description: str = 'Тестовая задача',
        priority: str = 'low',
        status: str = 'new',
) -> Task:
    return Task(task_id, description, priority, status, datetime.now())


async def fake_sleep(_: float) -> None:
    return None


def test_get_handler_success():
    task = make_task(priority='low')
    handlers = {'low': LowPriorityTaskHandler()}
    executor = TaskExecutor([task], handlers)
    handler = executor._get_handler(task)
    assert isinstance(handler, LowPriorityTaskHandler)

def test_get_handler_not_found():
    task = make_task(priority='high')
    handlers = {'low': LowPriorityTaskHandler()}
    executor = TaskExecutor([task], handlers)
    with pytest.raises(HandlerNotFoundError):
        executor._get_handler(task)

def test_gen_handler_invalid_handler():
    task = make_task(priority='low')
    handlers = {'low': object()}
    executor = TaskExecutor([task], handlers)
    with pytest.raises(InvalidHandlerError):
        executor._get_handler(task)

@pytest.mark.parametrize(
    'handler_class, priority',
    [
        (LowPriorityTaskHandler, 'low'),
        (MediumPriorityTaskHandler, 'medium'),
        (HighPriorityTaskHandler, 'high'),
    ]
)
def test_handler_processes_new_task(monkeypatch, handler_class, priority):
    monkeypatch.setattr(handlers_module.asyncio, 'sleep', fake_sleep)
    task = make_task(priority=priority, status='new')
    handler = handler_class()
    result = asyncio.run(handler.handle(task))
    assert result == TASK_PROCESSED
    assert task.status == 'done'

@pytest.mark.parametrize(
    'handler_class, priority',
    [
        (LowPriorityTaskHandler, 'low'),
        (MediumPriorityTaskHandler, 'medium'),
        (HighPriorityTaskHandler, 'high'),
    ]
)
def test_handler_skips_completed_task(monkeypatch, handler_class, priority):
    monkeypatch.setattr(handlers_module.asyncio, 'sleep', fake_sleep)
    task = make_task(priority=priority, status='done')
    handler = handler_class()
    result = asyncio.run(handler.handle(task))
    assert result == TASK_SKIPPED
    assert task.status == 'done'

@pytest.mark.parametrize(
    'handler_class, priority',
    [
        (LowPriorityTaskHandler, 'low'),
        (MediumPriorityTaskHandler, 'medium'),
        (HighPriorityTaskHandler, 'high'),
    ]
)
def test_handler_raises_for_task_in_progress(monkeypatch, handler_class, priority):
    monkeypatch.setattr(handlers_module.asyncio, 'sleep', fake_sleep)
    task = make_task(priority=priority, status='in_progress')
    handler = handler_class()
    with pytest.raises(Exception, match='уже находится в обработке'):
        asyncio.run(handler.handle(task))

def test_task_execution_context_prints_messages(capsys):
    async def run_context():
        async with TaskExecutionContext():
            pass
    asyncio.run(run_context())
    captured = capsys.readouterr()
    assert '[RESOURCE] Запуск контекста выполнения задач' in captured.out
    assert '[RESOURCE] Завершение контекста выполнения задач' in captured.out

def test_get_logger_returns_configured_logger():
    logger = get_logger('test_executor_logger')
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO
    assert logger.propagate is False
    assert len(logger.handlers) >= 2

def test_get_logger_does_not_duplicate_handlers():
    logger1 = get_logger('same_logger')
    handlers_count_1 = len(logger1.handlers)
    logger2 = get_logger('same_logger')
    handlers_count_2 = len(logger2.handlers)
    assert logger1 is logger2
    assert handlers_count_1 == handlers_count_2

def test_executor_run_logs_processed_task(monkeypatch):
    monkeypatch.setattr(handlers_module.asyncio, 'sleep', fake_sleep)
    info_messages = []
    warning_messages = []
    error_messages = []
    exception_messages = []
    monkeypatch.setattr(async_executor_module.logger, 'info', lambda msg: info_messages.append(msg))
    monkeypatch.setattr(async_executor_module.logger, 'warning', lambda msg: warning_messages.append(msg))
    monkeypatch.setattr(async_executor_module.logger, 'error', lambda msg: error_messages.append(msg))
    monkeypatch.setattr(async_executor_module.logger, 'exception', lambda msg: exception_messages.append(msg))
    task = make_task(task_id=1, priority='low', status='new')
    executor = TaskExecutor([task], {'low': LowPriorityTaskHandler()})
    asyncio.run(executor.run())
    assert task.status == 'done'
    assert any('Начата обработка задачи id=1' in msg for msg in info_messages)
    assert any('Завершена обработка задачи id=1' in msg for msg in info_messages)
    assert warning_messages == []
    assert error_messages == []
    assert exception_messages == []


def test_executor_run_logs_skipped_task(monkeypatch):
    monkeypatch.setattr(handlers_module.asyncio, 'sleep', fake_sleep)
    info_messages = []
    warning_messages = []
    monkeypatch.setattr(async_executor_module.logger, 'info', lambda msg: info_messages.append(msg))
    monkeypatch.setattr(async_executor_module.logger, 'warning', lambda msg: warning_messages.append(msg))
    monkeypatch.setattr(async_executor_module.logger, 'error', lambda msg: None)
    monkeypatch.setattr(async_executor_module.logger, 'exception', lambda msg: None)
    task = make_task(task_id=2, priority='low', status='done')
    executor = TaskExecutor([task], {'low': LowPriorityTaskHandler()})
    asyncio.run(executor.run())
    assert any('Начата обработка задачи id=2' in msg for msg in info_messages)
    assert any('Задача id=2 пропущена' in msg for msg in warning_messages)


def test_executor_run_logs_task_execution_error(monkeypatch):
    monkeypatch.setattr(handlers_module.asyncio, 'sleep', fake_sleep)
    error_messages = []
    monkeypatch.setattr(async_executor_module.logger, 'info', lambda msg: None)
    monkeypatch.setattr(async_executor_module.logger, 'warning', lambda msg: None)
    monkeypatch.setattr(async_executor_module.logger, 'error', lambda msg: error_messages.append(msg))
    monkeypatch.setattr(async_executor_module.logger, 'exception', lambda msg: None)
    task = make_task(task_id=3, priority='low', status='in_progress')
    executor = TaskExecutor([task], {'low': LowPriorityTaskHandler()})
    asyncio.run(executor.run())
    assert any('Ошибка обработки задачи id=3' in msg for msg in error_messages)


def test_executor_run_logs_invalid_task(monkeypatch):
    error_messages = []
    monkeypatch.setattr(async_executor_module.logger, 'info', lambda msg: None)
    monkeypatch.setattr(async_executor_module.logger, 'warning', lambda msg: None)
    monkeypatch.setattr(async_executor_module.logger, 'error', lambda msg: error_messages.append(msg))
    monkeypatch.setattr(async_executor_module.logger, 'exception', lambda msg: None)
    executor = TaskExecutor(['not_a_task'], {'low': LowPriorityTaskHandler()})
    asyncio.run(executor.run())
    assert any('Ошибка обработки задачи id=unknown' in msg for msg in error_messages)


def test_executor_run_logs_unexpected_error(monkeypatch):
    exception_messages = []

    class BadHandler:
        async def handle(self, task):
            raise ValueError('unexpected')

    monkeypatch.setattr(async_executor_module.logger, 'info', lambda msg: None)
    monkeypatch.setattr(async_executor_module.logger, 'warning', lambda msg: None)
    monkeypatch.setattr(async_executor_module.logger, 'error', lambda msg: None)
    monkeypatch.setattr(async_executor_module.logger, 'exception', lambda msg: exception_messages.append(msg))
    task = make_task(task_id=4, priority='low', status='new')
    executor = TaskExecutor([task], {'low': BadHandler()})
    asyncio.run(executor.run())
    assert any('Непредвиденная ошибка при обработке задачи id=4' in msg for msg in exception_messages)
import pytest
from datetime import datetime
from src.task import Task
from src.task_queue.filters import (
    filter_by_status,
    filter_by_priority,
    filter_ready_tasks,
    filter_completed_tasks,
)


@pytest.fixture
def tasks():
    return [
        Task(1, 'Подготовить отчёт', 'high', 'new', datetime(2026, 3, 22, 10, 0, 0)),
        Task(2, 'Проверить код', 'medium', 'in_progress', datetime(2026, 3, 22, 11, 0, 0)),
        Task(3, 'Отправить письмо', 'low', 'done', datetime(2026, 3, 22, 12, 0, 0)),
        Task(4, 'Собрать данные', 'high', 'done', datetime(2026, 3, 22, 13, 0, 0)),
    ]


def test_filter_by_status_returns_tasks(tasks):
    result = list(filter_by_status(tasks, 'done'))
    assert len(result) == 2
    assert result[0].id == 3
    assert result[1].id == 4


def test_filter_by_status_returns_empty(tasks):
    result = list(filter_by_status(tasks, 'недействительный статус'))
    assert result == []


def test_filter_by_priority_returns_tasks(tasks):
    result = list(filter_by_priority(tasks, 'high'))
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 4


def test_filter_by_priority_returns_empty(tasks):
    result = list(filter_by_priority(tasks, 'недействительный приоритет'))
    assert result == []


def test_filter_ready_tasks_returns_task(tasks):
    result = list(filter_ready_tasks(tasks))
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_completed_tasks_returns_tasks(tasks):
    result = list(filter_completed_tasks(tasks))
    assert len(result) == 2
    assert result[0].id == 3
    assert result[1].id == 4


def test_filter_functions_return_iterators(tasks):
    result = filter_by_status(tasks, 'done')
    assert iter(result) is result
    result = filter_by_priority(tasks, 'high')
    assert iter(result) is result
    result = filter_ready_tasks(tasks)
    assert iter(result) is result
    result = filter_completed_tasks(tasks)
    assert iter(result) is result

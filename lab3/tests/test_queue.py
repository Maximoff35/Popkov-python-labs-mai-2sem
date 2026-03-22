import pytest
from datetime import datetime
from src.task import Task
from src.task_queue import TaskQueue
from src.task_queue.queue_exceptions import InvalidTaskError


@pytest.fixture
def task1():
    return Task(1, 'Подготовить отчет', 'high', 'new', datetime(2026, 3, 22, 14, 56, 0))


@pytest.fixture
def task2():
    return Task(2, 'Рефакторинг кода', 'medium', 'in_progress', datetime(2026, 3, 22, 15, 56, 0))


@pytest.fixture
def task3():
    return Task(3, 'Деплой', 'low', 'done', datetime(2026, 3, 22, 16, 56, 0))


def test_task_queue_init_empty():
    queue = TaskQueue()
    assert len(queue) == 0
    assert list(queue) == []


def test_task_queue_init_with_tasks(task1, task2):
    queue = TaskQueue([task1, task2])
    assert len(queue) == 2
    assert list(queue) == [task1, task2]


def test_task_queue_init_error_for_invalid_task(task1):
    with pytest.raises(InvalidTaskError):
        TaskQueue([task1, 'не задача'])


def test_task_queue_iter_returns_tasks(task1, task2, task3):
    queue = TaskQueue([task1, task2, task3])
    result = list(queue)
    assert result == [task1, task2, task3]


def test_task_queue_repeated_iteration(task1, task2):
    queue = TaskQueue([task1, task2])
    first_pass = list(queue)
    second_pass = list(queue)
    assert first_pass == [task1, task2]
    assert second_pass == [task1, task2]


def test_task_queue_repr(task1, task2):
    queue = TaskQueue([task1, task2])
    assert repr(queue) == 'TaskQueue(size=2)'


def test_add_task_to_queue(task1):
    queue = TaskQueue()
    queue.add_task(task1)
    assert len(queue) == 1
    assert list(queue) == [task1]


def test_add_task_error_for_invalid_task():
    queue = TaskQueue()
    with pytest.raises(InvalidTaskError):
        queue.add_task('не задача')


def test_extend_adds_tasks_to_queue(task1, task2):
    queue = TaskQueue()
    queue.extend([task1, task2])
    assert len(queue) == 2
    assert list(queue) == [task1, task2]


def test_extend_error_for_invalid_task(task1):
    queue = TaskQueue()
    with pytest.raises(InvalidTaskError):
        queue.extend([task1, 123])


def test_contains_returns_true_for_task(task1, task2):
    queue = TaskQueue([task1, task2])
    assert task1 in queue
    assert task2 in queue


def test_contains_returns_true_for_task_id(task1, task2):
    queue = TaskQueue([task1, task2])
    assert 1 in queue
    assert 2 in queue


def test_contains_returns_false_for_missing_task(task1, task2, task3):
    queue = TaskQueue([task1, task2])
    assert task3 not in queue


def test_contains_returns_false_for_missing_task_id(task1, task2):
    queue = TaskQueue([task1, task2])
    assert 999 not in queue


def test_contains_returns_false_for_unsupported_type(task1, task2):
    queue = TaskQueue([task1, task2])
    assert 'abc' not in queue

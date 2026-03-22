import pytest
from datetime import datetime
from src.task import Task
from src.task.task_exceptions import (
    InvalidTaskIdError,
    InvalidTaskDescriptionError,
    InvalidTaskPriorityError,
    InvalidTaskStatusError,
    InvalidTaskCreatedAtError
)

created_at = datetime(2026, 3, 21, 22, 37, 0)


def test_task_init_success():
    t = Task(1, 'Подготовить отчёт', 'high', 'new', created_at)
    assert t.id == 1
    assert t.description == 'Подготовить отчёт'
    assert t.priority == 'high'
    assert t.status == 'new'
    assert t.created_at == created_at


def test_task_description_strip():
    t = Task(1, '    Подготовить отчёт    ', 'high', 'new', created_at)
    assert t.description == 'Подготовить отчёт'


def test_task_status_and_priority_norm():
    t1 = Task(1, 'Подготовить отчёт', 'High  ', '  NEW', created_at)
    assert t1.priority == 'high'
    assert t1.status == 'new'
    t2 = Task(2, 'Написать тесты', '  MEDium  ', 'in_Progress  ', created_at)
    assert t2.priority == 'medium'
    assert t2.status == 'in_progress'
    t3 = Task(3, 'Деплой', 'low', 'done', created_at)
    assert t3.priority == 'low'
    assert t3.status == 'done'


def test_task_is_completed_false():
    t1 = Task(1, 'Подготовить отчёт', 'high', 'new', created_at)
    assert t1.is_completed is False
    t2 = Task(2, 'Написать тесты', 'medium', 'in_progress', created_at)
    assert t2.is_completed is False


def test_task_is_completed_true():
    t1 = Task(1, 'Подготовить отчёт', 'high', 'done', created_at)
    assert t1.is_completed is True


def test_task_is_ready_true():
    t = Task(1, 'Подготовить отчёт', 'high', 'new', created_at)
    assert t.is_ready is True


def test_task_is_ready_false():
    t = Task(1, 'Подготовить отчёт', 'high', 'in_progress', created_at)
    assert t.is_ready is False
    t2 = Task(2, 'Написать тесты', 'medium', 'done', created_at)
    assert t2.is_ready is False


def test_task_summary():
    t = Task(1, 'Подготовить отчёт', 'high', 'done', created_at)
    assert t.summary == 'Task #1: [high] Подготовить отчёт (done)'


def test_task_repr():
    t = Task(1, 'Подготовить отчёт', 'high', 'done', created_at)
    assert repr(t) == "Task(id=1, description='Подготовить отчёт', priority='high', status='done', created_at=2026-03-21T22:37:00)"


def test_task_description_change():
    t = Task(1, 'Подготовить отчёт', 'high', 'new', created_at)
    t.description = 'Деплой'
    assert t.description == 'Деплой'

def test_task_priority_change():
    t = Task(1, 'Подготовить отчёт', 'high', 'new', created_at)
    t.priority = 'medium'
    assert t.priority == 'medium'
    t.priority = 'low'
    assert t.priority == 'low'

def test_task_status_change():
    t = Task(1, 'Подготовить отчёт', 'high', 'new', created_at)
    t.status = 'in_progress'
    assert t.status == 'in_progress'
    t.status = 'done'
    assert t.status == 'done'

def test_task_invalid_id_error():
    with pytest.raises(InvalidTaskIdError):
        Task('1', 'Подготовить отчёт', 'high', 'new', created_at)
    with pytest.raises(InvalidTaskIdError):
        Task(-8, 'Подготовить отчёт', 'high', 'new', created_at)
    t = Task(1, 'Подготовить отчёт', 'high', 'new', created_at)
    with pytest.raises(InvalidTaskIdError):
        t.id = 4

@pytest.mark.parametrize('d', [78, '', '  \t '])
def test_task_description_error(d):
    with pytest.raises(InvalidTaskDescriptionError):
        Task(1, d, 'high', 'new', created_at)
    t = Task(1, 'Подготовить отчёт', 'high', 'new', created_at)
    with pytest.raises(InvalidTaskDescriptionError):
        t.description = d

@pytest.mark.parametrize('p', [1, 'высокий', '', None])
def test_task_priority_error(p):
    with pytest.raises(InvalidTaskPriorityError):
        Task(1, 'Подготовить отчёт', p, 'new', created_at)
    t = Task(1, 'Подготовить отчёт', 'high', 'new', created_at)
    with pytest.raises(InvalidTaskPriorityError):
        t.priority = p

@pytest.mark.parametrize('st', [1, 'готово', '', None])
def test_task_status_error(st):
    with pytest.raises(InvalidTaskStatusError):
        Task(1, 'Подготовить отчёт', 'high', st, created_at)
    t = Task(1, 'Подготовить отчёт', 'high', 'new', created_at)
    with pytest.raises(InvalidTaskStatusError):
        t.status = st

@pytest.mark.parametrize('cr', [1, '2026-03-21T12:00:00', '', None])
def test_task_created_at_error(cr):
    with pytest.raises(InvalidTaskCreatedAtError):
        Task(1, 'Подготовить отчёт', 'high', 'new', cr)

def test_task_created_at_error_change():
    cr = datetime(2020, 3, 20, 6, 0, 0)
    t = Task(1, 'Подготовить отчёт', 'high', 'new', created_at)
    with pytest.raises(InvalidTaskCreatedAtError):
        t.created_at = cr
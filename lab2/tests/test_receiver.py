import pytest
from datetime import datetime
from src.receiver import collect_tasks
from src.task import Task


class InvalidSource:
    pass


class BadSource:
    def get_tasks(self):
        return 123


class GoodSource:
    def __init__(self):
        self.a = [
            {
                "id": 1,
                "description": "Обработать наблюдение",
                "priority": "high",
                "status": "new",
                "created_at": "2026-03-21T12:00:00"
            },
            {
                "id": 2,
                "description": "Проверить входящие данные из внешнего API",
                "priority": "medium",
                "status": "in_progress",
                "created_at": "2026-03-21T12:30:00"
            },
            {
                "id": 3,
                "description": "Сформировать отчет по задачам",
                "priority": "low",
                "status": "done",
                "created_at": "2026-03-21T13:00:00"
            }
        ]
    def get_tasks(self):
        for i in self.a:
            yield Task(i['id'], i['description'], i['priority'], i['status'], datetime.fromisoformat(i['created_at']))


def test_collect_tasks_returns_list():
    source = GoodSource()
    tasks = collect_tasks(source)
    assert isinstance(tasks, list)
    assert len(tasks) == len(source.a)
    for i in range(len(tasks)):
        assert isinstance(tasks[i], Task)
        assert tasks[i].id == source.a[i]['id']
        assert tasks[i].description == source.a[i]['description']
        assert tasks[i].priority == source.a[i]['priority']
        assert tasks[i].status == source.a[i]['status']
        assert tasks[i].created_at == datetime.fromisoformat(source.a[i]['created_at'])


def test_collect_tasks_raises_no_get_tasks():
    source = InvalidSource()
    with pytest.raises(TypeError):
        collect_tasks(source)


def test_collect_tasks_raises_non_iterable():
    source = BadSource()
    with pytest.raises(TypeError):
        collect_tasks(source)

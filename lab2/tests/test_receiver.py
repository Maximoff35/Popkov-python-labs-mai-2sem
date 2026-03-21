import pytest
from src.receiver import collect_tasks
from src.task import Task

class InvalidSource:
    pass

class BadSource:
    def get_tasks(self):
        return 123

class GoodSource:
    def get_tasks(self):
        a = [
            {"id": 1, "payload": "Обработать наблюдение"},
            {"id": 2, "payload": {"type": "report", "priority": "high"}}
        ]
        for i in a:
            yield Task(i['id'], i['payload'])

def test_collect_tasks_returns_list():
    source = GoodSource()
    tasks = collect_tasks(source)
    assert isinstance(tasks, list)
    assert len(tasks) == 2
    assert tasks[0].id == 1 and tasks[1].id == 2
    assert tasks[0].payload == "Обработать наблюдение"
    assert tasks[1].payload == {"type": "report", "priority": "high"}
    assert all(isinstance(t, Task) for t in tasks)

def test_collect_tasks_raises_no_get_tasks():
    source = InvalidSource()
    with pytest.raises(TypeError):
        collect_tasks(source)

def test_collect_tasks_raises_non_iterable():
    source = BadSource()
    with pytest.raises(TypeError):
        collect_tasks(source)
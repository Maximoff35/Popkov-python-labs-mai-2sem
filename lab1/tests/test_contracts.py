from src.contracts import TaskSource

class BadSource:
    pass

class GoodSource:
    def get_tasks(self):
        return []

def test_good_source_tasksource_protocol():
    source = GoodSource()
    assert isinstance(source, TaskSource)

def test_bad_source_not_tasksource_protocol():
    source = BadSource()
    assert not isinstance(source, TaskSource)
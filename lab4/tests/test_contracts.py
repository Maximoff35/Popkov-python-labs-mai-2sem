from src.contracts import TaskSource, ApiClient, TaskHandler

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


class GoodApiClient:
    def get_raw_tasks(self):
        return []

class BadApiClient:
    pass

def test_good_api_client():
    client = GoodApiClient()
    assert isinstance(client, ApiClient)

def test_bad_api_client():
    client = BadApiClient()
    assert not isinstance(client, ApiClient)

class GoodTaskHandler:
    async def handle(self, task):
        return 'processed'

class BadTaskHandler:
    pass

def test_good_task_handler():
    handler = GoodTaskHandler
    assert isinstance(handler, TaskHandler)

def test_bad_task_handler():
    handler = BadTaskHandler
    assert not isinstance(handler, TaskHandler)
from src.contracts import TaskSource, ApiClient

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
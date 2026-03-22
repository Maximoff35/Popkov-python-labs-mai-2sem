from src.sources.clients.jsonplaceholder_client import JsonPlaceholderClient
from datetime import datetime


class MockResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return [
            {
                'userId': 1,
                'id': 1,
                'title': 'delectus aut autem',
                'completed': False
            },
            {
                'userId': 1,
                'id': 2,
                'title': 'quis ut nam facilis et officia qui',
                'completed': True
            }
        ]


def mock_get(*args, **kwargs):
    return MockResponse()


def test_get_raw_tasks_success(monkeypatch):
    monkeypatch.setattr(
        'src.sources.clients.jsonplaceholder_client.requests.get',
        mock_get
    )

    client = JsonPlaceholderClient('https://test.com')
    tasks = list(client.get_raw_tasks())

    assert len(tasks) == 2
    assert isinstance(tasks[0], tuple)
    assert isinstance(tasks[1], tuple)

    assert tasks[0][0] == 1
    assert tasks[0][1] == 'delectus aut autem'
    assert tasks[0][2] == 'medium'
    assert tasks[0][3] == 'new'
    assert isinstance(tasks[0][4], datetime)
    assert tasks[0][:4] == (1, 'delectus aut autem', 'medium', 'new')

    assert tasks[1][0] == 2
    assert tasks[1][1] == 'quis ut nam facilis et officia qui'
    assert tasks[1][2] == 'medium'
    assert tasks[1][3] == 'done'
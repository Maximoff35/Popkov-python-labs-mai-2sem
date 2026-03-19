import json
from src.task import Task
from src.sources.generator_source import GeneratorSource
from src.sources.file_source import FileSource
from src.sources.api_source import ApiSource

def test_generator_source():
    source = GeneratorSource(5)
    tasks = list(source.get_tasks())
    assert len(tasks) == 5
    assert all(isinstance(t, Task) for t in tasks)
    assert tasks[0].id == 0
    assert tasks[-1].id == 4

def test_file_source(tmp_path):
    data = [
        {
            "id": 1,
            "payload": "Обработать наблюдение"
        },
        {
            "id": 2,
            "payload": {
                "type": "report",
                "priority": "high"
            }
        }
    ]
    file_path = tmp_path / "tasks.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")
    source = FileSource(str(file_path))
    tasks = list(source.get_tasks())
    assert len(tasks) == 2
    assert all(isinstance(t, Task) for t in tasks)
    assert tasks[0].id == 1
    assert tasks[0].payload == "Обработать наблюдение"
    assert tasks[1].id == 2
    assert tasks[1].payload == {"type": "report", "priority": "high"}

class MockResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return [
            {
                "userId": 1,
                "id": 1,
                "title": "delectus aut autem",
                "completed": False
            },
            {
                "userId": 1,
                "id": 2,
                "title": "quis ut nam facilis et officia qui",
                "completed": True
            }
        ]

def mock_get(*args, **kwargs):
    return MockResponse()

def test_api_source_reads_tasks(monkeypatch):
    monkeypatch.setattr("src.sources.api_source.requests.get", mock_get)
    source = ApiSource("https://jsonplaceholder.typicode.com/todos")
    tasks = list(source.get_tasks())
    assert len(tasks) == 2
    assert all(isinstance(t, Task) for t in tasks)
    assert tasks[0].id == 1
    assert tasks[0].payload["userId"] == 1
    assert tasks[0].payload["title"] == "delectus aut autem"
    assert tasks[0].payload["completed"] is False
    assert tasks[1].id == 2
    assert tasks[1].payload["completed"] is True



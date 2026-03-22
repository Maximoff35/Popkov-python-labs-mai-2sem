import pytest
import json
from datetime import datetime
from src.task import Task
from src.task.constants import ALLOWED_STATUSES, ALLOWED_PRIORITIES
from src.sources.generator_source import GeneratorSource
from src.sources.file_source import FileSource
from src.sources.api_source import ApiSource


def test_generator_source():
    source = GeneratorSource(5)
    cnt = 0
    for t in source.get_tasks():
        cnt += 1
        assert isinstance(t, Task)
        assert t.id == cnt
        assert t.description == f'Описание задачи №{cnt}'
        assert t.priority in ALLOWED_PRIORITIES
        assert t.status in ALLOWED_STATUSES
        assert isinstance(t.created_at, datetime)
    assert cnt == 5


def test_file_source(tmp_path):
    data = [
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

    file_path = tmp_path / "tasks.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")
    source = FileSource(str(file_path))
    cnt = 0
    for t in source.get_tasks():
        cnt += 1
        assert isinstance(t, Task)
        assert t.id == data[cnt - 1]['id']
        assert t.description == data[cnt - 1]['description']
        assert t.priority == data[cnt - 1]['priority']
        assert t.status == data[cnt - 1]['status']
        assert t.created_at == datetime.fromisoformat(data[cnt - 1]['created_at'])
    assert cnt == 3


def test_file_source_init_invalid_path_type():
    with pytest.raises(TypeError):
        FileSource(123)


def test_file_source_invalid_json(tmp_path):
    file_path = tmp_path / "bad.json"
    file_path.write_text("{ invalid json", encoding="utf-8")

    source = FileSource(str(file_path))

    with pytest.raises(ValueError, match='Файл не является корректным JSON.'):
        list(source.get_tasks())


def test_file_source_json_not_list(tmp_path):
    data = {"id": 1, "description": "Одна задача"}

    file_path = tmp_path / "tasks.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    source = FileSource(str(file_path))

    with pytest.raises(TypeError, match='Файл не является JSON-списком.'):
        list(source.get_tasks())


def test_file_source_list_item_not_dict(tmp_path):
    data = ["not a dict"]

    file_path = tmp_path / "tasks.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    source = FileSource(str(file_path))

    with pytest.raises(TypeError, match='Элемент не является JSON-словарем.'):
        list(source.get_tasks())


def test_file_source_missing_required_fields(tmp_path):
    data = [
        {
            "id": 1,
            "description": "Обработать наблюдение",
            "priority": "high",
            "status": "new"
        }
    ]

    file_path = tmp_path / "tasks.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    source = FileSource(str(file_path))

    with pytest.raises(ValueError, match='Не хватает необходимых полей в словаре.'):
        list(source.get_tasks())


def test_file_source_invalid_created_at_format(tmp_path):
    data = [
        {
            "id": 1,
            "description": "Обработать наблюдение",
            "priority": "high",
            "status": "new",
            "created_at": "not-a-date"
        }
    ]

    file_path = tmp_path / "tasks.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    source = FileSource(str(file_path))

    with pytest.raises(ValueError, match='Некорректный формат даты created_at.'):
        list(source.get_tasks())


class FakeApiClient:
    def get_raw_tasks(self):
        return [
            (1, 'delectus aut autem', 'medium', 'done', datetime(2026, 3, 21, 23, 39, 51, 178054)),
            (2, 'quis ut nam facilis et officia qui', 'high', 'new', datetime(2026, 3, 21, 23, 39, 51, 178054)),
            (3, 'fugiat veniam minus', 'high', 'new', datetime(2026, 3, 21, 23, 39, 51, 178054)),
            (4, 'et porro tempora', 'low', 'done', datetime(2026, 3, 21, 23, 39, 51, 178054)),
            (5, 'laboriosam mollitia et enim', 'medium', 'in_progress', datetime(2026, 3, 21, 23, 39, 51, 178054))
        ]


def test_api_source():
    client = FakeApiClient()
    raw_tasks = client.get_raw_tasks()
    source = ApiSource(client)
    cnt = 0
    for t in source.get_tasks():
        cnt += 1
        assert isinstance(t, Task)
        assert t.id == raw_tasks[cnt - 1][0]
        assert t.description == raw_tasks[cnt - 1][1]
        assert t.priority == raw_tasks[cnt - 1][2]
        assert t.status == raw_tasks[cnt - 1][3]
        assert t.created_at == raw_tasks[cnt - 1][4]
    assert cnt == 5


class BadApiClient:
    def get_raw_tasks(self):
        return ['bad data']


def test_api_source_invalid_data():
    source = ApiSource(BadApiClient())
    with pytest.raises(TypeError):
        list(source.get_tasks())
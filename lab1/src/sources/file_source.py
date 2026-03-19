import json
from typing import Iterable
from src.task import Task

class FileSource:
    """
    Источник задач.
    Загружает задачи из json-файла.
    """
    def __init__(self, file_path: str):
        """
        Инициализация.
        :param file_path: Путь к json-файлу
        """
        self.file_path = file_path

    def get_tasks(self) -> Iterable[Task]:
        """
        Загружает задачи из файла и возвращает генератор из объектов Task
        :return: Итерируемая коллекция объектов Task
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            json_tasks = json.load(file)

        for t in json_tasks:
            yield Task(t['id'], t['payload'])

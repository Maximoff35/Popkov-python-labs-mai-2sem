import json
from typing import Iterable
from datetime import datetime
from src.task import Task, constants


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

        if not isinstance(file_path, str):
            raise TypeError('Путь к файлу должен быть строкой.')
        self.file_path = file_path

    def get_tasks(self) -> Iterable[Task]:
        """
        Загружает задачи из файла и возвращает генератор из объектов Task
        :return: Итерируемая коллекция объектов Task
        """

        with open(self.file_path, 'r', encoding='utf-8') as file:
            try:
                json_tasks = json.load(file)
            except json.JSONDecodeError:
                raise ValueError('Файл не является корректным JSON.')

        if not isinstance(json_tasks, list):
            raise TypeError('Файл не является JSON-списком.')

        for t in json_tasks:
            if not isinstance(t, dict):
                raise TypeError('Элемент не является JSON-словарем.')
            if not set(constants.TASK_REQUIRED_FIELDS).issubset(t):
                raise ValueError('Не хватает необходимых полей в словаре.')

            try:
                created_at = datetime.fromisoformat(t['created_at'])
            except (TypeError, ValueError):
                raise ValueError('Некорректный формат даты created_at.')

            yield Task(
                t['id'],
                t['description'],
                t['priority'],
                t['status'],
                created_at
            )

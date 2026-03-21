from datetime import datetime
from src.task.constants import ALLOWED_STATUSES, ALLOWED_PRIORITIES
from src.task.task_exceptions import (
    InvalidTaskIdError,
    InvalidTaskDescriptionError,
    InvalidTaskPriorityError,
    InvalidTaskStatusError,
    InvalidTaskCreatedAtError
)


class BaseDescriptor:
    """
    Базовый descriptor.
    """

    def __set_name__(self, owner, name):
        """
        Сохраняет имя приватного атрибута, в котором хранится значение.
        """

        self.private_name = f'_{name}'

    def __get__(self, instance, owner):
        """
        Возвращает значение атрибута из внутреннего состояния объекта.
        """

        if instance is None:
            return self
        return instance.__dict__[self.private_name]


class TaskIdDescriptor(BaseDescriptor):
    """
    Data descriptor для id задачи.
    """

    def __set__(self, instance, value):
        """
        Проверяет, что id является целым положительным числом.
        Устанавливает значение id.
        """

        if self.private_name in instance.__dict__:
            raise InvalidTaskIdError('ID задачи нельзя изменять.')

        if not isinstance(value, int):
            raise InvalidTaskIdError('ID задачи должен быть целым числом.')
        if value <= 0:
            raise InvalidTaskIdError('ID задачи должен быть положительным.')
        instance.__dict__[self.private_name] = value


class TaskDescriptionDescriptor(BaseDescriptor):
    """
    Data descriptor для описания задачи.
    """

    def __set__(self, instance, value):
        """
        Проверяет, что описание является не пустой строкой.
        Устанавливает значение описания.
        """

        if not isinstance(value, str):
            raise InvalidTaskDescriptionError('Описание задачи должно быть строкой.')
        clean_value = value.strip()
        if clean_value == '':
            raise InvalidTaskDescriptionError('Описание задачи не должно быть пустым.')
        instance.__dict__[self.private_name] = clean_value


class TaskPriorityDescriptor(BaseDescriptor):
    """
    Data descriptor для приоритета задачи.
    """

    def __set__(self, instance, value):
        """
        Проверяет, что приоритет принимает допустимое значение.
        Устанавливает значение приоритета.
        """

        if not isinstance(value, str):
            raise InvalidTaskPriorityError('Приоритет задачи должен быть строкой.')
        clean_value = value.strip().lower()
        if clean_value not in ALLOWED_PRIORITIES:
            raise InvalidTaskPriorityError('Недопустимый приоритет задачи.')
        instance.__dict__[self.private_name] = clean_value


class TaskStatusDescriptor(BaseDescriptor):
    """
    Data descriptor для статуса задачи.
    """

    def __set__(self, instance, value):
        """
        Проверяет, что статус принимает допустимое значение.
        Устанавливает значение статуса.
        """

        if not isinstance(value, str):
            raise InvalidTaskStatusError('Статус задачи должен быть строкой.')
        clean_value = value.strip().lower()
        if clean_value not in ALLOWED_STATUSES:
            raise InvalidTaskStatusError('Недопустимый статус задачи.')
        instance.__dict__[self.private_name] = clean_value


class TaskCreatedAtDescriptor(BaseDescriptor):
    """
    Data descriptor для времени создания задачи.
    """

    def __set__(self, instance, value):
        """
        Проверяет, что время создания является объектом datetime.
        Устанавливает значение времени создания.
        """

        if self.private_name in instance.__dict__:
            raise InvalidTaskCreatedAtError('Время создания задачи нельзя изменять.')

        if not isinstance(value, datetime):
            raise InvalidTaskCreatedAtError('Время создания задачи должно быть типа datetime.')
        instance.__dict__[self.private_name] = value


class TaskSummaryDescriptor:
    """
    Non-data descriptor для получения краткой информации о задаче.
    """

    def __get__(self, instance, owner):
        """
        Возвращает строку с основными данными задачи.
        """

        if instance is None:
            return self
        return f'Task #{instance.id}: [{instance.priority}] {instance.description} ({instance.status})'

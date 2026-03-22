from dataclasses import dataclass
from datetime import datetime


class TaskError(Exception):
    pass

class InvalidTaskIdError(TaskError):
    pass

class InvalidTaskDescriptionError(TaskError):
    pass

class InvalidTaskPriorityError(TaskError):
    pass

class InvalidTaskStatusError(TaskError):
    pass

class InvalidTaskCreatedAtError(TaskError):
    pass


ALLOWED_STATUSES = ('new', 'in_progress', 'done')
ALLOWED_PRIORITIES = ('low', 'medium', 'high')


class BaseDescriptor:
    def __set_name__(self, owner, name):
        self.private_name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.private_name]


class TaskIdDescriptor(BaseDescriptor):
    def __set__(self, instance, value):
        if self.private_name in instance.__dict__:
            raise InvalidTaskIdError('ID задачи нельзя изменять.')

        if not isinstance(value, int):
            raise InvalidTaskIdError('ID задачи должен быть целым числом.')
        if value <= 0:
            raise InvalidTaskIdError('ID задачи должен быть положительным.')
        instance.__dict__[self.private_name] = value


class TaskDescriptionDescriptor(BaseDescriptor):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise InvalidTaskDescriptionError('Описание задачи должно быть строкой.')
        clean_value = value.strip()
        if clean_value == '':
            raise InvalidTaskDescriptionError('Описание задачи не должно быть пустым.')
        instance.__dict__[self.private_name] = clean_value


class TaskPriorityDescriptor(BaseDescriptor):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise InvalidTaskPriorityError('Приоритет задачи должен быть строкой.')
        clean_value = value.strip().lower()
        if clean_value not in ALLOWED_PRIORITIES:
            raise InvalidTaskPriorityError('Недопустимый приоритет задачи.')
        instance.__dict__[self.private_name] = clean_value


class TaskStatusDescriptor(BaseDescriptor):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise InvalidTaskStatusError('Статус задачи должен быть строкой.')
        clean_value = value.strip().lower()
        if clean_value not in ALLOWED_STATUSES:
            raise InvalidTaskStatusError('Недопустимый статус задачи.')
        instance.__dict__[self.private_name] = clean_value


class TaskCreatedAtDescriptor(BaseDescriptor):
    def __set__(self, instance, value):
        if self.private_name in instance.__dict__:
            raise InvalidTaskCreatedAtError('Время создания задачи нельзя изменять.')

        if not isinstance(value, datetime):
            raise InvalidTaskCreatedAtError('Время создания задачи должно быть типа datetime.')
        instance.__dict__[self.private_name] = value


class TaskSummaryDescriptor:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return f'Task #{instance.id}: [{instance.priority}] {instance.description} ({instance.status})'


@dataclass
class Task:
    id: int
    description: str
    priority: str
    status: str
    created_at: datetime

    id = TaskIdDescriptor()
    description = TaskDescriptionDescriptor()
    priority = TaskPriorityDescriptor()
    status = TaskStatusDescriptor()
    created_at = TaskCreatedAtDescriptor()

    summary = TaskSummaryDescriptor()

    @property
    def is_completed(self) -> bool:
        return self.status == 'done'

    @property
    def is_ready(self) -> bool:
        return self.status == 'new'

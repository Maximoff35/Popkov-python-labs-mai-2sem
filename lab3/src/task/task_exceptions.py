class TaskError(Exception):
    """Базовый класс для всех ошибок Task."""
    pass


class InvalidTaskIdError(TaskError):
    """Класс для ошибок id задач."""
    pass


class InvalidTaskDescriptionError(TaskError):
    """Класс для ошибок описания задач."""
    pass


class InvalidTaskPriorityError(TaskError):
    """Класс для ошибок приоритетов задач."""
    pass


class InvalidTaskStatusError(TaskError):
    """Класс для ошибок статусов задач."""
    pass


class InvalidTaskCreatedAtError(TaskError):
    """Класс для ошибок времени создания задач."""
    pass

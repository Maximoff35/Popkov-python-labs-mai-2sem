class TaskQueueError(Exception):
    """Базовый класс для исключений TaskQueue"""
    pass


class EmptyQueueError(TaskQueueError):
    """Класс для ошибок пустой очереди"""
    pass


class InvalidTaskError(TaskQueueError):
    """Класс для ошибок задач в очереди"""
    pass
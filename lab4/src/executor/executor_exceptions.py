class TaskExecutionError(Exception):
    """
    Общий класс всех ошибок обработки задач.
    """
    pass

class TaskAlreadyInProgressError(TaskExecutionError):
    """
    Ошибка обработки уже обрабатываемой задачи.
    """
    pass

class HandlerNotFoundError(TaskExecutionError):
    """
    Ошибка: не найден подходящий обработчик.
    """
    pass

class InvalidHandlerError(TaskExecutionError):
    """
    Обработчик не соответствует контракту.
    """
    pass

class InvalidTaskError(TaskExecutionError):
    """
    Невалидный объект задачи.
    """
    pass
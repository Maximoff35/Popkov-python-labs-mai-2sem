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
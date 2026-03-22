class TaskExecutionContext:
    """
    Контекст выполнения задач.
    Используется для демонстрации async context manager.
    """

    async def __aenter__(self):
        print('[RESOURCE] Запуск контекста выполнения задач')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print('[RESOURCE] Завершение контекста выполнения задач')
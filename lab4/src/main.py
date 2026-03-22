from typing import Iterable
from src.task import Task
from src.task_queue import TaskQueue
from src.sources.generator_source import GeneratorSource
from src.sources.api_source import ApiSource
from src.sources.file_source import FileSource
from src.receiver import collect_tasks
from src.sources.clients.jsonplaceholder_client import JsonPlaceholderClient
from src.executor.handlers import (
    HighPriorityTaskHandler,
    LowPriorityTaskHandler,
    MediumPriorityTaskHandler
)
from src.executor import TaskExecutor
import asyncio

def print_tasks(title: str, tasks: Iterable[Task]) -> None:
    """
    Печатает список задач с заголовком.
    :param title: Заголовок блока.
    :param tasks: Итерируемая коллекция задач.
    """
    print(f'\n=== {title} ===')
    found = False
    for t in tasks:
        print(t.summary)
        found = True
    if not found:
        print('Нет задач.')


def build_queue() -> TaskQueue:
    """
    Создает общую очередь из всех источников.
    :return: Объект TaskQueue.
    """
    all_tasks = TaskQueue()

    print('\n==============================')
    print('ДЕМОНСТРАЦИЯ ИСТОЧНИКОВ ЗАДАЧ')
    print('==============================')

    gen_source = GeneratorSource(5)
    gen_tasks = collect_tasks(gen_source)
    print_tasks('Задачи из GeneratorSource', gen_tasks)
    all_tasks.extend(gen_tasks)

    file_source = FileSource('data/tasks.json')
    file_tasks = collect_tasks(file_source)
    print_tasks('Задачи из FileSource', file_tasks)
    all_tasks.extend(file_tasks)

    client = JsonPlaceholderClient('https://jsonplaceholder.typicode.com/todos')
    api_source = ApiSource(client)
    api_tasks = collect_tasks(api_source)[:5]
    print_tasks('Задачи из ApiSource', api_tasks)
    all_tasks.extend(api_tasks)

    return all_tasks


def show_queue_features(queue: TaskQueue) -> None:
    """
    Демонстрирует работу очереди и фильтров.
    :param queue: Очередь задач.
    """
    print('\n==========================')
    print('ДЕМОНСТРАЦИЯ ОЧЕРЕДИ ЗАДАЧ')
    print('==========================')

    print(f'\nВсего задач в очереди: {len(queue)}')
    print(f'Представление очереди: {queue}')

    print_tasks('Все задачи', queue)
    print_tasks('Задачи со статусом in_progress', queue.filter_by_status('in_progress'))
    print_tasks('Задачи с приоритетом high', queue.filter_by_priority('high'))
    print_tasks('Готовые к выполнению задачи', queue.filter_ready_tasks())
    print_tasks('Выполненные задачи', queue.filter_completed_tasks())

    print('\n=== Проверка оператора in ===')
    print(f'Есть ли задача с id=1? {1 in queue}')


def build_handlers() -> dict:
    """
    Создает словарь обработчиков по приоритету.
    :return: Словарь обработчиков.
    """
    return {
        'low': LowPriorityTaskHandler(),
        'medium': MediumPriorityTaskHandler(),
        'high': HighPriorityTaskHandler()
    }


async def run_executor_demo(queue: TaskQueue) -> None:
    """
    Демонстрирует асинхронную обработку задач.
    :param queue: Очередь задач.
    """
    print('\n===================================')
    print('ДЕМОНСТРАЦИЯ АСИНХРОННОЙ ОБРАБОТКИ')
    print('===================================')

    handlers = build_handlers()
    executor = TaskExecutor(queue, handlers)

    print_tasks('Состояние задач ДО обработки', queue)
    await executor.run()
    print_tasks('Состояние задач ПОСЛЕ обработки', queue)


async def main() -> None:
    """
    Главная функция программы.
    """
    queue = build_queue()
    show_queue_features(queue)
    await run_executor_demo(queue)


if __name__ == "__main__":
    asyncio.run(main())
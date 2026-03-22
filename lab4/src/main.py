from src.sources.generator_source import GeneratorSource
from src.receiver import collect_tasks
from src.task_queue import TaskQueue


def main():
    gen_source = GeneratorSource(10)
    gen_tasks = collect_tasks(gen_source)
    queue = TaskQueue(gen_tasks)

    print('=== Все задачи ===')
    for task in queue:
        print(task.summary)

    print('\n=== Задачи со статусом in_progress ===')
    for task in queue.filter_by_status('in_progress'):
        print(task.summary)

    print('\n=== Задачи с приоритетом high ===')
    for task in queue.filter_by_priority('high'):
        print(task.summary)

    print('\n=== Готовые к выполнению задачи ===')
    for task in queue.filter_ready_tasks():
        print(task.summary)

    print('\n=== Выполненные задачи ===')
    for task in queue.filter_completed_tasks():
        print(task.summary)


if __name__ == "__main__":
    main()
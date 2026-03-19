from src.sources.generator_source import GeneratorSource
from src.sources.file_source import FileSource
from src.sources.api_source import ApiSource
from src.receiver import collect_tasks


def main():
    print("=== Генератор ===")
    gen_source = GeneratorSource(3)
    gen_tasks = collect_tasks(gen_source)
    for task in gen_tasks:
        print(task)

    print("\n=== Файл ===")
    file_source = FileSource("data/tasks.json")
    file_tasks = collect_tasks(file_source)
    for task in file_tasks:
        print(task)

    print("\n=== API ===")
    api_source = ApiSource("https://jsonplaceholder.typicode.com/todos")
    api_tasks = collect_tasks(api_source)
    for task in api_tasks[:5]:
        print(task)


if __name__ == "__main__":
    main()
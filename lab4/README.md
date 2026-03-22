
# Лабораторная работа №4. Асинхронная обработка задач

Попков Максим Александрович  
Группа: М8О-105БВ-25

---

## Цель и результаты

- Реализовать асинхронный исполнитель задач.
- Освоить работу с async/await.
- Использовать протоколы (`Protocol`) для контрактов обработчиков.
- Реализовать контекстный менеджер для управления ресурсами.
- Добавить централизованное логирование.
- Интегрировать решение с предыдущими лабораторными работами.
- Обеспечить покрытие тестами ≥ 80%.

---

## Структура проекта

```
.
├── data/
│   └── tasks.json
│
├── src/
│   ├── __init__.py
│   ├── contracts.py
│   ├── receiver.py
│   ├── main.py
│   │
│   ├── task/
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── descriptors.py
│   │   ├── constants.py
│   │   └── task_exceptions.py
│   │
│   ├── task_queue/
│   │   ├── __init__.py
│   │   ├── queue.py
│   │   ├── filters.py
│   │   └── queue_exceptions.py
│   │
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── api_source.py
│   │   ├── file_source.py
│   │   ├── generator_source.py
│   │   └── clients/
│   │       ├── __init__.py
│   │       └── jsonplaceholder_client.py
│   │
│   └── executor/
│       ├── __init__.py
│       ├── async_executor.py
│       ├── constants.py
│       ├── executor_exceptions.py
│       ├── handlers.py
│       ├── logger.py
│       └── resources.py
│
├── tests/
│   ├── test_queue.py
│   ├── test_queue_filters.py
│   ├── test_tasks.py
│   ├── test_sources.py
│   ├── test_receiver.py
│   ├── test_contracts.py
│   ├── test_executor.py
│   └── test_jsonplaceholder_client.py
│
├── requirements.txt
├── report.pdf
└── README.md
```

---

## Описание реализации

### executor/async_executor.py

Класс `TaskExecutor` — асинхронный исполнитель задач.

Функциональность:
- выбор обработчика по приоритету задачи;
- асинхронная обработка задач;
- обработка ошибок;
- логирование всех этапов выполнения;
- использование async context manager.

---

### executor/handlers.py

Реализованы обработчики задач:

- `LowPriorityTaskHandler`
- `MediumPriorityTaskHandler`
- `HighPriorityTaskHandler`

Особенности:
- асинхронная обработка (`async def`);
- имитация выполнения через `asyncio.sleep`;
- изменение статуса задачи (`new → in_progress → done`);
- обработка уже выполняемых задач.

---

### executor/resources.py

Реализован асинхронный контекстный менеджер:

- запуск ресурса при входе (`__aenter__`);
- завершение при выходе (`__aexit__`).

Используется в `TaskExecutor`.

---

### executor/logger.py

Реализован единый логгер:

- вывод в консоль;
- запись в файл (`executor.log`);
- единый формат логов.

---

### contracts.py

Добавлен контракт `TaskHandler`:

```python
async def handle(self, task: Task) -> str
```

Позволяет легко добавлять новые обработчики.

---

### main.py

Демонстрация полной работы системы:

- получение задач из всех источников;
- формирование очереди;
- применение фильтров;
- асинхронная обработка задач;
- вывод результатов до и после выполнения.

---

## Особенности реализации

- асинхронная архитектура (async/await);
- использование Protocol для контрактов;
- разделение логики по слоям;
- расширяемость (легко добавить новый handler);
- централизованная обработка ошибок;
- интеграция всех лабораторных в одну систему.

---

## Установка и запуск

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Запуск

```
python -m src.main
```

---

## Тестирование

```
pytest -v
pytest --cov=src --cov-report=term-missing
```

Покрытие: ~81%

Тестируются:
- executor и обработчики;
- источники данных;
- очередь задач;
- модель Task;
- контракты;
- обработка ошибок.

---

## Вывод

Реализована асинхронная система обработки задач с использованием современных возможностей Python.

Закреплены навыки:
- работы с async/await;
- проектирования расширяемой архитектуры;
- использования Protocol;
- написания тестов;
- интеграции нескольких модулей в единую систему.

Решение соответствует требованиям лабораторной работы.

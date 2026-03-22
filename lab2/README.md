# Лабораторная работа №2. Модель задачи: дескрипторы и @property

Попков Максим Александрович  
Группа: М8О-105БВ-25

---

## Цель и результаты

- Освоить управление доступом к атрибутам через дескрипторы.  
- Реализовать доменную модель задачи с защитой инвариантов.  
- Научиться использовать data и non-data descriptors.  
- Реализовать вычисляемые свойства через @property.  
- Обеспечить корректную обработку ошибок через пользовательские исключения.  

---

## Постановка задачи

В рамках платформы обработки задач необходимо реализовать модель задачи (Task) с корректной инкапсуляцией, валидацией данных и защитой состояния объекта.

Задача должна содержать:

- уникальный идентификатор (id);
- описание (description);
- приоритет (priority);
- статус (status);
- время создания (created_at);
- вычисляемые свойства.

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
│   └── sources/
│       ├── __init__.py
│       ├── api_source.py
│       ├── file_source.py
│       ├── generator_source.py
│       └── clients/
│           ├── __init__.py
│           └── jsonplaceholder_client.py
│
├── tests/
│   ├── test_tasks.py
│   ├── test_sources.py
│   ├── test_receiver.py
│   ├── test_contracts.py
│   └── test_jsonplaceholder_client.py
│
├── report.pdf
├── requirements.txt
└── README.md
```
---

## Описание реализованных модулей

### task/model.py

Класс Task — основная доменная модель.

Содержит:
- id
- description
- priority
- status
- created_at

Дополнительно:
- is_completed — задача выполнена
- is_ready — задача готова к выполнению

---

### task/descriptors.py

Реализованы пользовательские дескрипторы:

Data descriptors:
- TaskIdDescriptor
- TaskDescriptionDescriptor
- TaskPriorityDescriptor
- TaskStatusDescriptor
- TaskCreatedAtDescriptor

Обеспечивают:
- валидацию данных;
- нормализацию значений;
- защиту от изменения (id, created_at).

Non-data descriptor:
- TaskSummaryDescriptor — краткое описание задачи.

---

### task/constants.py

Содержит допустимые значения:

- статусов: new, in_progress, done
- приоритетов: low, medium, high

---

### task/task_exceptions.py

Пользовательские исключения:

- InvalidTaskIdError
- InvalidTaskDescriptionError
- InvalidTaskPriorityError
- InvalidTaskStatusError
- InvalidTaskCreatedAtError

---

### sources/*

Источники задач (с прошлой лабораторной):

- генератор (generator_source)
- файл (file_source)
- API (api_source)

Работают через единый контракт.

---

### receiver.py

Функция сбора задач из источников:
- проверяет контракт;
- возвращает список задач.

---

## Особенности реализации

- Использованы data descriptors для контроля записи атрибутов.
- Использован non-data descriptor для вычисляемого представления.
- Разделено публичное API и внутреннее состояние (_attr).
- Реализована защита инвариантов:
  - id нельзя изменить
  - created_at нельзя изменить
- Валидация всех входных данных.
- Чистая и расширяемая архитектура.

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

Минимальное покрытие: ≥ 80%

---

## Вывод

В ходе работы реализована безопасная и расширяемая модель задачи с использованием дескрипторов и property.

Достигнуто:
- полное управление доступом к атрибутам;
- защита от некорректных состояний;
- чистый и понятный API;
- соответствие требованиям архитектуры платформы обработки задач.

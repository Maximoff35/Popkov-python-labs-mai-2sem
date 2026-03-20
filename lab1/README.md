# Лабораторная работа №1. Обработка задач из различных источников

Попков Максим Александрович  
Группа: М8О-105БВ-25

## Цель и результаты

- Освоить использование протоколов (`Protocol`) и структурной типизации.  
- Реализовать систему обработки задач из разных источников.  
- Научиться работать с генераторами (`yield`).  
- Реализовать единый интерфейс для различных источников данных (генератор, файл, API).  
- Освоить написание модульных тестов с использованием PyTest.  
- Достичь высокого покрытия кода тестами (100%).

---

## Структура проекта

```
.
├── src/
│   ├── __init__.py
│   ├── task.py
│   ├── contracts.py
│   ├── receiver.py
│   ├── sources/
│   │   ├── generator_source.py
│   │   ├── file_source.py
│   │   └── api_source.py
│   └── main.py
│
├── tests/
│   ├── test_contracts.py
│   ├── test_receiver.py
│   └── test_sources.py
│
├── report.pdf
├── requirements.txt
└── README.md
```

---

## Описание реализованных модулей

### task.py
Класс Task:
- id — идентификатор
- payload — данные задачи

### contracts.py
Протокол TaskSource с методом get_tasks()

### generator_source.py
Генерация задач через yield

### file_source.py
Чтение задач из JSON-файла

### api_source.py
Получение задач из внешнего API (JSONPlaceholder)

### receiver.py
Функция collect_tasks:
- проверка источника
- преобразование в список

### main.py
Демонстрация работы системы

---

## Установка и запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Запуск

```bash
python -m src.main
```

---

## Тестирование

```bash
pytest -v
pytest --cov=src --cov-report=term-missing
```

Покрытие: 100%

---

## Особенности

- Protocol и структурная типизация
- Генераторы (yield)
- Работа с API
- monkeypatch в тестах

---

## Вывод

Реализована система обработки задач с единым интерфейсом и полной тестируемостью.

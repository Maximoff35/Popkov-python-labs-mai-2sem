from dataclasses import dataclass
from typing import Any

@dataclass
class Task:
    """
    Класс для задачи. Содержит:
    - id — уникальный идентификатор задачи;
    - payload — произвольные данные задачи.
    """
    id: int
    payload: Any

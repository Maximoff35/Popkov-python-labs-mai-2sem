from datetime import datetime
from src.task.descriptors import (
    TaskIdDescriptor,
    TaskDescriptionDescriptor,
    TaskPriorityDescriptor,
    TaskStatusDescriptor,
    TaskCreatedAtDescriptor,
    TaskSummaryDescriptor
)


class Task:
    """
    Класс для задачи. Содержит:
    - id - уникальный идентификатор задачи;
    - description - описание задачи;
    - priority - приоритет задачи;
    - status - статус задачи;
    - created_at - время создания задачи.
    """

    id = TaskIdDescriptor()
    description = TaskDescriptionDescriptor()
    priority = TaskPriorityDescriptor()
    status = TaskStatusDescriptor()
    created_at = TaskCreatedAtDescriptor()
    summary = TaskSummaryDescriptor()

    def __init__(
            self,
            id: int,
            description: str,
            priority: str,
            status: str,
            created_at: datetime
    ):
        """
        Инициализация.
        """

        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
        self.created_at = created_at

    @property
    def is_completed(self) -> bool:
        """
        Возвращает True, если задача выполнена.
        """

        return self.status == 'done'

    @property
    def is_ready(self) -> bool:
        """
        Возвращает True, если задача готова к выполнению.
        """

        return self.status == 'new'

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта задачи.
        """

        return (
            f"Task(id={self.id}, "
            f"description='{self.description}', "
            f"priority='{self.priority}', "
            f"status='{self.status}', "
            f"created_at={self.created_at.isoformat()})"
        )

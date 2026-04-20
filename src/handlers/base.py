from typing import runtime_checkable, Protocol
from src.models import Task

@runtime_checkable
class TaskHandler(Protocol):
    """A structural protocol defining the required interface for task source providers."""
    async def handle(self, task: Task) -> list[Task]:
        """Retrieve a list of tasks from the source."""
        pass
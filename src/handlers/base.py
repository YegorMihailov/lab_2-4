from typing import runtime_checkable, Protocol
from src.models import Task

@runtime_checkable
class TaskHandler(Protocol):
    """A structural protocol defining the required interface for all task handlers."""
    async def handle(self, task: Task) -> list[Task]:
        """Process the given task"""
        pass
from typing import runtime_checkable, Protocol, AsyncIterator
from src.models import Task

@runtime_checkable
class TaskSource(Protocol):
    """A structural protocol defining the required interface for task source providers."""
    def get_tasks(self) -> AsyncIterator[Task]:
        """Retrieve a list of tasks from the source."""
        pass
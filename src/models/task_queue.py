from typing import Iterator
from .task import Task

class TaskQueue:
    """A collection of Task objects"""

    def __init__(self):
        """Initialize an empty task queue"""

        self._tasks: list[Task] = []

    def add_task(self, task: Task):
        """Add a task"""

        self._tasks.append(task)

    def __iter__(self) -> Iterator[Task]:
        """Return an iterator to allow repeatable traversal over the tasks"""

        return iter(self._tasks)
    
    def filter_by_status(self, status: str) -> Iterator[Task]:
        """Yield tasks matching specific status"""

        for task in self._tasks:
            if task.status == status:
                yield task
    
    def filter_by_priority(self, min_priority: int, max_priority: int) -> Iterator[Task]:
        """Yield tasks within priority range"""

        for task in self._tasks:
            if min_priority <= task.priority <= max_priority:
                yield task

    def __len__(self) -> int:
        """Return total count of tasks in the queue"""

        return len(self._tasks)
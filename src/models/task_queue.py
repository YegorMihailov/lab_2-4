from typing import AsyncIterator
from .task import Task
import asyncio

class TaskQueue:
    """A collection of Task objects"""

    def __init__(self):
        """Initialize an empty task queue"""

        self._tasks: list[Task] = []

    def add_task(self, task: Task):
        """Add a task"""

        self._tasks.append(task)

    async def __aiter__(self) -> AsyncIterator[Task]:
        """Return an iterator to allow repeatable traversal over the tasks"""
        for task in self._tasks:
            await asyncio.sleep(0)
            yield task
    
    async def filter_by_status(self, status: str) -> AsyncIterator[Task]:
        """Yield tasks matching specific status"""

        async for task in self._tasks:
            if task.status == status:
                yield task
    
    async def filter_by_priority(self, min_priority: int, max_priority: int) -> AsyncIterator[Task]:
        """Yield tasks within priority range"""

        async for task in self._tasks:
            if min_priority <= task.priority <= max_priority:
                yield task

    def __len__(self) -> int:
        """Return total count of tasks in the queue"""

        return len(self._tasks)
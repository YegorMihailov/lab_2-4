import asyncio
import random
from src.models import Task
from typing import AsyncIterator

class ApiTaskSource:
    """API stub that simulates an external task source"""

    async def get_tasks(self) -> AsyncIterator[Task]:
        """Simulate API call to fetch tasks with a delay"""
        await asyncio.sleep(1)

        for i in range(4):
            yield Task(
                id=100 + i, 
                payload={
                    "type": "file",
                    "order_id": random.randint(1001, 2000)
                },
                description='API generated task', 
                priority=random.randint(1, 5)
            )
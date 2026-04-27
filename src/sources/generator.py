import random
import asyncio
from src.models import Task
from typing import AsyncIterator

class GeneratorTaskSource:
    """Task source that creates random task objects"""

    async def get_tasks(self) -> AsyncIterator[Task]:
        """Generate random tasks"""

        for _ in range(random.randint(1, 5)):
            await asyncio.sleep(0)
            yield Task(
                id=random.randint(1, 100), 
                payload={"type": "log", "amount": random.randint(100, 1000)}, 
                description='Random task', 
                priority=random.randint(1, 5)
            )
import asyncio
import logging
from src.models import Task

class LoggingHandler:
    """Handler for logging task information"""

    async def handle(self, task: Task) -> None:
        """Log task attributes"""

        await asyncio.sleep(0)
        logging.info(f"ID: {task.id} | Status: {task.status} | Priority: {task.priority} | Created: {task.created_at} | Data: {task.payload}")
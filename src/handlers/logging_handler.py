import asyncio
import logging
from src.models import Task
from .base import TaskHandler

class LoggingHandler:

    async def handle(self, task: Task) -> None:
        await asyncio.sleep(0)
        logging.info(f"ID: {task.id} | Status: {task.status} | Priority: {task.priority} | Created: {task.created_at} | Data: {task.payload}")
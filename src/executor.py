import asyncio
import logging
from typing import Dict
from src.models import Task, TaskQueue
from src.handlers.base import TaskHandler

class TaskExecutor:
    """Orchestrates the execution of tasks"""

    def __init__(self, queue: TaskQueue):
        """Initialize executor with a task queue"""

        self._queue = queue
        self._handlers: Dict[str, TaskHandler] = {}
    
    def register_handler(self, task_type: str, handler: TaskHandler):
        """Register handler for a given task type"""

        self._handlers[task_type] = handler

    async def run(self):
        """Iterates through the queue and processes tasks concurrently"""
        
        logging.info("Executor started")

        running_tasks = []

        async for task in self._queue:
            task_coroutine = self._process_task(task)
            running_tasks.append(asyncio.create_task(task_coroutine))

        if running_tasks:
            await asyncio.gather(*running_tasks, return_exceptions=True)
        
        logging.info("Executor finished processing all tasks")

    async def _process_task(self, task: Task):
        """Identify the correct handler for the task and execute it"""
        
        task_type = task.payload.get("type", "default")
        handler = self._handlers[task_type]

        if not handler:
            logging.error(f"No handler registered for type: {task_type}")
            task.status = "failed"
            return
        
        try:
            if isinstance(handler, TaskHandler):
                await handler.handle(task)
            else:
                logging.error(f"Handler for {task_type} does not follow Protocol")
        except Exception as e:
            logging.error(f"Error executing task {task.id}: {e}")
            task.status = "failed"

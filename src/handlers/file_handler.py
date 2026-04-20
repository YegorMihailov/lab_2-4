import aiofiles
import logging
from src.models import Task

class FileHandler:

    async def handle(self, task: Task):
        try:
            report_path = 'task_report.txt'

            async with aiofiles.open(report_path, mode='a', encoding='utf-8') as f:
                report_line = f"ID: {task.id} | Status: {task.status} | Priority: {task.priority} | Created: {task.created_at} | Data: {task.payload}\n"
                await f.write(report_line)
            logging.error(f"Successfully wrote to file. Task id: {task.id}")
        except Exception as e:
            logging.error(f"Error writing task to file. Task id: {task.id}")
            task.status = 'failed'
            
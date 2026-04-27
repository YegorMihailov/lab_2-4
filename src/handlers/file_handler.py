import aiofiles
import logging
from src.models import Task

class FileHandler:
    """Task handler that records task execution details into a local text file"""

    async def handle(self, task: Task):
        """Write task information to text file"""

        try:
            report_path = 'task_report.txt'

            async with aiofiles.open(report_path, mode='a', encoding='utf-8') as f:
                report_line = f"ID: {task.id} | Status: {task.status} | Priority: {task.priority} | Created: {task.created_at} | Data: {task.payload}\n"
                await f.write(report_line)
            logging.info(f"Successfully wrote to file. Task id: {task.id}")
        except:
            logging.error(f"Error writing task to file. Task id: {task.id}")
            task.status = 'failed'
            
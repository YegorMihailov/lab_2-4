import json
from src.models import Task
from typing import AsyncIterator
import aiofiles

class FileTaskSource:
    """Task source that reads and parses task data from JSON file"""

    def __init__(self, filename: str):
        self.filename = filename


    async def get_tasks(self) -> AsyncIterator[Task]:
        """Read and parse tasks from the JSON file"""
        
        try:
            async with aiofiles.open(self.filename, mode='r', encoding='utf-8') as f:
                content = await f.read()
                data = json.loads(content)

                for task in data:
                    yield Task(
                        id=task["id"], payload=task["payload"], description=task["payload"]["description"], priority=task["priority"]
                        )
                    
        except Exception as e:
            raise ValueError(f"Error: {e}")
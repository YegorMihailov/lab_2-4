import asyncio
import logging
from src.models import TaskQueue
from src.executor import TaskExecutor
from src.handlers import FileHandler, LoggingHandler
from src.sources import ApiTaskSource, FileTaskSource, GeneratorTaskSource

async def run_tasks():
    """Main entry point for the task processing application"""

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    queue = TaskQueue()

    sources = [
        GeneratorTaskSource(),
        ApiTaskSource(),
        FileTaskSource('input.json')
    ]

    logging.info("Loading tasks from sources")

    for source in sources:
        try:
            async for task in source.get_tasks():
                queue.add_task(task)
        except Exception as e:
            logging.error(f"Error loading from source: {e}")

    executor = TaskExecutor(queue)
    executor.register_handler("file", FileHandler())
    executor.register_handler("log", LoggingHandler())

    logging.info("Starting")

    try:
        await executor.run()
    except KeyboardInterrupt:
        logging.info("Stopped by user")
    

if __name__ == "__main__":
    asyncio.run(run_tasks())




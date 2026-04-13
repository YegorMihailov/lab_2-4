from src.sources import TaskSource
from src.models import TaskQueue

def run_tasks(source: TaskSource) -> TaskQueue:
    """Validate the source implements TaskSource protocol and retrieve tasks from it"""

    queue = TaskQueue()

    if not isinstance(source, TaskSource):
        raise TypeError(f"{source} does not match contract TaskSource")
    
    for task in source.get_tasks():
        queue.add_task(task)
    
    return queue




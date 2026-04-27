import pytest, json, random, datetime
import types
from src.main import run_tasks
from src.sources import GeneratorTaskSource, ApiTaskSource, FileTaskSource
from src.models import Task, TaskQueue
from src.executor import TaskExecutor
from src.handlers import FileHandler, LoggingHandler

@pytest.mark.asyncio
async def test_main():
    """Test the complete application workflow"""

    try:
        await run_tasks()
    except Exception as e:
        pytest.fail(f"Error: {e}")

@pytest.mark.asyncio
async def test_task_sources(tmp_path):
    """Test that all task sources return valid Task objects"""

    data = [
        {
            "id": 1,
            "payload": {
            "order_id": 5501,
            "amount": 1200,
            "description": "Task description"
            },
            "priority": random.randint(1, 5)
        },
        {
            "id": 2,
            "payload": {
            "order_id": 5502,
            "amount": 450,
            "description": "Task description"
            },
            "priority": random.randint(1, 5)
        },
        {
            "id": 3,
            "payload": {
            "order_id": 5503,
            "amount": 3100,
            "description": "Task description"
            },
            "priority": random.randint(1, 5)
        }
    ]

    dir = tmp_path/"data"
    dir.mkdir()
    file = dir/"data.json"
    
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f)

    sources =[GeneratorTaskSource(), ApiTaskSource(), FileTaskSource(file)]

    for source in sources:
        tasks = []
        async for task in source.get_tasks():
            tasks.append(task)
            assert isinstance(task, Task)
        assert len(tasks) > 0

@pytest.mark.asyncio
async def test_file_task_source_not_found():
    """Test FileTaskSource with non-existent file"""

    source = FileTaskSource("missing.json")

    with pytest.raises(ValueError) as err:
        async for _ in source.get_tasks():
            pass
    
    assert "Error" in str(err.value)

def test_task_creation_and_properties():
    """Test task creation"""

    task = Task(id=1, description="Task description", priority=4, payload={"order_id": 232})
    
    assert task.id == 1
    assert task.description == "Task description"
    assert task.priority == 4
    assert task.status == 'created'
    assert isinstance(task.created_at, datetime.datetime)
    assert task.order_id == 232

def test_task_invalid_id():
    """Test IntegerRange for invalid task id"""

    with pytest.raises(ValueError):
        Task(id=0, description="Task description", priority=3)
    with pytest.raises(TypeError):
        Task(id="1", description="Task description", priority=3)

def test_task_invalid_priority():
    """Test IntegerRange for invalid task priority"""

    with pytest.raises(ValueError):
        Task(id=1, description="Valid Desc", priority=6)

def test_task_invalid_description():
    """Test invalid task description"""

    with pytest.raises(ValueError):
        Task(id=1, description="A", priority=3)

def test_task_ready_to_start():
    """Test task computed property ready_to_start"""

    task = Task(id=1, description="Task description", priority=3)
    assert task.ready_to_start is True
    
    task.status = 'in_progress'
    assert task.ready_to_start is False

@pytest.mark.asyncio
async def test_add_task():
    """Test that tasks are correctly added and stored in the queue"""

    queue = TaskQueue()
    task1 = Task(id=1, description="Task desciption", priority=1)
    queue.add_task(task1)

    tasks = []

    async for task in queue:
        tasks.append(task)
        
    assert len(tasks) == 1
    assert isinstance(tasks[0], Task)

@pytest.mark.asyncio
async def test_filters_lazy():
    """Test that filtering methods return generator objects"""

    queue = TaskQueue()
    task1 = Task(id=1, description="Task desciption", priority=1)
    queue.add_task(task1)

    tasks = []

    async for task in queue:
        tasks.append(task)

    assert isinstance(queue.filter_by_priority(1, 5), types.AsyncGeneratorType)

@pytest.mark.asyncio
async def test_filter_by_priority():
    """Test if the priority filter correctly identifies tasks within priority range"""

    queue = TaskQueue()

    task1 = Task(id=1, description="Task desciption", priority=1)
    task2 = Task(id=2, description="Task desciption", priority=3)
    task3 = Task(id=3, description="Task desciption", priority=5)
    
    queue.add_task(task1)
    queue.add_task(task2)
    queue.add_task(task3)

    tasks = []

    async for task in queue.filter_by_priority(2, 4):
        tasks.append(task)

    assert len(tasks) == 1
    assert tasks[0].id == 2

@pytest.mark.asyncio
async def test_filter_by_status():
    """Test if the status filter correctly identifies tasks by status"""

    queue = TaskQueue()

    task1 = Task(id=1, description="Task desciption", priority=1)
    task2 = Task(id=2, description="Task desciption", priority=5)
    
    queue.add_task(task1)
    queue.add_task(task2)

    tasks = []

    async for task in queue.filter_by_status('created'):
        tasks.append(task)

    assert len(tasks) == 2

@pytest.mark.asyncio
async def test_queue_repeat_iteration():
    """Test that the queue can be iterated multiple times without exhausting data"""

    queue = TaskQueue()
    queue.add_task(Task(id=1, description="Task desciption", priority=1))
    
    res1 = [task async for task in queue]
    res2 = [task async for task in queue]

    assert len(res1) == len(res2) == 1

@pytest.mark.asyncio
async def test_executor_with_handler():
    """Test the TaskExecutor ability to dispatch tasks to appropriate handlers"""

    queue = TaskQueue()

    task1 = Task(id=77, payload={"type": "log"}, description="Task description", priority=1)
    task2 = Task(id=78, payload={"type": "file"}, description="Task description", priority=2)
    
    queue.add_task(task1)
    queue.add_task(task2)
    
    executor = TaskExecutor(queue)
    executor.register_handler("log", LoggingHandler())
    executor.register_handler("file", FileHandler())
    
    await executor.run()

async def test_filters_async_generator():
    """Test that filters return AsyncGenerator objects"""
    
    queue = TaskQueue()
    assert isinstance(queue.filter_by_priority(1, 5), types.AsyncGeneratorType)
    assert isinstance(queue.filter_by_status("created"), types.AsyncGeneratorType)


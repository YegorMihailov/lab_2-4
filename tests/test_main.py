import pytest, json, random, datetime
from src.main import run_tasks
from src.sources import GeneratorTaskSource, ApiTaskSource, FileTaskSource
from src.models import Task
from src.models import TaskQueue
import types

def test_run_tasks(tmp_path):
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
        tasks = run_tasks(source)
        assert all(isinstance(task, Task) for task in tasks)
        assert isinstance(tasks, TaskQueue)


def test_wrong_source():
    """Test run_tasks with invalid source"""

    with pytest.raises(TypeError) as err:
        run_tasks("invalid_source")
    assert "does not match contract TaskSource" in str(err.value)

def test_file_task_source_not_found():
    """Test FileTaskSource with non-existent file"""

    source = FileTaskSource("missing.json")

    with pytest.raises(ValueError) as err:
        source.get_tasks()
    
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

def test_add_task():
    """Test that tasks are correctly added and stored in the queue"""

    queue = TaskQueue()
    task1 = Task(id=1, description="Task desciption", priority=1)

    queue.add_task(task1)
    assert isinstance(list(queue)[0], Task)
    assert len(queue) == 1

def test_filters_lazy():
    """Test that filtering methods return generator objects"""

    queue = TaskQueue()
    task1 = Task(id=1, description="Task desciption", priority=1)
    queue.add_task(task1)
    assert isinstance(queue.filter_by_priority(1, 5), types.GeneratorType)

def test_filter_by_priority():
    """Test if the priority filter correctly identifies tasks within priority range"""

    queue = TaskQueue()

    task1 = Task(id=1, description="Task desciption", priority=1)
    task2 = Task(id=2, description="Task desciption", priority=3)
    task3 = Task(id=3, description="Task desciption", priority=5)
    
    queue.add_task(task1)
    queue.add_task(task2)
    queue.add_task(task3)

    assert len(list(queue.filter_by_priority(2, 4))) == 1
    assert next(queue.filter_by_priority(2, 4)).id == 2

def test_filter_by_status():
    """Test if the status filter correctly identifies tasks by status"""

    queue = TaskQueue()

    task1 = Task(id=1, description="Task desciption", priority=1)
    task2 = Task(id=2, description="Task desciption", priority=5)
    
    queue.add_task(task1)
    queue.add_task(task2)

    assert len(list(queue.filter_by_status('created'))) == 2

def test_queue_repeat_iteration():
    """Test that the queue can be iterated multiple times without exhausting data"""

    queue = TaskQueue()
    queue.add_task(Task(id=1, description="Task desciption", priority=1))
    
    pass1 = list(queue)
    pass2 = list(queue)
    
    assert len(pass1) == len(pass2) == 1

def test_stop_iteration():
    """Test the iterator raises StopIteration after the last element"""

    queue = TaskQueue()
    queue.add_task(Task(id=1, description="Task desciption", priority=1))
    
    iterator = iter(queue)
    next(iterator)
    
    with pytest.raises(StopIteration):
        next(iterator)

# def test_sum_compatibility():
#     count = sum(1 for _ in queue)
#     assert count == len(queue)
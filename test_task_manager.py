# tests/test_task_manager.py
import pytest
import json
from task_manager import TaskManager
from task import Task
from category import Category
import os

@pytest.fixture
def task_manager(tmp_path):
    """Фикстура для создания временного TaskManager."""
    task_file = tmp_path / "tasks.json"
    category_file = tmp_path / "categories.json"
    # Создаем начальную категорию "General"
    with open(category_file, 'w') as f:
        json.dump([{"name": "General"}], f)
    return TaskManager(task_filename=str(task_file), category_filename=str(category_file))

def test_add_category(task_manager):
    """Тест добавления новой категории."""
    # Arrange (Подготовка) - TaskManager инициализирован с категорией "General"

    # Act (Действие)
    added_shopping = task_manager.add_category("Shopping")
    added_existing = task_manager.add_category("General") # Попытка добавить существующую

    # Assert (Проверка)
    assert added_shopping is True
    assert added_existing is False
    assert any(cat.name == "Shopping" for cat in task_manager.categories)
    assert len(task_manager.categories) == 2 # General и Shopping

def test_delete_category_and_tasks(task_manager):
    """Тест удаления категории и связанных задач."""
    # Arrange
    task_manager.add_category("Shopping")
    task1 = Task(1, "Buy Milk", "Grocery store", "низкий", "05.01.2024", "General")
    task2 = Task(2, "Buy Bread", "Bakery", "средний", "05.01.2024", "Shopping")
    task_manager.add_task(task1)
    task_manager.add_task(task2)

    assert len(task_manager.get_tasks()) == 2
    assert len(task_manager.categories) == 2 # General и Shopping

    # Act
    deleted_shopping = task_manager.delete_category("Shopping")
    deleted_nonexistent = task_manager.delete_category("Work") # Попытка удалить несуществующую

    # Assert
    assert deleted_shopping is True
    assert deleted_nonexistent is False
    assert len(task_manager.categories) == 1 # Осталась только General
    assert not any(cat.name == "Shopping" for cat in task_manager.categories)
    assert len(task_manager.get_tasks()) == 1 # Осталась только task1
    assert task_manager.get_task(1) is not None
    assert task_manager.get_task(2) is None

def test_load_categories(tmp_path):
    """Тест загрузки категорий из файла."""
    # Arrange
    category_file = tmp_path / "categories.json"
    initial_data = [{"name": "Work"}, {"name": "Home"}]
    with open(category_file, 'w') as f:
        json.dump(initial_data, f)

    # Act
    tm = TaskManager(category_filename=str(category_file))

    # Assert
    assert len(tm.categories) == 2
    assert tm.categories[0].name == "Work"
    assert tm.categories[1].name == "Home"

def test_load_categories_file_not_found(tmp_path):
    """Тест загрузки категорий при отсутствии файла."""
    # Arrange - файл не создается

    # Act
    tm = TaskManager(category_filename=str(tmp_path / "nonexistent_categories.json"))

    # Assert
    assert len(tm.categories) == 0

def test_add_task_with_existing_category(task_manager):
    """Тест добавления задачи с существующей категорией."""
    # Arrange - TaskManager инициализирован с категорией "General"
    task = Task(1, "Buy Milk", "Grocery store", "низкий", "05.01.2024", "General")

    # Act
    task_manager.add_task(task)

    # Assert
    assert len(task_manager.get_tasks()) == 1
    assert task_manager.get_task(1) == task # Проверяем, что задача добавлена и ее можно получить

def test_add_task_with_nonexistent_category(task_manager):
    """Тест добавления задачи с несуществующей категорией (негативный сценарий)."""
    # Arrange
    task = Task(1, "Buy Milk", "Grocery store", "низкий", "05.01.2024", "Shopping") # Категория "Shopping" не добавлена

    # Act & Assert
    with pytest.raises(ValueError, match="Категория не существует."):
        task_manager.add_task(task)
    assert len(task_manager.get_tasks()) == 0 # Задача не должна быть добавлена

def test_update_task(task_manager):
    """Тест обновления существующей задачи."""
    # Arrange
    task1 = Task(1, "Task 1", "Desc 1", "низкий", "01.01.2024", "General")
    task_manager.add_task(task1)
    updated_task = Task(1, "Updated Task 1", "Updated Desc 1", "высокий", "02.01.2024", "General", completed=True)

    # Act
    updated = task_manager.update_task(1, updated_task)
    updated_nonexistent = task_manager.update_task(999, updated_task) # Попытка обновить несуществующую

    # Assert
    assert updated is True
    assert updated_nonexistent is False
    retrieved_task = task_manager.get_task(1)
    assert retrieved_task is not None
    assert retrieved_task.title == "Updated Task 1"
    assert retrieved_task.completed is True

def test_delete_task(task_manager):
    """Тест удаления задачи по ID."""
    # Arrange
    task1 = Task(1, "Task 1", "Desc 1", "низкий", "01.01.2024", "General")
    task2 = Task(2, "Task 2", "Desc 2", "средний", "02.01.2024", "General")
    task_manager.add_task(task1)
    task_manager.add_task(task2)
    assert len(task_manager.get_tasks()) == 2

    # Act
    task_manager.delete_task(1) # Удаляем первую задачу

    # Assert
    assert len(task_manager.get_tasks()) == 1
    assert task_manager.get_task(1) is None # Проверяем, что первая задача удалена
    assert task_manager.get_task(2) is not None # Проверяем, что вторая осталась

def test_get_tasks(task_manager):
    """Тест получения всех задач."""
    # Arrange
    task1 = Task(1, "Task 1", "Desc 1", "низкий", "01.01.2024", "General")
    task2 = Task(2, "Task 2", "Desc 2", "средний", "02.01.2024", "General")
    task_manager.add_task(task1)
    task_manager.add_task(task2)

    # Act
    tasks = task_manager.get_tasks()

    # Assert
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[1].id == 2

def test_get_tasks_by_category(task_manager):
    """Тест получения задач по категории."""
    # Arrange
    task_manager.add_category("Work")
    task1 = Task(1, "Task 1", "Desc 1", "низкий", "01.01.2024", "General")
    task2 = Task(2, "Task 2", "Desc 2", "средний", "02.01.2024", "Work")
    task3 = Task(3, "Task 3", "Desc 3", "высокий", "03.01.2024", "General")
    task_manager.add_task(task1)
    task_manager.add_task(task2)
    task_manager.add_task(task3)

    # Act
    general_tasks = task_manager.get_tasks_by_category("General")
    work_tasks = task_manager.get_tasks_by_category("Work")
    nonexistent_tasks = task_manager.get_tasks_by_category("Shopping")

    # Assert
    assert len(general_tasks) == 2
    assert all(task.category == "General" for task in general_tasks)
    assert len(work_tasks) == 1
    assert all(task.category == "Work" for task in work_tasks)
    assert len(nonexistent_tasks) == 0

def test_get_task(task_manager):
    """Тест получения задачи по ID."""
    # Arrange
    task1 = Task(1, "Task 1", "Desc 1", "низкий", "01.01.2024", "General")
    task_manager.add_task(task1)

    # Act
    found_task = task_manager.get_task(1)
    not_found_task = task_manager.get_task(999)

    # Assert
    assert found_task is not None
    assert found_task.id == 1
    assert not_found_task is None

def test_load_tasks(tmp_path):
    """Тест загрузки задач из файла."""
    # Arrange
    task_file = tmp_path / "tasks.json"
    category_file = tmp_path / "categories.json"
    # Создаем начальную категорию "General"
    with open(category_file, 'w') as f:
        json.dump([{"name": "General"}], f)

    initial_data = [
        {"id": 1, "title": "Task 1", "description": "Desc 1", "priority": "низкий", "due_date": "01.01.2024", "category": "General", "completed": False},
        {"id": 2, "title": "Task 2", "description": "Desc 2", "priority": "средний", "due_date": "02.01.2024", "category": "General", "completed": True}
    ]
    with open(task_file, 'w') as f:
        json.dump(initial_data, f)

    # Act
    tm = TaskManager(task_filename=str(task_file), category_filename=str(category_file))

    # Assert
    assert len(tm.tasks) == 2
    assert tm.tasks[0].id == 1
    assert tm.tasks[1].completed is True

def test_load_tasks_file_not_found(tmp_path):
    """Тест загрузки задач при отсутствии файла."""
    # Arrange - файл не создается
    category_file = tmp_path / "categories.json"
    with open(category_file, 'w') as f:
        json.dump([{"name": "General"}], f)

    # Act
    tm = TaskManager(task_filename=str(tmp_path / "nonexistent_tasks.json"), category_filename=str(category_file))

    # Assert
    assert len(tm.tasks) == 0
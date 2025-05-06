# tests/test_task.py
import pytest
from task import Task

def test_create_task():
    """Тест создания объекта задачи."""
    # Arrange (Подготовка)
    task = Task(1, "Test Task", "Description", "низкий", "01.01.2024", "Work")

    # Act (Действие) - Нет прямого действия, только создание объекта

    # Assert (Проверка)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Description"
    assert task.priority == "низкий"
    assert task.due_date == "01.01.2024"
    assert task.category == "Work"
    assert task.completed is False

def test_mark_task_as_completed():
    """Тест отметки задачи как выполненной."""
    # Arrange
    task = Task(1, "Test Task", "Description", "низкий", "01.01.2024", "Work")

    # Act
    task.mark_as_completed()

    # Assert
    assert task.completed is True

def test_task_repr():
    """Тест строкового представления задачи."""
    # Arrange
    task = Task(1, "Test Task", "Description", "низкий", "01.01.2024", "Work")
    expected_repr = ("Task(id=1, title=Test Task, description=Description, "
                     "priority=низкий, due_date=01.01.2024, category=Work, "
                     "completed=False)")

    # Act (Нет прямого действия)

    # Assert
    assert repr(task) == expected_repr
# tests/test_category.py
import pytest
from category import Category

def test_create_category():
    """Тест создания объекта категории."""
    # Arrange
    category = Category("Work")

    # Act (Нет прямого действия)

    # Assert
    assert category.name == "Work"

def test_category_repr():
    """Тест строкового представления категории."""
    # Arrange
    category = Category("Work")

    # Act (Нет прямого действия)

    # Assert
    assert repr(category) == "Category(name=Work)"
import json
from task import Task
from category import Category  # Импорт класса Category

class TaskManager:
    def __init__(self, task_filename='tasks.json', category_filename='categories.json'):
        self.tasks = []
        self.categories = []
        self.task_filename = task_filename
        self.category_filename = category_filename
        self.load_tasks()
        self.load_categories()

    def add_category(self, category_name):
        """Добавление новой категории"""
        if any(category.name == category_name for category in self.categories):
            return False  # категория уже существует
        self.categories.append(Category(category_name))
        self.save_categories()
        return True

    def delete_category(self, category_name):
        """Удаление категории по имени"""
        if not any(category.name == category_name for category in self.categories):
            return False  # категория не найдена

        # Удаляем категорию
        self.categories = [category for category in self.categories if category.name != category_name]
        self.save_categories()

        # Удаляем все задачи, связанные с этой категорией
        self.tasks = [task for task in self.tasks if task.category != category_name]
        self.save_tasks()
        return True

    def load_categories(self):
        """Загрузка категорий из файла"""
        try:
            with open(self.category_filename, 'r') as f:
                categories_data = json.load(f)
                self.categories = [Category(**cat) for cat in categories_data]
        except FileNotFoundError:
            self.categories = []
        except json.JSONDecodeError:
            print("Ошибка при чтении файла категорий, возможно, он поврежден.")

    def save_categories(self):
        """Сохранение категорий в файл"""
        with open(self.category_filename, 'w') as f:
            json.dump([category.__dict__ for category in self.categories], f)

    def add_task(self, task):
        """Добавление новой задачи"""
        if not any(category.name == task.category for category in self.categories):
            raise ValueError("Категория не существует.")  # Исключение, если категория не найдена
        self.tasks.append(task)
        self.save_tasks()

    def update_task(self, id, updated_task):
        """Обновление задачи по идентификатору"""
        for index, task in enumerate(self.tasks):
            if task.id == id:
                self.tasks[index] = updated_task
                self.save_tasks()
                return True
        return False

    def delete_task(self, id):
        """Удаление задачи по идентификатору"""
        self.tasks = [task for task in self.tasks if task.id != id]
        self.save_tasks()

    def get_tasks(self):
        """Получение всех задач"""
        return self.tasks

    def get_tasks_by_category(self, category_name):
        """Получение задач по категории"""
        return [task for task in self.tasks if task.category == category_name]

    def get_task(self, id):
        """Получение задачи по идентификатору"""
        for task in self.tasks:
            if task.id == id:
                return task
        return None

    def save_tasks(self):
        """Сохранение задач в файл"""
        with open(self.task_filename, 'w') as f:
            json.dump([task.__dict__ for task in self.tasks], f)

    def load_tasks(self):
        """Загрузка задач из файла"""
        try:
            with open(self.task_filename, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = [Task(**task) for task in tasks_data]
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            print("Ошибка при чтении файла задач, возможно, он поврежден.")
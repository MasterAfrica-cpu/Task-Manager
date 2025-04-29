import re
from task import Task
from task_manager import TaskManager


def is_valid_date(date_str):
    pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    return re.match(pattern, date_str)


def is_valid_priority(priority):
    return priority in ['низкий', 'средний', 'высокий']


def main():
    task_manager = TaskManager()

    while True:
        print("\nМеню:")
        print("1. Добавить задачу")
        print("2. Обновить задачу")
        print("3. Удалить задачу")
        print("4. Просмотреть все задачи")
        print("5. Пометить задачу как выполненную")
        print("6. Создать категорию")
        print("7. Удалить категорию")
        print("8. Просмотреть все категории")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            print("\nДоступные категории:")
            for category in task_manager.categories:
                print(category.name)

            title = input("Заголовок задачи: ")
            description = input("Описание задачи: ")
            priority = input("Приоритет (низкий, средний, высокий): ")
            while not is_valid_priority(priority):
                print("Некорректный приоритет. Пожалуйста, введите 'низкий', 'средний' или 'высокий'.")
                priority = input("Приоритет (низкий, средний, высокий): ")

            due_date = input("Срок выполнения (ДД.ММ.ГГГГ): ")
            while not is_valid_date(due_date):
                print("Некорректный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ.")
                due_date = input("Срок выполнения (ДД.ММ.ГГГГ): ")

            category = input("Категория: ")
            task_id = len(task_manager.tasks) + 1

            try:
                task_manager.add_task(Task(task_id, title, description, priority, due_date, category))
                print("Задача добавлена.")
            except ValueError as e:
                print(e)

        elif choice == '2':
            # Логика обновления задачи...

            task_id = int(input("Введите ID задачи для обновления: "))
            # Логика обновления задачи...

        elif choice == '3':
            task_id = int(input("Введите ID задачи для удаления: "))
            task_manager.delete_task(task_id)
            print("Задача удалена.")

        elif choice == '4':
            print("\nВыберите категорию для просмотра задач (или нажмите Enter для просмотра всех):")
            for category in task_manager.categories:
                print(category.name)

            category_name = input("Категория: ")
            tasks_to_display = task_manager.get_tasks()

            if category_name:
                tasks_to_display = [task for task in tasks_to_display if task.category == category_name]
                if not tasks_to_display:
                    print(f"Нет задач в категории '{category_name}'.")
                for task in tasks_to_display:
                    print(task)
            else:
                for task in tasks_to_display:
                    print(task)

        elif choice == '5':
            task_id = int(input("Введите ID задачи для отметки как выполненной: "))
            task = task_manager.get_task(task_id)
            if task:
                task.mark_as_completed()
                task_manager.update_task(task_id, task)
                print("Задача помечена как выполненная.")

        elif choice == '6':
            category_name = input("Введите название категории: ")
            if task_manager.add_category(category_name):
                print(f"Категория '{category_name}' добавлена.")
            else:
                print(f"Категория '{category_name}' уже существует.")

        elif choice == '7':
            category_name = input("Введите название категории для удаления: ")
            task_manager.delete_category(category_name)
            print(f"Категория '{category_name}' и все связанные задачи были удалены.")

        elif choice == '8':
            print("\nСозданные категории:")
            for category in task_manager.categories:
                print(category.name)

        elif choice == '0':
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
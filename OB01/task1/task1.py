import datetime

class Task:
    task_list = []

    def __init__(self, description, date, status=0):
        self.description = description  # Описание задачи
        self.date = self.convert_to_date(date)  # Дата выполнения (или None, если формат неверный)
        self.status = status  # Статус (0 - не выполнено, 1 - выполнено)

    def __str__(self):
        date_str = self.date.strftime('%d.%m.%Y') if self.date else '∞'
        return f"[{'✔' if self.status else ' '}] {self.description} (до {date_str})"

    @staticmethod
    def convert_to_date(date_string):
        """Преобразует строку в объект даты, если формат верный"""
        try:
            return datetime.datetime.strptime(date_string, "%d.%m.%Y").date()
        except ValueError:
            print(f"❌ Некорректный формат даты: {date_string}")
            return None

    @classmethod
    def add(cls, description, date):
        """Добавляет задачу в список (проверяет дату)"""
        new_task = cls(description, date, 0)
        cls.task_list.append(new_task)

    def check(self):
        """Отмечает задачу как выполненную"""
        self.status = 1

    @classmethod
    def print(cls):
        """Выводит список невыполненных задач"""
        tasks = [task for task in cls.task_list if task.status == 0]

        if tasks:
            print("\n📌 Список задач:")
            for task in tasks:
                print(task)
        else:
            print("\n✅ Все задачи выполнены!")

def main():
    Task.add("Сделать OB01", "20.02.2025")  # Корректная дата
    Task.add("Почитать книгу", "25.02.2025")  # Корректная дата
    Task.add("Ошибка в дате", "31.02.2025")  # Некорректная дата

    Task.print()  # Выведет задачи

    # Отметим первую задачу как выполненную
    Task.task_list[0].check()

    print("\n📌 После обновления статуса:")
    Task.print()  # Выведет только невыполненные задачи

if __name__ == "__main__":
    main()

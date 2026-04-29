import json
import random
from pathlib import Path
from typing import List, Dict, Optional

HISTORY_FILE = Path("tasks.json")

# Предопределённый пул задач с категориями
DEFAULT_TASKS: Dict[str, List[str]] = {
    "учёба": [
        "Прочитать статью",
        "Решить 5 задач по математике",
        "Посмотреть лекцию",
        "Повторить конспект",
        "Выучить 10 новых слов"
    ],
    "спорт": [
        "Сделать зарядку",
        "Пробежать 3 км",
        "Выполнить 20 отжиманий",
        "Позаниматься йогой 15 минут",
        "Растяжка на 10 минут"
    ],
    "работа": [
        "Проверить почту",
        "Написать отчёт",
        "Созвониться с клиентом",
        "Подготовить презентацию",
        "Обновить задачи в трекере"
    ]
}

class TaskManager:
    """Управляет задачами, историей и сохранением в JSON."""

    def __init__(self):
        self.tasks_pool = self._copy_default_tasks()
        self.history: list = []  # список сгенерированных задач (dict: description, type, timestamp?)
        self.load_history()

    def _copy_default_tasks(self) -> Dict[str, List[str]]:
        """Глубокое копирование исходного словаря задач."""
        return {k: v.copy() for k, v in DEFAULT_TASKS.items()}

    # --- работа с пулом задач ---
    def add_task(self, description: str, task_type: str) -> bool:
        """Добавляет задачу в пул. Возвращает True, если успешно."""
        description = description.strip()
        if not description:
            return False
        if task_type not in self.tasks_pool:
            # Можно создать новую категорию, но ограничимся существующими
            return False
        self.tasks_pool[task_type].append(description)
        return True

    def get_tasks_by_type(self, task_type: Optional[str]) -> List[str]:
        """Возвращает список задач заданного типа. Если None — все задачи."""
        if task_type and task_type in self.tasks_pool:
            return self.tasks_pool[task_type]
        all_tasks = []
        for lst in self.tasks_pool.values():
            all_tasks.extend(lst)
        return all_tasks

    # --- генерация случайной задачи ---
    def generate_random_task(self, task_type: Optional[str] = None) -> Optional[Dict]:
        """
        Выбирает случайную задачу из пула.
        Можно указать тип (учёба/спорт/работа) или None для всех.
        Возвращает словарь {'description': ..., 'type': ...} или None, если пул пуст.
        """
        tasks = self.get_tasks_by_type(task_type)
        if not tasks:
            return None
        description = random.choice(tasks)
        # Определяем тип по тому, где лежит description (возможны дубликаты – берём первый)
        for cat, lst in self.tasks_pool.items():
            if description in lst:
                cat_name = cat
                break
        else:
            cat_name = "неизвестно"
        task = {"description": description, "type": cat_name}
        self.history.append(task)
        self.save_history()
        return task

    # --- история и фильтрация ---
    def get_filtered_history(self, task_type: Optional[str] = None) -> List[Dict]:
        """Возвращает историю, отфильтрованную по типу задачи. Если None – всю."""
        if not task_type:
            return self.history
        return [t for t in self.history if t["type"] == task_type]

    # --- JSON сохранение/загрузка ---
    def save_history(self):
        """Сохраняет историю в JSON-файл."""
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def load_history(self):
        """Загружает историю из JSON-файла, если он существует."""
        if HISTORY_FILE.is_file():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, ValueError):
                self.history = []
        else:
            self.history = []
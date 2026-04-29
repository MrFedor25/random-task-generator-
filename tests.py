import pytest
from task_manager import TaskManager

@pytest.fixture
def fresh_manager():
    """Свежий менеджер с очищенной историей и стандартным пулом."""
    mgr = TaskManager()
    mgr.history = []
    return mgr

class TestAddTask:
    """Тесты добавления задачи в пул."""

    def test_add_normal_task(self, fresh_manager):
        assert fresh_manager.add_task("Новая рабочая задача", "работа")
        assert "Новая рабочая задача" in fresh_manager.tasks_pool["работа"]

    def test_add_empty_description(self, fresh_manager):
        assert not fresh_manager.add_task("   ", "учёба")
        assert not fresh_manager.add_task("", "спорт")

    def test_add_invalid_type(self, fresh_manager):
        assert not fresh_manager.add_task("Задача", "хобби")  # неизвестный тип

    def test_add_same_task_multiple_types(self, fresh_manager):
        fresh_manager.add_task("Общая задача", "учёба")
        fresh_manager.add_task("Общая задача", "спорт")
        assert "Общая задача" in fresh_manager.tasks_pool["учёба"]
        assert "Общая задача" in fresh_manager.tasks_pool["спорт"]

class TestGenerateRandomTask:
    """Тесты генерации случайной задачи."""

    def test_generate_all_types(self, fresh_manager):
        task = fresh_manager.generate_random_task()
        assert task is not None
        assert "description" in task
        assert "type" in task
        assert task["type"] in ("учёба", "спорт", "работа")

    def test_generate_filtered_type(self, fresh_manager):
        task = fresh_manager.generate_random_task("спорт")
        assert task["type"] == "спорт"

    def test_generate_empty_pool(self, fresh_manager):
        # Очистим все задачи
        fresh_manager.tasks_pool = {"учёба": [], "спорт": [], "работа": []}
        task = fresh_manager.generate_random_task()
        assert task is None

    def test_history_updated(self, fresh_manager):
        before = len(fresh_manager.history)
        fresh_manager.generate_random_task()
        assert len(fresh_manager.history) == before + 1

class TestHistoryFilter:
    """Фильтрация истории."""

    def test_filter_by_existing_type(self, fresh_manager):
        fresh_manager.history = [
            {"description": "A", "type": "учёба"},
            {"description": "B", "type": "спорт"},
            {"description": "C", "type": "учёба"},
        ]
        filtered = fresh_manager.get_filtered_history("учёба")
        assert len(filtered) == 2
        assert all(t["type"] == "учёба" for t in filtered)

    def test_filter_by_absent_type(self, fresh_manager):
        fresh_manager.history = [{"description": "A", "type": "работа"}]
        filtered = fresh_manager.get_filtered_history("спорт")
        assert filtered == []

    def test_no_filter_returns_all(self, fresh_manager):
        fresh_manager.history = [{"description": "X", "type": "спорт"}]
        assert len(fresh_manager.get_filtered_history(None)) == 1

class TestJSONPersistence:
    """Сохранение и загрузка из JSON (используется реальный файл)."""

    def test_save_and_load(self, tmp_path, monkeypatch):
        import task_manager as tm
        test_file = tmp_path / "test_history.json"
        monkeypatch.setattr(tm, "HISTORY_FILE", test_file)

        mgr = TaskManager()
        mgr.history = [{"description": "Test", "type": "учёба"}]
        mgr.save_history()

        # Новый менеджер должен загрузить историю
        mgr2 = TaskManager()
        mgr2.load_history()
        assert mgr2.history == [{"description": "Test", "type": "учёба"}]
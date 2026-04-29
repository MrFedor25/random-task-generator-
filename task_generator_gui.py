import tkinter as tk
from tkinter import ttk, messagebox
from task_manager import TaskManager

class TaskGeneratorApp:
    """Графический интерфейс приложения Random Task Generator."""

    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x550")

        self.manager = TaskManager()

        # Строка добавления новой задачи
        add_frame = ttk.LabelFrame(root, text="Добавить новую задачу")
        add_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(add_frame, text="Описание:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.new_task_desc = ttk.Entry(add_frame, width=40)
        self.new_task_desc.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Тип:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.new_task_type = ttk.Combobox(add_frame, values=["учёба", "спорт", "работа"], state="readonly", width=12)
        self.new_task_type.current(0)  # по умолчанию учёба
        self.new_task_type.grid(row=0, column=3, padx=5, pady=5)

        add_btn = ttk.Button(add_frame, text="Добавить", command=self.add_task)
        add_btn.grid(row=0, column=4, padx=10, pady=5)

        # Блок генерации случайной задачи
        gen_frame = ttk.LabelFrame(root, text="Сгенерировать случайную задачу")
        gen_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(gen_frame, text="Фильтр по типу:").pack(side="left", padx=5)
        self.gen_type_var = tk.StringVar(value="Все")
        self.gen_type_combo = ttk.Combobox(gen_frame, textvariable=self.gen_type_var,
                                           values=["Все", "учёба", "спорт", "работа"],
                                           state="readonly", width=14)
        self.gen_type_combo.pack(side="left", padx=5)

        generate_btn = ttk.Button(gen_frame, text="Сгенерировать задачу", command=self.generate_task)
        generate_btn.pack(side="left", padx=20)

        # Блок отображения истории
        hist_frame = ttk.LabelFrame(root, text="История сгенерированных задач")
        hist_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Фильтр истории
        hist_filter_frame = ttk.Frame(hist_frame)
        hist_filter_frame.pack(fill="x", padx=5, pady=2)

        ttk.Label(hist_filter_frame, text="Показать:").pack(side="left")
        self.hist_filter = tk.StringVar(value="Все")
        hist_combo = ttk.Combobox(hist_filter_frame, textvariable=self.hist_filter,
                                  values=["Все", "учёба", "спорт", "работа"],
                                  state="readonly", width=14)
        hist_combo.pack(side="left", padx=5)
        hist_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_history())

        # Список (Listbox) с историей
        self.history_listbox = tk.Listbox(hist_frame, height=12, font=("Courier", 10))
        self.history_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(hist_frame, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        self.refresh_history()

    def add_task(self):
        """Обработчик кнопки добавления задачи."""
        desc = self.new_task_desc.get().strip()
        task_type = self.new_task_type.get()
        if not desc:
            messagebox.showerror("Ошибка", "Описание задачи не может быть пустым.")
            return
        success = self.manager.add_task(desc, task_type)
        if success:
            messagebox.showinfo("Успех", f"Задача '{desc}' добавлена в категорию '{task_type}'.")
            self.new_task_desc.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", "Не удалось добавить задачу (неверный тип?).")

    def generate_task(self):
        """Генерирует случайную задачу с учётом выбранного фильтра."""
        selected_type = self.gen_type_var.get()
        if selected_type == "Все":
            task_type = None
        else:
            task_type = selected_type

        task = self.manager.generate_random_task(task_type)
        if task is None:
            messagebox.showwarning("Пусто", "Нет задач выбранного типа. Добавьте новые или выберите другую категорию.")
            return

        self.refresh_history()

    def refresh_history(self):
        """Обновляет отображение списка истории с учётом фильтра."""
        self.history_listbox.delete(0, tk.END)
        filter_val = self.hist_filter.get()
        if filter_val == "Все":
            filter_type = None
        else:
            filter_type = filter_val

        tasks = self.manager.get_filtered_history(filter_type)
        for idx, t in enumerate(tasks, 1):
            line = f"{idx:3d}. [{t['type']:6s}] {t['description']}"
            self.history_listbox.insert(tk.END, line)

def main():
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
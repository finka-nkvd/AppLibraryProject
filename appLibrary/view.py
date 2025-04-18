# view.py
import customtkinter as ctk
from tkinter import filedialog, ttk


class LoginView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        self.title("Авторизация")
        self.geometry("315x220")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Логин:").place(x=15, y=40)
        ctk.CTkLabel(self, text="Пароль:").place(x=15, y=120)

        self.login_entry = ctk.CTkEntry(self)
        self.login_entry.place(x=90, y=40)

        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.place(x=90, y=120)

        ctk.CTkButton(self, text="Регистрация", command=self.controller.register).place(x=15, y=175)
        ctk.CTkButton(self, text="Войти", command=self.controller.login).place(x=160, y=175)


class MainView(ctk.CTk):
    def __init__(self, controller, username):
        super().__init__()
        self.controller = controller
        self.username = username
        self._setup_ui()

    def _setup_ui(self):
        self.title("Главное окно")
        self.geometry("1920x1030")

        # Левая панель
        self.app_list = ctk.CTkScrollableFrame(self, width=240)
        self.app_list.pack(side="left", fill="y")

        self.btn_add = ctk.CTkButton(self.app_list, text="Добавить игру", command=self.controller.open_add_app)
        self.btn_add.pack(pady=10)

        # Верхняя панель
        self.top_frame = ctk.CTkFrame(self, height=50)
        self.top_frame.pack(side="top", fill="x")

        ctk.CTkLabel(self.top_frame, text=f"Логин: {self.username}").pack(side="right", padx=10)

        if self.username == "admin":
            ctk.CTkButton(self.top_frame, text="Логи", command=self.controller.open_logs).pack(side="right", padx=10)


class AddAppView(ctk.CTkToplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        self.title("Добавить приложение")
        self.geometry("400x300")

        ctk.CTkLabel(self, text="Имя:").pack(pady=5)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack()

        ctk.CTkLabel(self, text="EXE файл:").pack(pady=5)
        self.btn_browse = ctk.CTkButton(self, text="Выбрать", command=self._browse)
        self.btn_browse.pack()

        ctk.CTkButton(self, text="Сохранить", command=self._save).pack(pady=20)

    def _browse(self):
        self.exe_path = filedialog.askopenfilename(filetypes=[("EXE files", "*.exe")])

    def _save(self):
        self.controller.add_app(
            self.name_entry.get(),
            self.exe_path
        )
        self.destroy()


class LogsView(ctk.CTkToplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        self.title("Логи")
        self.geometry("800x600")

        self.tree = ttk.Treeview(self, columns=("time", "user", "action"), show="headings")
        self.tree.heading("time", text="Время")
        self.tree.heading("user", text="Пользователь")
        self.tree.heading("action", text="Действие")
        self.tree.pack(fill="both", expand=True)

        ctk.CTkButton(self, text="Очистить", command=self.controller.clear_logs).pack(pady=10)
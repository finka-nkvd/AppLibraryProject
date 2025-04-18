# controller.py
from model import UserModel, AppModel, LogModel
from view import LoginView, MainView, AddAppView, LogsView
import subprocess
import hashlib
import shutil
import customtkinter as ctk
from pathlib import Path
from tkinter import messagebox
import json

class AppController:
    def __init__(self):
        self.user_model = UserModel()
        self.app_model = AppModel()
        self.log_model = LogModel()
        self.current_user = None

        self.login_view = LoginView(self)
        self.main_view = None
        self.login_view.mainloop()

    def register(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showerror("Ошибка", "Поля логина и пароля должны быть заполнены")
            return

        try:
            with open('../../data.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        if login in data:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")
            return

        hashed_password = self.hashlib.sha3_256(password.encode()).hexdigest()

        data[login] = hashed_password

        with open('../../data.json', 'w') as file:
            json.dump(data, file)

        messagebox.showinfo("Успех", "Вы успешно зарегистрированы")

    def login_user(self):
        global login
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showerror("Ошибка", "Поля логина и пароля должны быть заполнены")
            return

        try:
            with open('../../data.json', 'r') as file:
                data = json.load(file)

                hashed_input_password = self.hash_password(password)

                if login in data and data[login] == hashed_input_password:
                    messagebox.showinfo("Успех", "Вы успешно вошли в систему")
                    self.logged_in = True
                    self.reg.destroy()
                    self.main_window()
                else:
                    messagebox.showerror("Ошибка", "Неправильный логин или пароль")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл данных не найден")

    def open_add_app(self):
        AddAppView(self)

    def add_app(self, name, exe_path):
        dest = Path("apps") / f"{name}.exe"
        shutil.copy(exe_path, dest)

        self.app_model.add_app(self.current_user, {
            "name": name,
            "path": str(dest),
            "launches": 0
        })
        self.log_model.add_log(f"Добавлено приложение {name}", self.current_user)

    def _load_apps(self):
        for app in self.app_model.apps.get(self.current_user, []):
            btn = ctk.CTkButton(
                self.main_view.app_list,
                text=app["name"],
                command=lambda p=app["path"]: self.launch_app(p)
            )
            btn.pack()

    def launch_app(self, path):
        subprocess.Popen(path)
        self.log_model.add_log(f"Запуск {Path(path).name}", self.current_user)

    def open_logs(self):
        LogsView(self)

    def clear_logs(self):
        self.log_model.logs = []
        self.log_model.save()
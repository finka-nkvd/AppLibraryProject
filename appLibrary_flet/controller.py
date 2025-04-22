import subprocess
from typing import Callable
import flet as ft
import shutil
import hashlib
from pathlib import Path
from view import LoginView, MainView, AppsView, LogsView, AddAppDialog



class AppController:
    def __init__(self, page: ft.Page, models: dict):
        self.page = page
        self.models = models
        self.current_user = None

        # Инициализация представлений
        self.login_view = LoginView(self.login, self.register)
        self.main_view = MainView("", False, self.logout, self.navigate)
        self.apps_view = AppsView(self.show_add_app_dialog, self.launch_app)
        self.logs_view = LogsView(self.filter_logs, self.show_clear_logs_confirmation)

        self.page.title = "Менеджер приложений"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.window_min_width = 800
        self.page.window_min_height = 600

        self.show_login()

    def show_login(self):
        self.page.clean()
        self.page.add(self.login_view.build())
        self.page.update()

    def show_main(self):
        self.page.clean()
        self.main_view.username = self.current_user
        self.main_view.is_admin = self.current_user == "admin"
        self.page.add(self.main_view.build())
        self.show_apps()
        self.page.update()

    def show_apps(self):
        apps = self.models["app"].apps.get(self.current_user, [])
        self.main_view.content_area.clean()
        self.main_view.content_area.controls.append(self.apps_view.build(apps))
        self.main_view.content_area.update()

    def show_logs(self):
        logs = self.models["log"].logs
        users = sorted(set(log["user"] for log in logs))
        self.main_view.content_area.clean()
        self.main_view.content_area.controls.append(
            self.logs_view.build(logs, users)
        )
        self.main_view.content_area.update()

    def register(self, e):
        login = self.login_view.login_field.value
        password = self.login_view.password_field.value

        if not login or not password:
            self.show_snackbar("Поля логина и пароля должны быть заполнены")
            return

        if login in self.models["user"].users:
            self.show_snackbar("Пользователь с таким логином уже существует")
            return

        hashed_password = hashlib.sha3_256(password.encode()).hexdigest()
        self.models["user"].users[login] = hashed_password
        self.models["user"].save()

        self.show_snackbar("Вы успешно зарегистрированы")

    def login(self, e):
        login = self.login_view.login_field.value
        password = self.login_view.password_field.value

        if not login or not password:
            self.show_snackbar("Поля логина и пароля должны быть заполнены")
            return

        hashed_input_password = hashlib.sha3_256(password.encode()).hexdigest()

        if login in self.models["user"].users and self.models["user"].users[login] == hashed_input_password:
            self.current_user = login
            self.models["log"].add_log(f"Пользователь {login} вошел в систему", login)
            self.show_main()
        else:
            self.show_snackbar("Неправильный логин или пароль")

    def logout(self, e):
        self.models["log"].add_log(f"Пользователь {self.current_user} вышел из системы", self.current_user)
        self.current_user = None
        self.show_login()

    def navigate(self, e):
        if e.control.selected_index == 0:
            self.show_apps()
        elif e.control.selected_index == 1:
            self.show_logs()

    def show_add_app_dialog(self, e):
        self.add_app_dialog = AddAppDialog(self.save_app, self.pick_file)
        self.dialog = self.add_app_dialog.build()
        self.dialog.open = True
        self.page.dialog = self.dialog
        self.page.update()

    def pick_file(self, e):
        def on_file_picked(e: ft.FilePickerResultEvent):
            if e.files:
                self.add_app_dialog.exe_path_field.value = e.files[0].path
                self.page.update()

        file_picker = ft.FilePicker(on_result=on_file_picked)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allowed_extensions=["exe"], dialog_title="Выберите .exe файл")

    def save_app(self, e):
        name = self.add_app_dialog.name_field.value
        exe_path = self.add_app_dialog.exe_path_field.value

        if not name or not exe_path:
            self.show_snackbar("Заполните все поля")
            return

        try:
            dest = Path("apps") / f"{name}.exe"
            shutil.copy(exe_path, dest)

            self.models["app"].add_app(self.current_user, {
                "name": name,
                "path": str(dest),
                "launches": 0
            })

            self.models["log"].add_log(f"Добавлено приложение {name}", self.current_user)
            self.show_apps()
            self.dialog.open = False
            self.page.update()
        except Exception as ex:
            self.show_snackbar(f"Ошибка: {str(ex)}")

    def launch_app(self, path):
        try:
            subprocess.Popen(path)
            self.models["log"].add_log(f"Запуск {Path(path).name}", self.current_user)
            self.models["app"].increment_launch_count(self.current_user, path)
            self.show_apps()
        except Exception as ex:
            self.show_snackbar(f"Ошибка запуска: {str(ex)}")

    def filter_logs(self, e):
        user_filter = self.logs_view.user_filter.value
        search_query = self.logs_view.search_field.value

        filtered_logs = self.models["log"].get_filtered_logs(user_filter, search_query)

        self.logs_view.logs_table.rows.clear()
        for log in reversed(filtered_logs):
            self.logs_view.logs_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(log["timestamp"][:19])),
                        ft.DataCell(ft.Text(log["user"])),
                        ft.DataCell(ft.Text(log["action"])),
                    ]
                )
            )
        self.logs_view.logs_table.update()

    def show_clear_logs_confirmation(self, e):
        def confirm_clear(e):
            self.models["log"].clear_logs()
            self.models["log"].add_log("Логи очищены", self.current_user)
            self.show_logs()
            confirm_dialog.open = False
            self.page.update()

        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Подтверждение"),
            content=ft.Text("Вы уверены, что хотите очистить все логи?"),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: setattr(confirm_dialog, "open", False)),
                ft.TextButton("Очистить", on_click=confirm_clear),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()

    def show_snackbar(self, message: str):
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()
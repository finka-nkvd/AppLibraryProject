import flet as ft
from typing import Callable


class LoginView:
    def __init__(self, on_login: Callable, on_register: Callable):
        self.on_login = on_login
        self.on_register = on_register

    def build(self) -> ft.Column:
        self.page.window_width = 1200  # Ширина окна
        self.page.window_height = 800  # Высота окна
        self.page.window_min_width = 800  # Минимальная ширина
        self.page.window_min_height = 600  # Минимальная высота
        self.page.window_resizable = True  # Разрешить изменение размера
        self.page.window_maximized = False  # Не разворачивать на весь экран
        self.login_field = ft.TextField(label="Логин", width=300)
        self.password_field = ft.TextField(label="Пароль", password=True, width=300)

        return ft.Column(
            [
                ft.Text("Авторизация", size=24),
                self.login_field,
                self.password_field,
                ft.Row(
                    [
                        ft.ElevatedButton("Войти", on_click=self.on_login),
                        ft.ElevatedButton("Регистрация", on_click=self.on_register),
                    ],
                    spacing=20
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )


class MainView:
    def __init__(self, username: str, is_admin: bool,
                 on_logout: Callable, on_navigate: Callable):
        self.username = username
        self.is_admin = is_admin
        self.on_logout = on_logout
        self.on_navigate = on_navigate

    def build(self) -> ft.Row:
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.APPS,
                    selected_icon=ft.icons.APPS_OUTLINED,
                    label="Приложения"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.HISTORY,
                    selected_icon=ft.icons.HISTORY_OUTLINED,
                    label="Логи",
                    visible=self.is_admin
                ),
            ],
            on_change=self.on_navigate
        )

        self.header = ft.Row(
            [
                ft.Text(f"Пользователь: {self.username}", size=18),
                ft.IconButton(ft.icons.LOGOUT, on_click=self.on_logout)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.content_area = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

        return ft.Row(
            [
                self.rail,
                ft.VerticalDivider(width=1),
                ft.Column(
                    [
                        self.header,
                        ft.Divider(),
                        self.content_area
                    ],
                    expand=True,
                    spacing=10
                )
            ],
            expand=True
        )


class AppsView:
    def __init__(self, on_add_app: Callable, on_launch_app: Callable):
        self.on_add_app = on_add_app
        self.on_launch_app = on_launch_app

    def build(self, apps: list) -> ft.Column:
        self.apps_list = ft.Column(spacing=10)

        for app in apps:
            self.apps_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.APPS),
                    title=ft.Text(app["name"]),
                    subtitle=ft.Text(f"Запусков: {app.get('launches', 0)}"),
                    on_click=lambda e, path=app["path"]: self.on_launch_app(path),
                )
            )

        return ft.Column(
            [
                ft.ElevatedButton(
                    "Добавить приложение",
                    icon=ft.icons.ADD,
                    on_click=self.on_add_app
                ),
                ft.Divider(),
                self.apps_list
            ]
        )


class LogsView:
    def __init__(self, on_filter_logs: Callable, on_clear_logs: Callable):
        self.on_filter_logs = on_filter_logs
        self.on_clear_logs = on_clear_logs

    def build(self, logs: list, users: list) -> ft.Column:
        self.user_filter = ft.Dropdown(
            label="Пользователь",
            options=[ft.dropdown.Option("Все")] + [
                ft.dropdown.Option(user) for user in sorted(users)
            ],
            on_change=self.on_filter_logs
        )

        self.search_field = ft.TextField(
            label="Поиск по действию",
            on_change=self.on_filter_logs,
            suffix_icon=ft.icons.SEARCH
        )

        self.logs_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Время")),
                ft.DataColumn(ft.Text("Пользователь")),
                ft.DataColumn(ft.Text("Действие"), expand=True),
            ],
            rows=[]
        )

        for log in reversed(logs):
            self.logs_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(log["timestamp"][:19])),
                        ft.DataCell(ft.Text(log["user"])),
                        ft.DataCell(ft.Text(log["action"])),
                    ]
                )
            )

        return ft.Column(
            [
                ft.Row([self.user_filter, self.search_field], spacing=20),
                ft.Divider(),
                ft.Row(
                    [ft.ElevatedButton(
                        "Очистить логи",
                        icon=ft.icons.CLEAR_ALL,
                        on_click=self.on_clear_logs
                    )],
                    alignment=ft.MainAxisAlignment.END
                ),
                ft.Column(
                    [ft.Container(self.logs_table, border=ft.border.all(1), border_radius=5)],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )
            ]
        )


class AddAppDialog:
    def __init__(self, on_save: Callable, on_pick_file: Callable):
        self.on_save = on_save
        self.on_pick_file = on_pick_file

    def build(self) -> ft.AlertDialog:
        self.name_field = ft.TextField(label="Название приложения")
        self.exe_path_field = ft.TextField(label="Путь к .exe файлу", read_only=True)

        return ft.AlertDialog(
            title=ft.Text("Добавить приложение"),
            content=ft.Column(
                [
                    self.name_field,
                    self.exe_path_field,
                    ft.ElevatedButton(
                        "Выбрать файл",
                        on_click=self.on_pick_file
                    )
                ],
                tight=True
            ),
            actions=[
                ft.TextButton("Отмена", on_click=self.close_dialog),
                ft.TextButton("Сохранить", on_click=self.on_save),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

    def close_dialog(self, e):
        self.dialog.open = False
        self.dialog.page.update()
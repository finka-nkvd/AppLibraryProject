import flet as ft
from model import UserModel, AppModel, LogModel
from controller import AppController


def main(page: ft.Page):
    # Инициализация моделей
    models = {
        "user": UserModel(),
        "app": AppModel(),
        "log": LogModel()
    }

    # Создание и запуск контроллера
    app = AppController(page, models)


ft.app(target=main)
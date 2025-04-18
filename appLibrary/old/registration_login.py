import customtkinter as ctk
from tkinter import messagebox, Canvas
import json
import hashlib

class App:
    def __init__(self):
        self.logged_in = False

    def hash_password(self, password):
        return hashlib.sha3_256(password.encode()).hexdigest()

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

        hashed_password = self.hash_password(password)

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

    def login_registration(self):
        self.reg = ctk.CTk()
        self.reg.title("Регистрация и вход")
        self.reg.geometry("315x220")
        self.reg.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        login_label = ctk.CTkLabel(self.reg, text="Логин:")
        login_label.place(x=15, y=40)
        password_label = ctk.CTkLabel(self.reg, text="Пароль:")
        password_label.place(x=15, y=120)

        self.login_entry = ctk.CTkEntry(self.reg)
        self.login_entry.place(x=90, y=40)

        self.password_entry = ctk.CTkEntry(self.reg)
        self.password_entry.place(x=90, y=120)

        reg_button = ctk.CTkButton(self.reg, text="Зарегистрироваться", command=self.register)
        reg_button.place(x=15, y=175)

        log_button = ctk.CTkButton(self.reg, text="Войти", command=self.login_user)
        log_button.place(x=160, y=175)

        self.reg.mainloop()

    def main_window(self):
        root = ctk.CTk()
        root.title("Customtkinter Centered Window")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        root.geometry(f"1920x1030-7-3")

        canvas = Canvas(root, width=1920, height=1030, bg='#242424', highlightthickness=0)
        canvas.pack()

        canvas.create_line(250, 0, 250, 1030, width=5, fill="black")
        canvas.create_line(0, 50, 1920, 50, width=5, fill="black")
        canvas.create_line(250, 400, 1920, 400, width=5, fill="black")

        login_label = ctk.CTkLabel(root, text=login)
        login_label.place(x=1800, y=5)

        root.mainloop()

    def run_app(self):
        self.login_registration()

app = App()
app.run_app()

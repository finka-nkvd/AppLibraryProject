import json
import hashlib
from pathlib import Path
from datetime import datetime
import shutil


class UserModel:
    def __init__(self):
        self.data_file = Path("data/data.json")
        self.users = self._load_data()
        self._create_admin()

    def _load_data(self):
        try:
            return json.loads(self.data_file.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save(self):
        self.data_file.parent.mkdir(exist_ok=True)
        self.data_file.write_text(json.dumps(self.users, indent=2))

    def _create_admin(self):
        if "admin" not in self.users:
            hashed_pw = hashlib.sha3_256("admin".encode()).hexdigest()
            self.users["admin"] = hashed_pw
            self.save()


class AppModel:
    def __init__(self):
        self.apps_dir = Path("apps")
        self.apps_dir.mkdir(exist_ok=True)
        self.data_file = Path("data/apps.json")
        self.apps = self._load_data()

    def _load_data(self):
        try:
            return json.loads(self.data_file.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save(self):
        self.data_file.parent.mkdir(exist_ok=True)
        self.data_file.write_text(json.dumps(self.apps, indent=2))

    def add_app(self, username, app_data):
        if username not in self.apps:
            self.apps[username] = []
        self.apps[username].append(app_data)
        self.save()

    def increment_launch_count(self, username, app_path):
        if username in self.apps:
            for app in self.apps[username]:
                if app["path"] == app_path:
                    app["launches"] = app.get("launches", 0) + 1
                    self.save()
                    break


class LogModel:
    def __init__(self):
        self.data_file = Path("data/logs.json")
        self.logs = self._load_data()

    def _load_data(self):
        try:
            return json.loads(self.data_file.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self):
        self.data_file.parent.mkdir(exist_ok=True)
        self.data_file.write_text(json.dumps(self.logs, indent=2))

    def add_log(self, action, username):
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "user": username,
            "action": action
        })
        self.save()

    def clear_logs(self):
        self.logs = []
        self.save()

    def get_filtered_logs(self, user_filter=None, search_query=None):
        filtered = self.logs.copy()

        if user_filter and user_filter != "Все":
            filtered = [log for log in filtered if log["user"] == user_filter]

        if search_query:
            search_query = search_query.lower()
            filtered = [log for log in filtered if search_query in log["action"].lower()]

        return filtered
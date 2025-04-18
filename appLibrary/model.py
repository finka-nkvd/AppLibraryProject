# model.py
import json
from pathlib import Path
from datetime import datetime

class UserModel:
    def __init__(self):
        self.data_file = Path("data.json")
        self.users = self._load_data()
        self._create_admin()

    def _load_data(self):
        try:
            return json.loads(self.data_file.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save(self):
        self.data_file.write_text(json.dumps(self.users, indent=2))

    def _create_admin(self):
        if "admin" not in self.users:
            hashed_pw = "e81b8cdc621fa3b492d5f09ad8e83a732b23c6579c31192efb1991bec711d8b8Й"
            self.users["admin"] = hashed_pw
            self.save()

class AppModel:
    def __init__(self):
        self.apps_dir = Path("apps")
        self.apps_dir.mkdir(exist_ok=True)
        self.data_file = Path("apps.json")
        self.apps = self._load_data()

    def _load_data(self):
        try:
            return json.loads(self.data_file.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save(self):
        self.data_file.write_text(json.dumps(self.apps, indent=2))

    def add_app(self, username, app_data):
        if username not in self.apps:
            self.apps[username] = []
        self.apps[username].append(app_data)
        self.save()

class LogModel:
    def __init__(self):
        self.data_file = Path("logs.json")
        self.logs = self._load_data()

    def _load_data(self):
        try:
            return json.loads(self.data_file.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self):
        self.data_file.write_text(json.dumps(self.logs, indent=2))

    def add_log(self, action, username):
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "user": username,
            "action": action
        })
        self.save()
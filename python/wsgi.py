from gunicorn.app.base import BaseApplication
from main import flask_api


class StandaloneApplication(BaseApplication):
    def __init__(self, api, options=None):
        self.options = options or {}
        self.application = api
        super().__init__()

    def load_config(self):
        config = {
            key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    StandaloneApplication(flask_api, {}).run()

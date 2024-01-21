from flask import Flask

from accounts.accounts_bp import accounts_bp
from common.app_factory import create
from configuration.manager import SQLAlchemyConfig
from users.users_bp import users_bp


blueprints = [users_bp, accounts_bp]
flask_api = create(blueprints, SQLAlchemyConfig)

# Serve API at port 1911
if __name__ == "__main__":
    flask_api.run(debug=False, host="0.0.0.0", port=1911)

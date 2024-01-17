from accounts.accounts_bp import accounts_bp
from users.users_bp import users_bp
from flask import Flask

flask_api = Flask(__name__)

# Register blueprint for context 'users'
flask_api.register_blueprint(users_bp)

# Register blueprint for context 'accounts'
flask_api.register_blueprint(accounts_bp)

# Serve API at port 1911
if __name__ == "__main__":
    flask_api.run(debug=False, host="0.0.0.0", port=1911)

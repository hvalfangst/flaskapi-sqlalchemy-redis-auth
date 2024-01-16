from flask import Flask
from python.route.users.module import register_user_routes

flask_api = Flask(__name__)

# Register routes for context 'users'
register_user_routes(flask_api)

# Serve API at port 1911
if __name__ == "__main__":
    flask_api.run(debug=False, host="0.0.0.0", port=1911)

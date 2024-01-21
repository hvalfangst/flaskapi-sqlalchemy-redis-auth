from common.app_factory import create
from configuration.manager import SQLAlchemyConfig

flask_api = create(SQLAlchemyConfig)

# Serve API at port 1911
if __name__ == "__main__":
    flask_api.run(debug=False, host="0.0.0.0", port=1911)

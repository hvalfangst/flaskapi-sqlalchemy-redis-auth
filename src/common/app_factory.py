from flask import Flask

from accounts.accounts_bp import accounts_bp
from users.users_bp import users_bp
from .db import db

# Define blueprints
blueprints = [users_bp, accounts_bp]


def create(config=None):
    """Construct the core application."""
    app = Flask("HVALFANGST", instance_relative_config=False)
    app.config.from_object(config)

    # Initialize Database Plugin
    db.init_app(app)

    # Register blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # Migrate database based on registered
    with app.app_context():
        db.create_all()
        return app

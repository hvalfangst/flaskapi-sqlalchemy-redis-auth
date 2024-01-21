from flask import Flask

from configuration.manager import SQLAlchemyConfig
from .db import db


def create(blueprints=None, config=None):
    """Construct the core application."""
    app = Flask("HVALFANGST", instance_relative_config=False)
    app.config.from_object(config)

    # Initialize Database Plugin
    db.init_app(app)

    # Register blueprints
    if blueprints:
        for blueprint in blueprints:
            app.register_blueprint(blueprint)

    # Migrate database based on registered
    with app.app_context():
        db.create_all()
        return app

from .handlers import create_user_handler, list_users_handler, \
    get_user_handler, delete_user_handler, login_user_handler, update_user_handler
from flask import Blueprint

users_bp = Blueprint("users", __name__, url_prefix="/users")

users_bp.add_url_rule("", methods=["POST"], view_func=create_user_handler)
users_bp.add_url_rule("/<email>", methods=["PUT"], view_func=update_user_handler)
users_bp.add_url_rule("", methods=["GET"], view_func=list_users_handler)
users_bp.add_url_rule("/<email>", methods=["GET"], view_func=get_user_handler)
users_bp.add_url_rule("/<email>", methods=["DELETE"], view_func=delete_user_handler)
users_bp.add_url_rule("/login", methods=["POST"], view_func=login_user_handler)

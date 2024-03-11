from .handlers import create_account_handler, update_account_handler, list_accounts_handler, \
    get_account_by_number_handler, delete_account_by_number_handler, delete_account_by_id_handler
from flask import Blueprint

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")

accounts_bp.add_url_rule("/", methods=["POST"], view_func=create_account_handler)
accounts_bp.add_url_rule("/<account_number>", methods=["PUT"], view_func=update_account_handler)
accounts_bp.add_url_rule("/", methods=["GET"], view_func=list_accounts_handler)
accounts_bp.add_url_rule("/<account_number>", methods=["GET"], view_func=get_account_by_number_handler)
accounts_bp.add_url_rule("/<account_id>", methods=["DELETE"], view_func=delete_account_by_id_handler)
accounts_bp.add_url_rule("/<account_number>", methods=["DELETE"], view_func=delete_account_by_number_handler)
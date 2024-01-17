import logging
import traceback

from .models import CreateAccountRequest, UpdateAccountRequest, Account
from .repository import AccountsRepository
from common import db_config, jwt_config, blacklist_cache
from common.models import AccessType
from common.security import authorize
import sys
from typing import List
from flask import request, jsonify
from pydantic import Field

# Configure the logging module
logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

# Create a logger for this module
logger = logging.getLogger(__name__)

# Initialize the AccountsRepository
db = AccountsRepository(config=db_config)


# Define the decorator for authorization
def auth_decorator(access_type):
    return authorize(cache=blacklist_cache, required_access=access_type, config=jwt_config)


@auth_decorator(AccessType.WRITE)
def create_account_handler():
    """
    Handle the creation of an account.

    Creates a new account with the provided data in the request.

    Returns:
        tuple: Tuple containing the JSON response and HTTP status code.
    """
    try:
        req = CreateAccountRequest(**request.get_json())
        db.create(request=req)
        return jsonify({"message": "Successfully created account."})
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Unauthorized"}), 401


@auth_decorator(AccessType.MODIFY)
def update_account_handler(account_number: str):
    """
    Handle the update of an account.

    Updates an existing account with the provided data in the request.

    Args:
        account_number (str): Account number to be updated.

    Returns:
        tuple: Tuple containing the JSON response and HTTP status code.
    """
    try:
        req = UpdateAccountRequest(**request.get_json())
        db.update(account_number=account_number, request=req)
        return jsonify({"message": "Successfully updated account."})
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Unauthorized"}), 401


@auth_decorator(AccessType.READ)
def list_accounts_handler():
    """
    Handle the listing of accounts.

    Lists all accounts present in the system.

    Returns:
        tuple: Tuple containing the JSON response and HTTP status code.
    """
    try:
        accounts: List[Account] = db.list()

        if not accounts:
            return jsonify({"error": f"No accounts present"}), 404

        accounts_dict = [account.to_dict() for account in accounts]
        return jsonify(accounts_dict)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Unauthorized"}), 401


@auth_decorator(AccessType.READ)
def get_account_by_number_handler(account_number: str):
    """
   Handle the retrieval of an account.

   Retrieves the account with the specified account number.

   Args:
       account_number (str): Account number to be retrieved.

   Returns:
       tuple: Tuple containing the JSON response and HTTP status code.
   """
    try:
        account: Account = db.get_by_number(account_number=account_number)

        if account is None:
            return jsonify({"error": f"No account found with account_number: {account_number}"}), 404

        return jsonify(account.to_dict())
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Unauthorized"}), 401


@auth_decorator(AccessType.DELETE)
def delete_account_by_id_handler(account_id: int):
    """
    Handle the deletion of an account by ID.

    Deletes the account with the specified ID.

    Args:
        account_id (int): ID of the account to be deleted.

    Returns:
        tuple: Tuple containing the JSON response and HTTP status code.
    """
    try:
        db.delete_by_id(account_id)
        return jsonify({"message": f"Successfully deleted account with id {account_id}."})
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Unauthorized"}), 401


@auth_decorator(AccessType.DELETE)
def delete_account_by_number_handler(account_number: str):
    """
    Handle the deletion of an account by account number.

    Deletes the account with the specified account number.

    Args:
        account_number (str): Account number to be deleted.

    Returns:
        tuple: Tuple containing the JSON response and HTTP status code.
    """
    try:
        db.delete_by_number(account_number)
        return jsonify({"message": f"Successfully deleted account with number {account_number}."})
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Unauthorized"}), 401

from sqlalchemy import text

# Create Account
CREATE_ACCOUNT_QUERY = text(
    """
    INSERT INTO accounts (user_id, account_number, balance)
    VALUES (:user_id, :account_number, :balance)
    """
)

# Update Account
UPDATE_ACCOUNT_QUERY = text(
    """
    UPDATE accounts
    SET balance = :balance
    WHERE account_number = :account_number
    """
)

# List Accounts
LIST_ACCOUNTS_QUERY = text(
    """
    SELECT * FROM accounts
    """
)


# Get Account by Account Number
GET_ACCOUNT_BY_ACCOUNT_NUMBER_QUERY = text(
    """
    SELECT * FROM accounts
    WHERE account_number = :account_number
    """
)

# Delete Account by Account ID
DELETE_ACCOUNT_BY_ACCOUNT_ID_QUERY = text(
    """
    DELETE FROM accounts
    WHERE account_id = :account_id
    """
)

# Delete Account by Account Number
DELETE_ACCOUNT_BY_ACCOUNT_NUMBER_QUERY = text(
    """
    DELETE FROM accounts
    WHERE account_number = :account_number
    """
)

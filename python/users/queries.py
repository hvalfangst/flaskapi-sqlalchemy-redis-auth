from sqlalchemy import text

# Create User
CREATE_USER_QUERY = text(
    """
    INSERT INTO users (first_name, last_name, phone_number, address, email, password, ssn, access)
    VALUES (:first_name, :last_name, :phone_number, :address, :email, :password, :ssn, :access)
    RETURNING user_id, first_name, last_name, phone_number, address, email, password, ssn, access
    """
)

# Update User
UPDATE_USER_QUERY = text(
    """
    UPDATE users
    SET phone_number = :phone_number, address = :address
    WHERE email = :email
    RETURNING user_id, first_name, last_name, phone_number, address, email, password, ssn, access
    """
)

# List Users
LIST_USERS_QUERY = text(
    """
    SELECT user_id, first_name, last_name, phone_number, address, email, password, ssn, access
    FROM users
    """
)

# Get User by Email
GET_USER_BY_EMAIL_QUERY = text(
    """
    SELECT user_id, first_name, last_name, phone_number, address, email, password, ssn, access
    FROM users
    WHERE email = :email
    """
)

# Delete User by Email
DELETE_USER_BY_EMAIL_QUERY = text(
    """
    DELETE FROM users
    WHERE email = :email
    RETURNING user_id, first_name, last_name, phone_number, address, email, password, ssn, access
    """
)

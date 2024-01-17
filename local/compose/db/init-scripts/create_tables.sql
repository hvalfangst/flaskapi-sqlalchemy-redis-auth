-- Create table for accounts
CREATE TABLE IF NOT EXISTS accounts (
                                             account_id SERIAL PRIMARY KEY,
                                             user_email VARCHAR(255) UNIQUE NOT NULL,
                                             account_number VARCHAR(12) UNIQUE NOT NULL,
                                             balance DECIMAL NOT NULL
);
-- PostgreSQL Script 
-- Ensure my_db is already created and connected

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash BYTEA NOT NULL,
    role_id INT DEFAULT 2,
    phone_number VARCHAR(20) UNIQUE,
    address_id INT,
    status VARCHAR(20) CHECK (status IN ('active', 'inactive', 'banned')) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- address table
CREATE TABLE IF NOT EXISTS address (
    address_id SERIAL PRIMARY KEY,
    line_1 VARCHAR(255) NOT NULL,
    line_2 VARCHAR(255) DEFAULT 'N/A',
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip VARCHAR(10) NOT NULL
);

-- Roles table
CREATE TABLE IF NOT EXISTS roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(30) UNIQUE NOT NULL
);

-- Permissions table
CREATE TABLE IF NOT EXISTS permissions (
    permission_id SERIAL PRIMARY KEY,
    role_id INT,
    permission_detail VARCHAR(100) UNIQUE NOT NULL
);

-- Initialize relationship
ALTER TABLE users
    ADD CONSTRAINT fk_user_role FOREIGN KEY (role_id) REFERENCES roles(role_id);

ALTER TABLE users
    ADD CONSTRAINT fk_user_address FOREIGN KEY (address_id) REFERENCES address(address_id);

ALTER TABLE permissions
    ADD CONSTRAINT fk_permission_role FOREIGN KEY (role_id) REFERENCES roles(role_id);

-- Initialize roles after roles table creation
INSERT INTO roles (role_name) 
VALUES 
    ('admin'),
    ('basicuser');
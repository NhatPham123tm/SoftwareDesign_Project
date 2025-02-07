INSERT INTO users (name, email, password_hash, role_id, phone_number, address)
VALUES
('John Doe', 'john.doe@example.com', '\x8e4e070cbe470cd7c2267052b59d5e8f8c8586eac99ee24e2e1658f6b42419c1', 1, '123-456-7890', '123 Main St, Anytown, USA'),
('Jane Smith', 'jane.smith@example.com', '\x3c3c0d92a0d24145fd45568f80fba4b775c1d7c871bb3e2c1b244be8f8ee3c9d', 2, '987-654-3210', '456 Oak St, Othercity, USA');

Select * From users;

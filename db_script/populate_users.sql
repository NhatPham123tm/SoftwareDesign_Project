-- Sample data for api_roles
INSERT INTO api_roles (id, role_name) 
VALUES 
    (1, 'admin'),
    (2, 'basicuser');

-- Sample data for api_address
INSERT INTO api_address (line_1, line_2, city, state, zip_code)
VALUES 
    ('123 Main St', 'Apt 101', 'Springfield', 'IL', '62701'),
    ('456 Oak Rd', 'N/A', 'Shelbyville', 'IL', '62565'),
    ('789 Pine Ln', 'Suite 200', 'Capital City', 'IL', '62702');

-- Sample data for users
INSERT INTO api_user_accs (name, email, password_hash, role_id, phone_number, address_id, status, created_at)
VALUES 
    ('John Doe', 'john.doe@example.com', '\\x5f4dcc3b5aa765d61d8327deb882cf99', 1, '111-555-1234', 1, 'active', NOW()),
    ('Jane Smith', 'jane.smith@example.com', '\\x5f4dcc3b5aa765d61d8327deb882cf99', 2, '111-555-5678', 2, 'inactive', NOW()),
    ('Alice Johnson', 'alice.johnson@example.com', '\\x5f4dcc3b5aa765d61d8327deb882cf99', 2, '111-555-8765', 3, 'banned', NOW());

-- Sample data for permissions
INSERT INTO api_permission (role_id, permission_detail)
VALUES
    (1, 'access_admin_dashboard'),
    (1, 'manage_users'),
    (2, 'view_content'),
    (2, 'comment_on_posts');

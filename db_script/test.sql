-- test dummy delete
DELETE FROM users
WHERE email IN ('john.doe@example.com', 'jane.smith@example.com');
Select * From users;
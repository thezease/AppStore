-- Get all users
SELECT * FROM users ORDER BY first_name;

-- Get details of a selected user
SELECT email, first_name, last_name, date_of_birth, since, 
       country, credit_card_type, credit_card_no
FROM users WHERE email = '';

-- Check if user exists
SELECT 1
FROM users
WHERE email = '';

--TODO: transfer queries here


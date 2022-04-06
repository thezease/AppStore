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

-- Check if there is duplicate credit card number in database
SELECT *
FROM users
WHERE credit_card_no = '';

-- Call stored procedure to insert a new user
CALL insert_users('', '', '', '', '', '', '', '');

-- Authenticate user by checking email and password in database
SELECT (password = '')
FROM users
WHERE email = '';

-- Call stored procedure to update a user
CALL update_users('', '', '', '', '', '', '')

-- Call user-defined function to select all fields for a selected apartment
SELECT * FROM get_selected_apt('')

-- Get list of bookings that a user has made
SELECT  tb.tempbooking_id, apt.country, apt.city, tb.check_in, tb.check_out, 
              apt.price * (tb.check_out - tb.check_in + 1) AS total_price
FROM tempbookings tb NATURAL JOIN apartments apt
WHERE tb.guest = ''
AND apt.listed = TRUE
ORDER BY tb.check_in ASC;

-- Get list of rentals user the user's name
-- An approved booking is also considered a rental
SELECT * FROM selected_rental('');

-- Update the ratings for a rental that user has went for
UPDATE rentals
SET rating = ''
WHERE rental_id = '';

-- User to delete a booking he has made
DELETE FROM tempbookings
WHERE tempbooking_id = '';

-- User to make a new booking
INSERT INTO tempbookings (
apartment_id,
check_in,
check_out,
guest
)
VALUES ('', '', '', '');



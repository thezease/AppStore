-- Function to select list of rentals that a user had rented
CREATE OR REPLACE FUNCTION selected_rental(x VARCHAR)  
	RETURNS TABLE( 
    	rental_id int,  
		country VARCHAR(16),  
		city VARCHAR(32), 
		check_in DATE, 
		check_out DATE, 
		total_price DECIMAL(8,2), 
		rating INT
	) 
LANGUAGE SQL
AS $$ 
    SELECT r.rental_id, apt.country, apt.city,
		   r.check_in, r.check_out, 
		   apt.price * (r.check_out - r.check_in + 1) AS total_price,
		   r.rating
 	FROM apartments apt NATURAL JOIN rentals r
 	WHERE r.guest = x
	AND apt.listed = true
    ORDER BY r.check_out DESC;
$$; 
 

-- Function to insert new user
CREATE OR REPLACE PROCEDURE insert_users(
	f_name VARCHAR(16),
	l_name VARCHAR(16),
	e_mail VARCHAR(64),
	pass VARCHAR(32),
	dob DATE,
	count_ry VARCHAR(32),
	cred_card_type VARCHAR(16),
	cred_card_no BIGINT
) 
LANGUAGE SQl
AS
$$
    INSERT INTO users 
	(first_name, last_name, email, password, date_of_birth, country, credit_card_type, credit_card_no) 
	VALUES (f_name, l_name, e_mail, pass, dob, count_ry, cred_card_type, cred_card_no );
$$;
  

-- Procedure to update user details
CREATE OR REPLACE PROCEDURE update_users(
	f_name VARCHAR(16),
	l_name VARCHAR(16),
	dob DATE,
	count_ry VARCHAR(32),
	cred_card_type VARCHAR(16),
	cred_card_no BIGINT,
	e_mail VARCHAR(64)
) 
LANGUAGE SQL
AS
$$
    UPDATE users SET 
    first_name = f_name, 
    last_name = l_name, 
    date_of_birth = dob, 
    country = count_ry, 
    credit_card_type = cred_card_type, 
    credit_card_no = cred_card_no
    WHERE email = e_mail;
$$;


-- Function to get list of apartments filtered by country, city, and number of guests
CREATE OR REPLACE FUNCTION get_apartment(i VARCHAR, j VARCHAR, k INT)  
	RETURNS TABLE( 
    	apartment_id INT,  
		host VARCHAR(64), 
 		country VARCHAR(16),  
 		city VARCHAR(32), 
 		address VARCHAR(64), 
 		num_guests INT, 
 		num_beds INT, 
 		num_bathrooms INT, 
 		property_type VARCHAR(64), 
 		amenities VARCHAR(64), 
 		house_rules VARCHAR(64), 
 		price NUMERIC,
		listed BOOL,
 		avg_rating DECIMAL(2,1)
 		) 
LANGUAGE SQL
AS $$ 
    SELECT  apt.apartment_id,  
		apt.host, 
		apt.country,  
		apt.city, 
		apt.address, 
		apt.num_guests, 
		apt.num_beds, 
		apt.num_bathrooms, 
		apt.property_type, 
		apt.amenities , 
		apt.house_rules, 
		apt.price, 
		apt.listed,
		COALESCE(rts.avg_rating, -1) AS avg_rating
	FROM apartments apt LEFT JOIN overall_ratings rts
	ON apt.apartment_id = rts.apartment_id
	WHERE listed = true
	AND apt.country = i
	AND apt.city = j
	AND apt.num_guests >= k
	ORDER BY apt.price;
$$; 


-- function to get list of all apartments
CREATE OR REPLACE FUNCTION get_all_apartments()  
	RETURNS TABLE( 
		apartment_id INT,  
		host VARCHAR(64), 
		country VARCHAR(16),  
		city VARCHAR(32), 
		address VARCHAR(64), 
		num_guests INT, 
		num_beds INT, 
		num_bathrooms INT, 
		property_type VARCHAR(64), 
		amenities VARCHAR(64), 
		house_rules VARCHAR(64), 
		price NUMERIC, 
		listed BOOL,
		avg_rating DECIMAL(2,1)
 	) 
LANGUAGE SQL
AS $$ 
	SELECT  apt.apartment_id,  
		apt.host, 
		apt.country,  
		apt.city, 
		apt.address, 
		apt.num_guests, 
		apt.num_beds, 
		apt.num_bathrooms, 
		apt.property_type, 
		apt.amenities , 
		apt.house_rules, 
		apt.price, 
		apt.listed,
		COALESCE(rts.avg_rating, -1) AS avg_rating
	FROM apartments apt LEFT JOIN overall_ratings rts
	ON apt.apartment_id = rts.apartment_id
	WHERE listed = true
	ORDER BY apt.price;
$$; 


-- Function to get details of a selected apartment
CREATE OR REPLACE FUNCTION get_selected_apt(apt_id INT)  
	RETURNS TABLE( 
    	apartment_id INT,  
		host VARCHAR(64), 
		country VARCHAR(16),  
		city VARCHAR(32), 
		address VARCHAR(64), 
		num_guests INT, 
		num_beds INT, 
		num_bathrooms INT, 
		property_type VARCHAR(64), 
		amenities VARCHAR(64), 
		house_rules VARCHAR(64), 
		price NUMERIC, 
		listed BOOL,
		avg_rating DECIMAL(2,1)
 	) 
LANGUAGE SQL
AS $$ 
    SELECT *  
 	FROM apartments apt NATURAL JOIN overall_ratings rts 
 	WHERE apt_id=apartment_id;
	
	SELECT  apt.apartment_id,  
		apt.host, 
		apt.country,  
		apt.city, 
		apt.address, 
		apt.num_guests, 
		apt.num_beds, 
		apt.num_bathrooms, 
		apt.property_type, 
		apt.amenities , 
		apt.house_rules, 
		apt.price, 
		apt.listed,
		COALESCE(rts.avg_rating, -1) AS avg_rating
	FROM apartments apt LEFT JOIN overall_ratings rts
	ON apt.apartment_id = rts.apartment_id
	WHERE apt_id=apt.apartment_id;
$$; 



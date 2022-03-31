-- Function to select list of rentals that a user had rented
CREATE OR REPLACE FUNCTION selected_rental(x varchar)  
	RETURNS TABLE( 
    	apartment_id int,  
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
		price DECIMAL(8,2), 
		rental_id int, 
		check_in VARCHAR(64), 
		check_out VARCHAR(64), 
		guest VARCHAR(64), 
		total_price DECIMAL(8,2), 
		rating INT
	) 
LANGUAGE SQL
AS $$ 
    SELECT *  
 	FROM apartments ap NATURAL JOIN rentals r
 	WHERE x = r.guest; 
$$; 
 

-- Function to insert new user
CREATE OR REPLACE Procedure insert_users(
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
	cred_card_no bigint,
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
CREATE OR REPLACE FUNCTION get_apartment(i varchar, j varchar, k int)  
	RETURNS TABLE( 
    	apartment_id int,  
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
 		price Varchar(64), 
 		avg_rating Decimal(2,1)
 		) 
LANGUAGE SQL
AS $$ 
    SELECT *  
 	FROM apartments apt natural join overall_ratings rts 
 	WHERE apt.country = i
	AND apt.city = j
	AND apt.num_guests >= k
	ORDER BY apt.price;
$$; 


-- function to get list of all apartments
CREATE OR REPLACE FUNCTION get_all_apartments()  
	RETURNS TABLE( 
		apartment_id int,  
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
		price Varchar(64), 
		avg_rating Decimal(2,1)
 	) 
LANGUAGE SQL
AS $$ 
    SELECT *  
 	FROM apartments apt natural join overall_ratings rts 
 	WHERE apt.apartment_id = rts.apartment_id 
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
		price VARCHAR(64), 
		avg_rating DECIMAL(2,1)
 	) 
LANGUAGE SQL
AS $$ 
    SELECT *  
 	FROM apartments apt NATURAL JOIN overall_ratings rts 
 	WHERE apt_id=apartment_id; 
$$; 



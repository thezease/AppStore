SELECT *
FROM rentals;
SELECT *
FROM users;
SELECT *
FROM apartments order by apartment_id;
-- create new user, new rental and new apartment
insert into users (first_name, last_name, email, password, date_of_birth, country, credit_card_type, credit_card_no) values ('Filide', 'O''Dreain', 'fodreain0@hibu.com', 'uvbgOqQuZuAz0', '1983-02-15', 'Brazil', 'visa', 4743679680836);
insert into rentals (apartment_id, check_in, check_out, guest, total_price, rating) values (43, '2023-01-26', '2023-01-27', 'acullin2d@oakley.com', 362.97, 5);
insert into apartments (host, country, city, address, num_guests, num_beds, num_bathrooms, property_type, amenities, house_rules, price) values ('bbelford1r@dedecms.com', 'China', 'Qingzhou', '4113 Fordem Trail', 10, 11, 4, 'Apartment', 'Free Wifi/Parking/Washing Machine and Dryer', 'No Smoking', 279);

-- update entries
-- table rentals
-- from html, state what field to be updated and updated value
-- copy the original values for the fields that are not needed to be updated 
UPDATE rentals
SET apartment_id = '', check_in = '', check_out = '', guest = '', total_price = '', rating = ''
WHERE rental_id = '';

UPDATE apartments
SET host = '', country = '',city = '',address = '',num_guests = '',num_beds = '',num_bathrooms = '',property_type = '',amenities = '', house_rules = '', price = ''
WHERE apartment_id = '';

-- only since cannot be amended
UPDATE users
SET first_name = '', last_name = '', date_of_brith = '', country = '', credit_card_type = '', credit_card_no = ''
WHERE email = '';

-- delete entries
DELETE FROM users
WHERE email = '';

DELETE FROM apartments
WHERE apartment_id = '';

DELETE FROM rentals
WHERE rental_id = '';

-- statistics display

-- -- rentals statistics
-- total income of all rentals
SELECT SUM(total_price)
FROM rentals;

-- the total income in each city of each country
SELECT a.country, a.city, ROUND(SUM(r.total_price),2)
FROM rentals r, apartments a
WHERE r.apartment_id = a.apartment_id
GROUP BY a.country, a.city
ORDER BY ROUND(SUM(r.total_price),2) DESC;

-- the total income in each country
SELECT a.country, ROUND(SUM(r.total_price),2)
FROM rentals r, apartments a
WHERE r.apartment_id = a.apartment_id
GROUP BY a.country
ORDER BY ROUND(SUM(r.total_price),2) DESC;

-- the rating rank of apartment
SELECT a.country, a.city, a.address, a.apartment_id, ROUND(AVG(r.rating),1)
FROM rentals r, apartments a
WHERE r.apartment_id = a.apartment_id
GROUP BY a.country, a.city, a.apartment_id
ORDER BY ROUND(AVG(r.rating),1) DESC;

SELECT a.apartment_id, ROUND(AVG(r.rating),1)
FROM rentals r, apartments a
WHERE r.apartment_id = a.apartment_id
GROUP BY a.country, a.city, a.apartment_id
ORDER BY ROUND(AVG(r.rating),1) DESC
LIMIT 3;

-- the top 3 best rating of apartment in each city of each country
SELECT * FROM (
    SELECT a.country, 
	a.apartment_id,
	ROUND(AVG(r.rating),1) AS average_rating,
	ROW_NUMBER() over (PARTITION BY a.country ORDER BY ROUND(AVG(r.rating),1) DESC) AS country_rank 
	FROM rentals r, apartments a
	WHERE r.apartment_id = a.apartment_id
	GROUP BY a.country, a.apartment_id
) ranks
WHERE country_rank <= 3;

-- the best rating of apartment
SELECT a.country, a.apartment_id, ROUND(AVG(r.rating),1)
FROM rentals r, apartments a
WHERE r.apartment_id = a.apartment_id
GROUP BY a.country, a.apartment_id
HAVING ROUND(AVG(r.rating),1) >= ALL(
	SELECT ROUND(AVG(r2.rating),1)
	FROM rentals r2, apartments a2
	WHERE r2.apartment_id = a2.apartment_id
	GROUP BY a2.country, a2.apartment_id
);

-- average length of stay for all rentals of each apartment DESC
SELECT a.country, a.city, a.address, a.apartment_id, ROUND(AVG(r.check_out-r.check_in),1) AS average_length_of_stay
FROM rentals r, apartments a
WHERE r.apartment_id = a.apartment_id
GROUP BY a.country, a.city, a.apartment_id
ORDER BY average_length_of_stay DESC;

-- sum of length of stay for all rentals of each apartment DESC
SELECT a.country, a.city, a.address, a.apartment_id, SUM(r.check_out-r.check_in) AS total_length_of_stay
FROM rentals r, apartments a
WHERE r.apartment_id = a.apartment_id
GROUP BY a.country, a.city, a.apartment_id
ORDER BY total_length_of_stay DESC;


-- -- apartments statistics
-- number of available apartments for each property type in each country DESC
SELECT country, property_type, COUNT(*) AS number_of_available_apartments
FROM apartments
GROUP BY country, property_type
ORDER BY number_of_available_apartments DESC;

-- average rental price per day in each city/country DESC
SELECT country, city, ROUND(AVG(price),2) AS average_price
FROM apartments
GROUP BY country, city
ORDER BY average_price DESC;

SELECT country, ROUND(AVG(price),2) AS average_price
FROM apartments
GROUP BY country
ORDER BY average_price DESC;

-- total number of apartments in each city/country DESC
SELECT country, city, COUNT(*) AS total_number_of_apartments
FROM apartments
GROUP BY country, city
ORDER BY total_number_of_apartments DESC;

SELECT country, COUNT(*) AS total_number_of_apartments
FROM apartments
GROUP BY country
ORDER BY total_number_of_apartments DESC;

-- total number of apartments that disallow smoking/pets in each country DESC
SELECT country, COUNT(*) AS total_number_of_apartments
FROM apartments
WHERE house_rules SIMILAR TO '%No Smoking%'
GROUP BY country
ORDER BY total_number_of_apartments DESC;

SELECT country, COUNT(*) AS total_number_of_apartments
FROM apartments
WHERE house_rules SIMILAR TO '%No Pets%'
GROUP BY country
ORDER BY total_number_of_apartments DESC;

SELECT country, COUNT(*) AS total_number_of_apartments
FROM apartments
WHERE house_rules SIMILAR TO '%No Pets%'
AND house_rules SIMILAR TO '%No Smoking%'
GROUP BY country
ORDER BY total_number_of_apartments DESC;

-- -- users statitics
-- number of registered users
SELECT COUNT(*) FROM users;

-- total number of credit cards for each credit card type grouped and patitioned by countries
SELECT country, credit_card_type, COUNT(*),
ROW_NUMBER() OVER (PARTITION BY country ORDER BY COUNT(*) DESC) AS rank
FROM users
GROUP BY country, credit_card_type;

-- number of users who registered an account in the past one month
SELECT COUNT(*)
FROM users
WHERE since >= (CURRENT_DATE - 30);

-- -- mixed tables statistics
-- for each country of apartments, count the number of guests grouped by aparment country and guest nationality
SELECT a.country AS apartment_country, u.country AS guest_nationality, COUNT(*) AS number_of_guests,
ROW_NUMBER() OVER (PARTITION BY a.country ORDER BY COUNT(*) DESC) AS rank
FROM apartments a, rentals r, users u
WHERE a.apartment_id = r.apartment_id
AND r.guest = u.email
GROUP BY apartment_country, guest_nationality;

-- the total income of each aparment country grouped by guest nationality
SELECT a.country AS apartment_country, u.country AS guest_nationality, ROUND(SUM(r.total_price), 2) AS income,
ROW_NUMBER() OVER (PARTITION BY a.country ORDER BY ROUND(SUM(r.total_price), 2) DESC) AS rank
FROM apartments a, rentals r, users u
WHERE a.apartment_id = r.apartment_id
AND r.guest = u.email
GROUP BY apartment_country, guest_nationality;

-- continued: to select one specific country
SELECT ranks.guest_nationality, ranks.income, ranks.rank
FROM (
	SELECT a.country AS apartment_country, u.country AS guest_nationality, ROUND(SUM(r.total_price), 2) AS income,
	ROW_NUMBER() OVER (PARTITION BY a.country ORDER BY ROUND(SUM(r.total_price), 2) DESC) AS rank
	FROM apartments a, rentals r, users u
	WHERE a.apartment_id = r.apartment_id
	AND r.guest = u.email
	GROUP BY apartment_country, guest_nationality
) AS ranks
WHERE ranks.apartment_country = 'China';

-- the total values of transaction for each credict card type and each guest nationality
SELECT u.country AS guest_nationality, u.credit_card_type, ROUND(SUM(r.total_price), 2),
ROW_NUMBER() OVER (PARTITION BY u.country ORDER BY ROUND(SUM(r.total_price), 2) DESC) AS rank
FROM users u , rentals r
WHERE u.email = r.guest
GROUP BY guest_nationality, u.credit_card_type;





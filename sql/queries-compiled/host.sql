-- Get all apartments that a host owns
-- also shows averaging rating across all associated rentals,
-- and total earning from finished rentals under each apartment
SELECT 
    apt.apartment_id,
    apt.country, 
    apt.city, 
    apt.address, 
    apt.num_guests, 
    apt.num_beds,
    apt.num_bathrooms,
    apt.property_type,
    apt.amenities,
    apt.house_rules,
    apt.price,
    apt.listed,
    COALESCE(rts.avg_rating, -1) AS avg_rating,
    COALESCE(earning.earning, 0) AS earning
FROM 
apartments apt
LEFT JOIN overall_ratings rts
ON apt.apartment_id = rts.apartment_id
LEFT JOIN (
    SELECT apartment_id,  SUM(tp.stay_price) AS earning
    FROM (
        SELECT apartment_id, apt.price * (r.check_out - r.check_in + 1) AS stay_price
        FROM rentals r NATURAL JOIN apartments apt
        WHERE r.check_out < CURRENT_DATE
    ) AS tp
    GROUP BY apartment_id
) AS earning
ON apt.apartment_id = earning.apartment_id
WHERE host = ''
ORDER BY apt.apartment_id ASC;

-- Get all tempbookings that are associated with apartments that the host owns
SELECT  apt.country, apt.city, apt.address, tb.check_in, tb.check_out, 
        apt.price * (tb.check_out - tb.check_in + 1) AS total_price,
        tb.tempbooking_id, apt.apartment_id
FROM tempbookings tb NATURAL JOIN apartments apt
WHERE host = ''
ORDER BY tb.check_in ASC;

-- Get all upcoming rentals that are associated with apartments that the host owns
SELECT  apt.country, apt.city, apt.address, r.check_in, r.check_out, 
        apt.price * (r.check_out - r.check_in + 1) AS total_price,
        apt.apartment_id
FROM rentals r NATURAL JOIN apartments apt
WHERE host = ''
AND r.check_in > CURRENT_DATE
ORDER BY r.check_in ASC;

-- Get all past rentals that are associated with apartments that the host owns
SELECT  apt.country, apt.city, apt.address, r.check_in, r.check_out, 
        apt.price * (r.check_out - r.check_in + 1) AS total_price,
        COALESCE(r.rating, -1) AS rating, apt.apartment_id
FROM rentals r NATURAL JOIN apartments apt
WHERE host = ''
AND r.check_out < CURRENT_DATE
ORDER BY r.check_in ASC;

-- Insert a new apartment
INSERT INTO apartments (
    host,
    country,
    city,
    address,
    num_guests,
    num_beds,
    num_bathrooms,
    property_type,
    amenities,
    house_rules,
    price
) VALUES (
    '', '', '', '', '',
    '', '', '', '', '',
    ''
);

-- Update apartment details
UPDATE apartments
SET 
    country = '',
    city = '',
    address = '',
    num_guests = '',
    num_beds = '',
    num_bathrooms = '',
    property_type = '',
    amenities = '',
    house_rules = '',
    price = ''
WHERE apartment_id = '';

-- List or unlist an apartment
UPDATE apartments
SET listed = (NOT listed)
WHERE apartment_id = '';

-- Approve a tempbooking by updating its 'status' column
-- An AFTER UPDATE trigger will then call a function
-- to migrate this tempbooking entry into rentals table
UPDATE tempbookings
SET status = CAST(1 AS BIT)
WHERE tempbooking_id = '';


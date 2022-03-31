-- helper function
-- check if a given date overlaps with any interval (check_in, check_out) from any entry in tempbookings
-- TRUE if the given date has no overlap with existing entries for a given apt
-- Use case: to display all the days available from given month and year
CREATE OR REPLACE FUNCTION check_single_date(apt INT, curr_date VARCHAR)
RETURNS BOOL AS
$$
DECLARE booking RECORD;

BEGIN
	FOR booking IN 
		SELECT *
		FROM tempbookings
		WHERE apartment_id = apt
	LOOP
		IF (booking.check_in, booking.check_out) OVERLAPS (CAST(curr_date AS DATE), CAST(curr_date AS DATE))
		THEN RETURN FALSE;
		END IF;
	END LOOP;
	RETURN TRUE;
END;
$$ LANGUAGE plpgsql;


-- helper function
-- check if given interval (s_date, e_date) overlaps with interval (check_in, check_out) from any entry in tempbookings
-- TRUE if there is any overlap with existing entries for a given apt
-- Use case: check if new booking clashes with existing booking
CREATE OR REPLACE FUNCTION is_there_overlap(apt INT, s_date DATE, e_date DATE)
RETURNS BOOL AS
$$
DECLARE rental RECORD;

BEGIN
	FOR rental IN 
		SELECT *
		FROM rentals
		WHERE apartment_id = apt
	LOOP
		IF (
			(rental.check_in, rental.check_out)
			OVERLAPS
			(CAST(s_date AS DATE), CAST(e_date AS DATE))
		)
		THEN RETURN TRUE;
		END IF;
	END LOOP;
	RETURN FALSE;
END;
$$ LANGUAGE plpgsql;
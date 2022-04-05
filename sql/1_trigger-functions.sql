--
CREATE OR REPLACE FUNCTION checkoverlap() RETURNS TRIGGER AS
$$
DECLARE 
  f record;
BEGIN
  FOR f IN
    SELECT *
	FROM rentals
	WHERE apartment_id = new.apartment_id
  LOOP
    IF (new.check_in , new.check_out) OVERLAPS (f.check_in, f.check_out)
	THEN
    RAISE EXCEPTION 'prior booking present :' ;
	END IF;
  END LOOP;
  RETURN NEW;
END;
$$
LANGUAGE plpgsql;

--
CREATE TRIGGER overlap
BEFORE INSERT on rentals
FOR EACH ROW
EXECUTE FUNCTION checkoverlap();


-- 
CREATE OR REPLACE FUNCTION add_to_rentals() RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO
       rentals
        VALUES(default, old.apartment_id, old.check_in, old.check_out, old.guest);
		DELETE FROM tempbookings
		WHERE tempbooking_id = old.tempbooking_id;
		RETURN NEW;
END;
$$
language plpgsql;

-- 
CREATE TRIGGER rental
AFTER UPDATE of status ON tempbookings
FOR EACH ROW
EXECUTE FUNCTION add_to_rentals();


--
CREATE OR REPLACE FUNCTION checkdate() RETURNS TRIGGER AS
$$
BEGIN
  IF old.check_out > CURRENT_DATE 
  THEN
    RAISE EXCEPTION 'unable to rate before staying';
	END IF;
	CREATE VIEW overall_ratings AS
        SELECT ap.apartment_id, CAST(AVG(r.rating) AS DECIMAL(2, 1)) AS avg_rating
        FROM apartments ap, rentals r
        WHERE ap.apartment_id = r.apartment_id
        GROUP BY ap.apartment_id;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

--
CREATE TRIGGER rating
AFTER UPDATE of rating ON rentals
FOR EACH ROW
EXECUTE FUNCTION checkdate();

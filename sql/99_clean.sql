/*******************

  Cleaning script

*******************/

-- Clear all tables and views
-- Also clears triggers that depend on those tables
DROP VIEW IF EXISTS overall_ratings;
DROP TABLE IF EXISTS tempbookings CASCADE;
DROP TABLE IF EXISTS rentals CASCADE;
DROP TABLE IF EXISTS apartments CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Clear all functions
DROP FUNCTION IF EXISTS checkdate;
DROP FUNCTION IF EXISTS checkoverlap;
DROP FUNCTION IF EXISTS rentals;

DROP FUNCTION IF EXISTS get_all_apartments;
DROP FUNCTION IF EXISTS get_apartment;
DROP FUNCTION IF EXISTS get_selected_apt;
DROP FUNCTION IF EXISTS selected_rental;

DROP PROCEDURE IF EXISTS insert_users;
DROP PROCEDURE IF EXISTS update_users;
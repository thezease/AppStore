/*******************

  Cleaning script

*******************/

-- Clear all tables and views
-- Also clears triggers, procedures and functions that depend on those tables
DROP VIEW IF EXISTS overall_ratings;
DROP TABLE IF EXISTS rentals CASCADE;
DROP TABLE IF EXISTS apartments CASCADE;
DROP TABLE IF EXISTS users CASCADE;
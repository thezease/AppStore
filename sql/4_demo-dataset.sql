-- to insert a series of cherry-picked entries to showcase app functionalities

insert into users (first_name, last_name, email, password, date_of_birth, since , country, credit_card_type, credit_card_no) values ('Esteban', 'Propper', 'epropper0@baidu.com', 'cJ7OOorOn', '1970-04-02', '2012-05-30', 'United States', 'americanexpress', '6759419933254742');
insert into users (first_name, last_name, email, password, date_of_birth, since , country, credit_card_type, credit_card_no) values ('Iris', 'Obert', 'iobert1@opera.com', 'wMuZDe3NL', '1980-02-21', '2014-06-13', 'United States', 'visa', '3537782618790306');
insert into users (first_name, last_name, email, password, date_of_birth, since , country, credit_card_type, credit_card_no) values ('Hercules', 'Cantu', 'hcantu2@goo.gl', 'kEfLQkO0N', '1995-04-11', '2004-07-30', 'United States', 'mastercard', '3583897205521501');
insert into users (first_name, last_name, email, password, date_of_birth, since , country, credit_card_type, credit_card_no) values ('Janina', 'Gammill', 'jgammill3@paginegialle.it', '3Ia0SkfLq', '1995-05-24', '2016-08-29', 'United States', 'visa', '3562115964704555');
insert into users (first_name, last_name, email, password, date_of_birth, since , country, credit_card_type, credit_card_no) values ('Pepi', 'Perrigo', 'pperrigo4@wordpress.com', '3Dv6FcNN5', '1977-02-03', '2012-05-28', 'United States', 'mastercard', '3551489434445831');
insert into users (first_name, last_name, email, password, date_of_birth, since , country, credit_card_type, credit_card_no) values ('Sebastiano', 'Tulk', 'stulk5@dailymotion.com', 'l1t1HzSRd', '1985-02-25', '2007-03-18', 'United States', 'visa', '4175000769143893');
insert into users (first_name, last_name, email, password, date_of_birth, since , country, credit_card_type, credit_card_no) values ('Amalee', 'Grelak', 'agrelak6@jimdo.com', 'hAdPLtf8z', '1986-11-29', '2005-08-14', 'Malaysia', 'americanexpress', '5602258917585858');
insert into users (first_name, last_name, email, password, date_of_birth, since , country, credit_card_type, credit_card_no) values ('Jeni', 'Slesser', 'jslesser7@state.gov', 'eNg4Ahs1s', '1980-06-17', '2006-01-06', 'United States', 'visa', '3545822325600396');
insert into users (first_name, last_name, email, password, date_of_birth, since , country, credit_card_type, credit_card_no) values ('Jeromy', 'Hardison', 'jhardison8@va.gov', '8Qt9RwQle', '1999-08-28', '2008-01-11', 'United States', 'visa', '3534022506059347');
insert into users (first_name, last_name, email, password, date_of_birth, since , country, credit_card_type, credit_card_no) values ('Clemens', 'Liversedge', 'cliversedge9@ed.gov', 'm6w6Ll9Uq', '1979-06-21', '2006-03-25', 'United States', 'mastercard', '5048379516651461');

insert into apartments (host, country, city, address, num_guests, num_beds, num_bathrooms, property_type, amenities, house_rules, price) values ('cliversedge9@ed.gov', 'China', 'Haiyan', '18 Prairie Rose Avenue', 3, 3, 5, 'Bungalow', 'Free Wifi/Parking/Washing Machine and Dryer', 'No Smoking/No Pets', 213);
insert into apartments (host, country, city, address, num_guests, num_beds, num_bathrooms, property_type, amenities, house_rules, price) values ('jhardison8@va.gov', 'China', 'Heshan', '782 Judy Circle', 5, 6, 3, 'Luxury Apartment', 'Free Wifi/Washing Machine and Dryer', 'No Smoking', 275);
insert into apartments (host, country, city, address, num_guests, num_beds, num_bathrooms, property_type, amenities, house_rules, price) values ('agrelak6@jimdo.com', 'France', 'Thiers', '12 Farwell Hill', 6, 7, 2, 'Luxury Apartment', 'Free Wifi/Parking/Gym/Pool/Washing Machine and Dryer', 'No Smoking/No Pets', 629);
insert into apartments (host, country, city, address, num_guests, num_beds, num_bathrooms, property_type, amenities, house_rules, price) values ('jslesser7@state.gov', 'China', 'Aimin', '188 Hoffman Road', 7, 8, 1, 'Luxury Apartment', 'Free Wifi/Washing Machine and Dryer', 'No Smoking/No Pets', 141);
insert into apartments (host, country, city, address, num_guests, num_beds, num_bathrooms, property_type, amenities, house_rules, price) values ('stulk5@dailymotion.com', 'China', 'Jinjiang', '545 Judy Lane', 9, 9, 1, 'Apartment', 'Free Wifi/Parking/Washing Machine and Dryer', 'No Pets', 270);

insert into rentals (apartment_id, check_in, check_out, guest,  rating) values (1, '2012-09-12', '2012-09-14', 'pperrigo4@wordpress.com',  4);
insert into rentals (apartment_id, check_in, check_out, guest,  rating) values (2, '2017-08-26', '2017-09-06', 'jgammill3@paginegialle.it',  3);
insert into rentals (apartment_id, check_in, check_out, guest,  rating) values (3, '2021-05-19', '2021-05-22', 'pperrigo4@wordpress.com',  4);
insert into rentals (apartment_id, check_in, check_out, guest,  rating) values (4, '2018-10-18', '2018-10-20', 'jgammill3@paginegialle.it',  4);
insert into rentals (apartment_id, check_in, check_out, guest,  rating) values (5, '2021-03-03', '2021-03-07', 'hcantu2@goo.gl', 4);
insert into rentals (apartment_id, check_in, check_out, guest,  rating) values (2, '2013-04-10', '2013-06-20', 'pperrigo4@wordpress.com',  5);
insert into rentals (apartment_id, check_in, check_out, guest,  rating) values (3, '2021-05-25', '2021-10-19', 'hcantu2@goo.gl', 5);
insert into rentals (apartment_id, check_in, check_out, guest,  rating) values (2, '2021-12-13', '2022-02-07', 'iobert1@opera.com',  2);
insert into rentals (apartment_id, check_in, check_out, guest,  rating) values (1, '2014-04-30', '2014-11-18', 'pperrigo4@wordpress.com',  5);
insert into rentals (apartment_id, check_in, check_out, guest,  rating) values (4, '2021-04-22', '2022-01-01', 'epropper0@baidu.com',  3);




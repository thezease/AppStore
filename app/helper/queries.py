"""
Functions created to mask raw SQL queries
To be called by app/views.py
"""
from __future__ import annotations

from django.db import connection
from django.db import IntegrityError, InternalError, DatabaseError

import re

from django.http import QueryDict


def dictfetchall_(cursor: connection.cursor) -> list[dict]:
    """
    Helper function
    Return all rows from a cursor as a dict that
    allows named reference to SQL query results in html templates
    e.g. {{ user.first_name }} instead of {{ user.0 }}
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def dictfetchone_(cursor: connection.cursor) -> dict:
    return dictfetchall_(cursor)[0]


def get_all_users() -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users ORDER BY first_name")
        records = dictfetchall_(cursor)
    return records


def get_single_user(email) -> dict:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT email, first_name, last_name, date_of_birth, since, 
                   country, credit_card_type, credit_card_no
            FROM users WHERE email = %s
            """, 
            [email]
        )
        return dictfetchone_(cursor)


def check_user_exists(email: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1
            FROM users
            WHERE email = %s
            """,
            [email])
        
        user = cursor.fetchone()

        if user == None: return False
        else: return True

def check_user_cardno(credit_card_no: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE credit_card_no = %s
            """,
            [credit_card_no])
        
        user = cursor.fetchone()

        if user == None: return False
        else: return True


def insert_user(form: QueryDict) -> str:
    """
    Returns status message of the insertion
        If insertion is successful: return success message
        Else: return error message
    """
    status = ''

    user_exsts = check_user_exists(form['email'])
    credcardno_exsts = check_user_cardno(form['credit_card_no'])
    
    if user_exsts:
        status = 'User with email %s already exists' % (form['email'])
    
    elif credcardno_exsts:
        status = 'User with credit card number %s already exists' % (form['credit_card_no'])

    else:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    CALL insert_users(%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        form['first_name'],
                        form['last_name'],
                        form['email'],
                        form['password'],
                        form['date_of_birth'],
                        form['country'],
                        form['credit_card_type'],
                        form['credit_card_no']
                    ]
                )
                status = 'Successfully registered.'

            except IntegrityError as ie:
                e_msg = str(ie.__cause__)
                # regex search to find the column that violated integrity constraint
                constraint = re.findall(r'(?<=\")[A-Za-z\_]*(?=\")', e_msg)[-1]
                status = f'Violated constraint: {constraint}. Please follow the required format.'
    
    return status


def authenticate_user(email:str, pw:str) -> bool:
    """Return True if password matches record in databse, else False"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT (password = %s)
            FROM users
            WHERE email = %s
            """,
            [pw, email])
        res = cursor.fetchone()
        if res == None:
            return False
        else:
            return res[0]


def update_user(form:QueryDict, email:str) -> str:
    """
    Returns status message of the update
        If update is successful: return success message
        Else: return error message
    """
    status = ''

    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """
                CALL update_users(%s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    form['first_name'],
                    form['last_name'],
                    form['date_of_birth'],
                    form['country'],
                    form['credit_card_type'],
                    form['credit_card_no'],
                    email
                ]
                )
            status = 'User edited successfully!'
       
        except IntegrityError as e:
            e_msg = str(e.__cause__)
            # regex search to find the column that violated integrity constraint
            constraint = re.findall(r'(?<=\")[A-Za-z\_]*(?=\")', e_msg)[1]
            status = f'Violated constraint: {constraint}. Please follow the required format.'

    return status


def find_apt_availability(form:QueryDict, apt_id:int) -> dict:
    res = {}
    dates_avail = list()
    year = int(form['year'])
    month = int(form['month'])
    num_days = days_in_mth[month]
    if year % 4 == 0 and month == 2: # leap year
        num_days += 1

    for day in range(1, num_days+1):
        curr_day = f'{year}-{month}-{day}'
        with connection.cursor() as cursor:
            cursor.execute(
                # uses user-defined function
                """
                SELECT * FROM check_single_date(%s, %s)
                """,
                [apt_id, curr_day]
            )
            avail = cursor.fetchone()[0]
            if avail:
                dates_avail.append(day)
    
    res['year'] = str(year)
    res['month'] = mth_num_to_text[month]
    res['dates'] = ', '.join(str(e) for e in dates_avail)

    return res
            

def get_single_apartment(apt_id:int) -> dict:
    with connection.cursor() as cursor:
        cursor.execute(
            # uses user-defined SQL function
            "SELECT * FROM get_selected_apt(%s)",
            [apt_id])
        selected_apt = dictfetchall_(cursor)[0]
    return selected_apt


def get_user_bookings(email:str) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT  tb.tempbooking_id, apt.country, apt.city, tb.check_in, tb.check_out, 
		            apt.price * (tb.check_out - tb.check_in + 1) AS total_price
            FROM tempbookings tb NATURAL JOIN apartments apt
            WHERE tb.guest = %s
            AND apt.listed = true
            ORDER BY tb.check_in ASC
            """,
            [email]
        )
        return dictfetchall_(cursor)


def get_user_rentals(email:str) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(
            # uses user-defined SQL function
            "Select * FROM selected_rental(%s)",
            [email]
        )
        return dictfetchall_(cursor)


def user_update_rental_rating(rental_id:int, new_rating:int) -> str:
    status = ''
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """
                UPDATE rentals
                SET rating = %s
                WHERE rental_id = %s
                """,
                [new_rating, rental_id]
                )
            status = 'Rating added/updated!'
       
        except (IntegrityError, InternalError) as e:
            status = str(e.__cause__)
    return status

def user_delete_booking(tempbooking_id:int) -> str:
    status = ''
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """
                DELETE FROM tempbookings
                WHERE tempbooking_id = %s
                """,
                [
                    tempbooking_id
                ]
            )
            status = 'Booking deleted.'
       
        except IntegrityError as e:
            status = str(e.__cause__)
    return status

def get_host_apartments(email:str) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(
                """
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
                apartments apt LEFT JOIN overall_ratings rts ON apt.apartment_id = rts.apartment_id
                LEFT JOIN
                (
                    SELECT apartment_id,  SUM(tp.stay_price) AS earning
                    FROM (
                        SELECT apartment_id, apt.price * (r.check_out - r.check_in + 1) AS stay_price
                        FROM rentals r NATURAL JOIN apartments apt
                    ) AS tp
                    GROUP BY apartment_id
                ) AS earning
                ON apt.apartment_id = earning.apartment_id
                WHERE host = %s
                ORDER BY apt.apartment_id ASC;
                """,
                [email]
        )
        apartments = dictfetchall_(cursor)
    return apartments

def get_host_bookings(email:str) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(
                """
                SELECT  apt.country, apt.city, apt.address, tb.check_in, tb.check_out, 
                        apt.price * (tb.check_out - tb.check_in + 1) AS total_price,
                        tb.tempbooking_id
                FROM tempbookings tb NATURAL JOIN apartments apt
                WHERE host = %s
                ORDER BY tb.check_in ASC;
                """,
                [email]
        )
        bookings = dictfetchall_(cursor)
    return bookings

def get_host_rentals(email:str) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(
                """
                SELECT  apt.country, apt.city, apt.address, r.check_in, r.check_out, 
                        apt.price * (r.check_out - r.check_in + 1) AS total_price
                FROM rentals r NATURAL JOIN apartments apt
                WHERE host = %s
                ORDER BY r.check_in ASC;
                """,
                [email]
        )
        rentals = dictfetchall_(cursor)
    return rentals

def host_new_apt(form:QueryDict, email:str) -> str:
    status = ''
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """
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
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s
                )
                """,
                [
                    email,
                    form['country'],
                    form['city'],
                    form['address'],
                    form['num_guests'],
                    form['num_beds'],
                    form['num_bathrooms'],
                    form['property_type'],
                    form['amenities'],
                    form['house_rules'],
                    form['price'],
                ]
                )
            status = 'Apartment added successfully!'
       
        except IntegrityError as e:
            status = str(e.__cause__)
    
    return status

def host_edit_apt(form:QueryDict, apt_id:int) -> str:
    status = ''
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """
                UPDATE apartments
                SET 
                    country = %s,
                    city = %s,
                    address = %s,
                    num_guests = %s,
                    num_beds = %s,
                    num_bathrooms = %s,
                    property_type = %s,
                    amenities = %s,
                    house_rules = %s,
                    price = %s
                WHERE apartment_id = %s;
                """,
                [
                    form['country'],
                    form['city'],
                    form['address'],
                    form['num_guests'],
                    form['num_beds'],
                    form['num_bathrooms'],
                    form['property_type'],
                    form['amenities'],
                    form['house_rules'],
                    form['price'],
                    apt_id,
                ]
                )
            status = 'Apartment details updated!'
       
        except IntegrityError as e:
            status = str(e.__cause__)
    return status

def host_toggle_apt_listing(apt_id:int) -> str:
    """
    Inverts columne (listed) for an apartment
    """
    status = ''
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """
                UPDATE apartments
                SET listed = (NOT listed)
                WHERE apartment_id = %s;
                """,
                [
                    apt_id
                ]
                )
            status = 'Apartment listing status changed!'
       
        except IntegrityError as e:
            status = str(e.__cause__)
    return status

def host_approve_booking(tempbooking_id:int) -> str:
    status = ''
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """
                UPDATE tempbookings
                SET status = CAST(1 AS BIT)
                WHERE tempbooking_id = %s
                """,
                [
                    tempbooking_id
                ]
            )
            status = 'Booking approved!'
       
        except IntegrityError as e:
            status = str(e.__cause__)
    
    return status

def host_delete_booking(tempbooking_id:int) -> str:
    return user_delete_booking(tempbooking_id)

def user_make_booking(form:QueryDict, apt_id:int) -> bool:
    status = ''
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """
                INSERT INTO tempbookings (
                    apartment_id,
                    check_in,
                    check_out,
                    guest
                )
                VALUES (%s, %s, %s, %s)
                """,
                [
                    apt_id,
                    form['check_in'],
                    form['check_out'],
                    form['email'],
                ]
            )
            status = 'Aparment has been booked. Waiting for approval from host.'
       
        except IntegrityError as e:
            status = str(e.__cause__)

    return status

""" Reference Data """
# for use in queries.find_apt_availability
days_in_mth = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

# for use in queries.find_apt_availability
mth_num_to_text = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

from readline import insert_text
from django.shortcuts import render, redirect
from django.db import connection
from django.db import IntegrityError, DatabaseError
from django.http import HttpResponse

import re

## Admin Login Panel
def login(request):
    result_dict = {}
    adminName = "IT2002"
    adminPassword = "it2002"
    if request.POST:
        if request.POST['login'] == "login":
            if request.POST['name'] == adminName and request.POST['password'] == adminPassword:
                return dashboard(request)
    return render(request,'app/admin_login.html', result_dict)

## Admin Dashboard Panel
def dashboard(request):
    """
    Shows dashboard data in admin page
    """
    
    result_dict = dict()

    # Number of registered users
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users")
        users_num = cursor.fetchone()
    result_dict['user_num'] = users_num[0]

    # Number of registered users in the past 7 days
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users WHERE since >= (CURRENT_DATE - 7)")
        users7_num = cursor.fetchone()
    result_dict['users7_num'] = users7_num[0]

    # Top 3 active guests
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT r.guest, u.country, COUNT(*),
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rank
        FROM users u, rentals r
        WHERE r.guest = u.email
        GROUP BY r.guest, u.country;
        """)
        activeGuests = cursor.fetchall()
    result_dict['activeGuests'] = activeGuests
    
    # Number of registered apartments
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM apartments")
        apartments_num = cursor.fetchone()
    result_dict['apartments_num'] = apartments_num[0]


    # Number of listed apartments
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM apartments WHERE listed = true")
        listedApartments_num = cursor.fetchone()
    result_dict['listedApartments_num'] = listedApartments_num[0]

    # Top 3 best rating of apartments
    with connection.cursor() as cursor:
        cursor.execute("SELECT a.apartment_id, ROUND(AVG(r.rating),1) \
                        FROM rentals r, apartments a \
                        WHERE r.apartment_id = a.apartment_id \
                        GROUP BY a.country, a.city, a.apartment_id \
                        ORDER BY ROUND(AVG(r.rating),1) DESC \
                        LIMIT 3;")
        top3apartments = cursor.fetchall()
    result_dict['top3apartments'] = top3apartments

    # Number of rentals
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM rentals")
        rentals_num = cursor.fetchone()
    result_dict['rentals_num'] = rentals_num[0]

    # Total income for all rentals
    with connection.cursor() as cursor:
        cursor.execute("SELECT SUM((r.check_out - r.check_in)*a.price) \
                        FROM rentals r, apartments a \
                        WHERE r.apartment_id = a.apartment_id;")
        rental_sum = cursor.fetchone()
    result_dict['rental_sum'] = rental_sum[0]

    # Top 3 lengths of stay for all rentals
    with connection.cursor() as cursor:
        cursor.execute("""SELECT rental_id, guest, (check_out-check_in) AS length_of_stay
                        FROM rentals
                        ORDER BY length_of_stay DESC;""")
        stayRank = cursor.fetchall()

    result_dict['stayRank'] = stayRank

    # Number of bookings
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM tempbookings;")
        bookings_num = cursor.fetchone()
    result_dict['bookings_num'] = bookings_num[0]

    # Total worth of all unsettled bookings
    with connection.cursor() as cursor:
        cursor.execute("SELECT SUM((t.check_out - t.check_in)*a.price) \
                        FROM tempbookings t, apartments a \
                        WHERE t.apartment_id = a.apartment_id;")
        booking_sum = cursor.fetchone()
    result_dict['booking_sum'] = booking_sum[0]

    # Rank of number of unsettled bookings by apartment
    with connection.cursor() as cursor:
        cursor.execute("""SELECT apartment_id, COUNT(*),
                        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rank
                        FROM tempbookings
                        GROUP BY apartment_id;""")
        bookingRank = cursor.fetchall()

    result_dict['bookingRank'] = bookingRank

    return render(request,'app/admin_dashboard.html', result_dict)


# rank of active guests
def dashboard_activeGuest_rank(request):
    """Shows rank of active guests DESC"""

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT r.guest, u.country, COUNT(*),
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rank
        FROM users u, rentals r
        WHERE r.guest = u.email
        GROUP BY r.guest, u.country;
        """)
        rank = cursor.fetchall()
    
    result_dict = {'Records': rank}

    return render(request,'app/admin_dashboard_activeGuest_rank.html', result_dict)

# rating rank of apartments
def dashboard_rating_rank(request):
    """Shows rating rank of all apartments DESC"""
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT a.country, a.city, a.address, a.apartment_id, ROUND(AVG(r.rating),1), \
                        ROW_NUMBER() OVER (ORDER BY ROUND(AVG(r.rating),1) DESC) AS rank \
                        FROM rentals r, apartments a \
                        WHERE r.apartment_id = a.apartment_id \
                        GROUP BY a.country, a.city, a.apartment_id")
        ratingRank = cursor.fetchall()

    result_dict = {'Records': ratingRank}

    return render(request,'app/admin_dashboard_rating_rank.html', result_dict)

# lengths of stay ranking for all rentals
def dashboard_lengthOfStay_rank(request):
    """Shows lengths of stay ranking for all rentals DESC"""
    
    with connection.cursor() as cursor:
        cursor.execute("""SELECT rental_id, guest, (check_out-check_in) AS length_of_stay
                        FROM rentals
                        ORDER BY length_of_stay DESC;""")
        rank = cursor.fetchall()

    result_dict = {'Records': rank}

    return render(request,'app/admin_dashboard_lengthOfStay_rank.html', result_dict)

# rank of unsettled booking numbers by apartments
def dashboard_bookingNum_rank(request):
    """Shows rank of unsettled booking numbers by apartments DESC"""
    
    with connection.cursor() as cursor:
        cursor.execute("""SELECT apartment_id, COUNT(*),
                        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rank
                        FROM tempbookings
                        GROUP BY apartment_id;""")
        rank = cursor.fetchall()

    result_dict = {'Records': rank}

    return render(request,'app/admin_dashboard_bookingNum_rank.html', result_dict)

## Admin User Panel
def users(request):
    """
    Shows user data in admin page
    """
    
    ## Delete/search customer 
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE email = %s", [request.POST['id']])
        elif request.POST['action'] == 'search':
            email = request.POST['email']
            with connection.cursor() as cursor:
                    cursor.execute("SELECT email FROM users")
                    allemail = cursor.fetchall()
            if tuple([email]) in allemail:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE email = %s", [email])
                    user = cursor.fetchone()
                result_dict = {'user': user}
                return render(request,'app/admin_users_search.html', result_dict)

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users ORDER BY first_name")
        users = cursor.fetchall()

    result_dict = {'records': users}

    return render(request,'app/admin_users.html', result_dict)

def users_edit(request, id):
    """Shows the user edit page"""

    result_dict = {}
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            [id]
            )
        user = cursor.fetchone()
    result_dict['user'] = user
    if user[7] == "visa":
        result_dict['visa'] = "checked"
        result_dict['americanexpress'] = ""
        result_dict['mastercard'] = ""
    elif user[7] == "americanexpress":
        result_dict['visa'] = ""
        result_dict['americanexpress'] = "checked"
        result_dict['mastercard'] = ""
    elif user[7] == "mastercard":
        result_dict['visa'] = ""
        result_dict['americanexpress'] = ""
        result_dict['mastercard'] = "checked"
    if request.POST:
        if request.POST['action'] == 'Update':
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        """
                        UPDATE users SET 
                        first_name = %s, 
                        last_name = %s, 
                        date_of_birth = %s, 
                        country = %s, 
                        credit_card_type = %s, 
                        credit_card_no = %s 
                        WHERE email = %s""",
                        [
                            request.POST['first_name'],
                            request.POST['last_name'],
                            request.POST['date_of_birth'],
                            request.POST['country'],
                            request.POST['credit_card_type'],
                            request.POST['credit_card_no'],
                            id
                            ]
                            )
                except IntegrityError as ie:
                    e_msg = str(ie.__cause__)
                    #regex search to find the column that violated integrity constraint
                    constraint = re.findall(r'(?<=\")[A-Za-z\_]*(?=\")', e_msg)[-1]
                    if constraint == 'users_credit_card_no_key':
                        status = f'Violated constraint: {constraint}. Card in use.Please type in a valid credit card number.'
                        result_dict['status'] = status
                    else:
                        status = f'Violated constraint: {constraint}. Please follow the required format.'
                        result_dict['status'] = status
                        
                    return render(request, "app/admin_users_edit.html", result_dict)
            return redirect("admin_users")
    return render(request, "app/admin_users_edit.html", result_dict)
 
def users_view(request, id):
    """
    Shows the view all user details, 
    which include user details and rental data
    """
    
    result_dict = dict()

    ## Use raw query to get a user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [id])
        selected_user = cursor.fetchone()
    result_dict['user'] = selected_user

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT r.apartment_id, ap.host, ap.country, ap.city, r.check_in, r.check_out, ROUND((r.check_out - r.check_in)*ap.price, 2) AS total_price, r.rating
            FROM apartments ap, rentals r 
            WHERE ap.apartment_id = r.apartment_id AND r.guest = %s;
            """,
            [id])
        selected_rentals = cursor.fetchall()

    result_dict['records'] = selected_rentals

    return render(request,'app/admin_users_view.html', result_dict)

def users_add(request):
    """Add User"""
    context = {}
    status = ''

    if request.POST:
        if request.POST['action'] == 'Add':
            ## Check if email is already in the table
            with connection.cursor() as cursor:

                cursor.execute("SELECT * FROM users WHERE email = %s", [request.POST['email']])
                user = cursor.fetchone()
                ## No user with same email
                if user == None:
                    try:
                        cursor.execute(
                            """
                            INSERT INTO users 
                            (first_name, last_name, email, password, date_of_birth, country, credit_card_type, credit_card_no) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                            [
                                request.POST['first_name'],
                                request.POST['last_name'],
                                request.POST['email'],
                                request.POST['password'],
                                request.POST['date_of_birth'],
                                request.POST['country'],
                                request.POST['credit_card_type'],
                                request.POST['credit_card_no']
                            ]
                            )
                    except IntegrityError as ie:
                        e_msg = str(ie.__cause__)
                        # regex search to find the column that violated integrity constraint
                        constraint = re.findall(r'(?<=\")[A-Za-z\_]*(?=\")', e_msg)[-1]
                        status = f'Violated constraint: {constraint}. Please follow the required format.'
                        return status

                    return redirect('admin_users')    
                else:
                    status = 'User with email %s already exists' % (request.POST['email'])


    context['status'] = status
 
    return render(request, "app/admin_users_add.html", context)

## Admin Statistics Panel
def statistics(request):
    """
    Shows statistics panel in admin page
    """
    result_dict = {}

    if request.POST:
        if request.POST['action'] == 'section1':
            country = request.POST['country']
            stats = request.POST['stats1']
            if stats == "section1table1":
                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT ranks.guest_nationality, ranks.income, ranks.rank 
                        FROM ( 
                            SELECT a.country AS apartment_country, u.country AS guest_nationality, ROUND(SUM((r.check_out - r.check_in)*a.price), 2) AS income,
                            ROW_NUMBER() OVER (PARTITION BY a.country ORDER BY ROUND(SUM((r.check_out - r.check_in)*a.price), 2) DESC) AS rank
                            FROM apartments a, rentals r, users u 
                            WHERE a.apartment_id = r.apartment_id 
                            AND r.guest = u.email 
                            GROUP BY apartment_country, guest_nationality 
                        ) AS ranks 
                        WHERE ranks.apartment_country = %s""",
                        [
                            country
                        ]
                        )
                    ranking = cursor.fetchall()
                result_dict['table'] = ranking
                result_dict['country'] = country
                return render(request,'app/admin_statistics_table1.html', result_dict)
            elif stats == "section1table2":
                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT a.city, ROUND(SUM((r.check_out - r.check_in)*a.price),2),
                        ROW_NUMBER() over (ORDER BY ROUND(SUM((r.check_out - r.check_in)*a.price),2) DESC) AS country_rank 
                        FROM rentals r, apartments a
                        WHERE r.apartment_id = a.apartment_id AND a.country = %s
                        GROUP BY a.city;""",
                        [
                            country
                        ]
                        )
                    ranking = cursor.fetchall()
                result_dict['table'] = ranking
                result_dict['country'] = country
                return render(request,'app/admin_statistics_table2.html', result_dict)
            elif stats == "section1table3":
                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT u.country AS guest_nationality, COUNT(*) AS number_of_guests,
                        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rank
                        FROM apartments a, rentals r, users u
                        WHERE a.apartment_id = r.apartment_id AND r.guest = u.email AND a.country = %s
                        GROUP BY guest_nationality;
                        """,
                        [
                            country
                        ]
                        )
                    ranking = cursor.fetchall()
                result_dict['table'] = ranking
                result_dict['country'] = country
                return render(request,'app/admin_statistics_table3.html', result_dict)
        elif request.POST['action'] == 'section2':
            stats = request.POST['stats2']
            if stats == "section2table1":
                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT u.country AS guest_nationality, u.credit_card_type, ROUND(SUM((r.check_out - r.check_in)*a.price), 2) AS income,
                        ROW_NUMBER() OVER (PARTITION BY u.country ORDER BY ROUND(SUM((r.check_out - r.check_in)*a.price), 2) DESC) AS rank
                        FROM users u , rentals r, apartments a
                        WHERE u.email = r.guest AND a.apartment_id = r.apartment_id
                        GROUP BY guest_nationality, u.credit_card_type;""")
                    ranking = cursor.fetchall()
                result_dict['table'] = ranking
                return render(request,'app/admin_statistics_table4.html', result_dict)
            elif stats == "section2table2":
                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT u.country, u.credit_card_type, COUNT(*),
                        ROW_NUMBER() OVER (PARTITION BY u.country ORDER BY COUNT(*) DESC) AS rank
                        FROM users u, rentals r
                        WHERE u.email = r.guest
                        GROUP BY u.country, u.credit_card_type;""")
                    ranking = cursor.fetchall()
                result_dict['table'] = ranking
                return render(request,'app/admin_statistics_table5.html', result_dict)
        elif request.POST['action'] == 'section3':
            stats = request.POST['stats3']
            if stats == "section3table1":
                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT a.country, ROUND(AVG(r.check_out-r.check_in),1) AS average_length_of_stay,
                            ROW_NUMBER() over (ORDER BY ROUND(AVG(r.check_out-r.check_in),1) DESC) AS rank 
                            FROM rentals r, apartments a
                            WHERE r.apartment_id = a.apartment_id
                            GROUP BY a.country;""")
                    ranking = cursor.fetchall()
                result_dict['table'] = ranking
                return render(request,'app/admin_statistics_table6.html', result_dict)
            elif stats == "section3table2":
                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT a.country, SUM(r.check_out-r.check_in) AS total_length_of_stay,
                            ROW_NUMBER() over (ORDER BY SUM(r.check_out-r.check_in) DESC) AS rank 
                            FROM rentals r, apartments a
                            WHERE r.apartment_id = a.apartment_id
                            GROUP BY a.country;""")
                    ranking = cursor.fetchall()
                result_dict['table'] = ranking
                return render(request,'app/admin_statistics_table7.html', result_dict)

    ##  Get all guest nationalities
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT country FROM apartments ORDER BY country")
        countries = cursor.fetchall()

    result_dict['records'] = countries

    return render(request,'app/admin_statistics.html', result_dict)

def statistics_table1(request, id):
    result_dict = {}
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT ranks.guest_nationality, ranks.income, ranks.rank \
            FROM ( \
                SELECT a.country AS apartment_country, u.country AS guest_nationality, ROUND(SUM((r.check_out - r.check_in)*a.price), 2) AS income, \
                ROW_NUMBER() OVER (PARTITION BY a.country ORDER BY ROUND(SUM((r.check_out - r.check_in)*a.price), 2) DESC) AS rank \
                FROM apartments a, rentals r, users u \
                WHERE a.apartment_id = r.apartment_id \
                AND r.guest = u.email \
                GROUP BY apartment_country, guest_nationality \
            ) AS ranks \
            WHERE ranks.apartment_country = %s",
            [
                id
            ]
            )
        ranking = cursor.fetchall()
    result_dict['table1'] = ranking

    return render(request,'app/admin_statistics_table1.html', result_dict)

## Admin Aparments Panel
def apartments(request):
    """
    Shows Apartment Panel in admin page
    """
    
    ## Delete/search apartment
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM apartments WHERE apartment_id = %s", [request.POST['id']])
        elif request.POST['action'] == 'search':
            apartment_id = request.POST['apartment']
            with connection.cursor() as cursor:
                    cursor.execute("SELECT apartment_id FROM apartments")
                    allapartment = cursor.fetchall()
            if apartment_id in list(map(lambda x: str(x[0]), allapartment)):
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM apartments WHERE apartment_id = %s", [apartment_id])
                    apartment = cursor.fetchone()
                result_dict = {'apartment': apartment}
                return render(request,'app/admin_apartments_search.html', result_dict)

    ## Use raw query to get all apartments
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM apartments ORDER BY apartment_id")
        apartments = cursor.fetchall()

    result_dict = {'records': apartments}

    return render(request,'app/admin_apartments.html', result_dict)

def apartments_edit(request, id):
    """Shows the apartment edit page"""

    result_dict = {}
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM apartments WHERE apartment_id = %s",
            [id]
            )
        apartment = cursor.fetchone()
    result_dict['apartment'] = apartment
    
    if request.POST:
        if request.POST['action'] == 'Update':
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE apartments
                    SET host = %s, 
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
                    WHERE apartment_id = %s;""",
                    [
                        request.POST['host'],
                        request.POST['country'],
                        request.POST['city'],
                        request.POST['address'],
                        request.POST['num_guests'],
                        request.POST['num_beds'],
                        request.POST['num_bathrooms'],
                        request.POST['property_type'],
                        request.POST['amenities'],
                        request.POST['house_rules'],
                        request.POST['price'],
                        id
                    ]
                    )
            return redirect("/admin_apartments")
    return render(request, "app/admin_apartments_edit.html", result_dict)


def apartments_view(request, id):
    """
    Shows the view all apartment details, 
    which include apartment details and rental data
    """
    
    result_dict = dict()

    ## Use raw query to get the apartment
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM apartments WHERE apartment_id = %s", [id])
        apartment = cursor.fetchone()
    result_dict['apartment'] = apartment

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT r.*, ROUND((r.check_out - r.check_in)*ap.price, 2)
            FROM apartments ap, rentals r 
            WHERE ap.apartment_id = r.apartment_id 
            AND r.apartment_id = %s""",
            [id])
        selected_rentals = cursor.fetchall()

    result_dict['records'] = selected_rentals

    return render(request,'app/admin_apartments_view.html', result_dict)

def apartments_add(request):
    """Add Apartment"""
    context = {}
    status = ''

    if request.POST:
        if request.POST['action'] == 'Add':
            if 'listed' in request.POST:
                    listed = "TRUE"
            else:
                listed = "FALSE"
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO apartments (host, country, city, address, num_guests, num_beds, num_bathrooms, property_type, amenities, house_rules, price, listed) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    [
                        request.POST['host'],
                        request.POST['country'],
                        request.POST['city'],
                        request.POST['address'],
                        request.POST['num_guests'],
                        request.POST['num_beds'],
                        request.POST['num_bathrooms'],
                        request.POST['property_type'],
                        request.POST['amenities'],
                        request.POST['house_rules'],
                        request.POST['price'],
                        listed
                    ]
                    )
                return redirect('/admin_apartments')    

    context['status'] = status
    return render(request, "app/admin_apartments_add.html", context)


## Admin Retals Panel
def rentals(request):
    """
    Shows Rental Panel in admin page
    """
    
    ## Delete/search rental
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM rentals WHERE rental_id = %s", [request.POST['id']])
        elif request.POST['action'] == 'search':
            rental_id = request.POST['rental']
            with connection.cursor() as cursor:
                    cursor.execute("SELECT rental_id FROM rentals")
                    allrental = cursor.fetchall()
            if rental_id in list(map(lambda x: str(x[0]), allrental)):
                with connection.cursor() as cursor:
                    cursor.execute("""
                    SELECT r.*, ROUND((r.check_out - r.check_in)*a.price, 2)
                    FROM rentals r, apartments a
                    WHERE r.apartment_id = a.apartment_id AND rental_id = %s""", [rental_id])
                    rental = cursor.fetchone()
                result_dict = {'rental': rental}
                return render(request,'app/admin_rentals_search.html', result_dict)



    ## Use raw query to get all rentals
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT r.*, ROUND((r.check_out - r.check_in)*a.price, 2)
        FROM rentals r, apartments a
        WHERE r.apartment_id = a.apartment_id
        ORDER BY rental_id;
        """)
        rentals = cursor.fetchall()

    result_dict = {'records': rentals}

    return render(request,'app/admin_rentals.html', result_dict)

def rentals_edit(request, id):
    """Shows the rental edit page"""
    status = ''
    result_dict = {}
    
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM rentals WHERE rental_id = %s",
            [id]
            )
        rental = cursor.fetchone()
    result_dict['rental'] = rental
    
    if request.POST:
        if request.POST['action'] == 'Update':
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        """
                        UPDATE rentals
                        SET apartment_id = %s, 
                        check_in = %s, 
                        check_out = %s, 
                        guest = %s,
                        rating = %s
                        WHERE rental_id = %s;""",
                        [
                            request.POST['apartment_id'],
                            request.POST['check_in'],
                            request.POST['check_out'],
                            request.POST['guest'],
                            request.POST['rating'],
                            id
                        ]
                        )
                    status = 'Rental edited successfully!'
                    result_dict['status'] = status

                except IntegrityError as e:
                    e_msg = str(e.__cause__)
                    # regex search to find the column that violated integrity constraint
                    constraint = re.findall(r'(?<=\")[A-Za-z\_]*(?=\")', e_msg)[1]
                    status = f'Violated constraint: {constraint}. Please follow the required format.'
                    result_dict['status'] = status
                    return render(request, "app/admin_rentals_edit.html", result_dict)
            return redirect("/admin_rentals")
    return render(request, "app/admin_rentals_edit.html", result_dict)

def rentals_add(request):
    """Add Rental"""
    context = {}
    status = ''

    if request.POST:
        if request.POST['action'] == 'Add':
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO rentals (apartment_id, check_in, check_out, guest, rating)
                    VALUES (%s, %s, %s, %s, %s)""",
                    [
                        request.POST['apartment_id'],
                        request.POST['check_in'],
                        request.POST['check_out'],
                        request.POST['guest'],
                        request.POST['rating']
                    ]
                    )
                return redirect('/admin_rentals')    

    context['status'] = status
    return render(request, "app/admin_rentals_add.html", context)


## Admin Bookings Panel
def bookings(request):
    """
    Shows Booking Panel in admin page
    """
    
    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM tempbookings WHERE tempbooking_id = %s", [request.POST['id']])
        elif request.POST['action'] == 'search':
            booking_id = request.POST['booking']
            with connection.cursor() as cursor:
                cursor.execute("SELECT tempbooking_id FROM tempbookings")
                allbooking = cursor.fetchall()
            if booking_id in list(map(lambda x: str(x[0]), allbooking)):
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM tempbookings WHERE tempbooking_id = %s", [booking_id])
                    booking = cursor.fetchone()
                result_dict = {'booking': booking}
                return render(request,'app/admin_bookings_search.html', result_dict)



    ## Use raw query to get all bookings
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tempbookings ORDER BY tempbooking_id")
        bookings = cursor.fetchall()

    result_dict = {'records': bookings}

    return render(request,'app/admin_bookings.html', result_dict)

def bookings_edit(request, id):
    """Shows the bookings edit page"""

    result_dict = {}
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM tempbookings WHERE tempbooking_id = %s",
            [id]
            )
        booking = cursor.fetchone()
    result_dict['booking'] = booking
    
    if request.POST:
        if request.POST['action'] == 'Update':
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tempbookings
                    SET apartment_id = %s, 
                    check_in = %s, 
                    check_out = %s, 
                    guest = %s
                    WHERE tempbooking_id = %s;""",
                    [
                        request.POST['apartment_id'],
                        request.POST['check_in'],
                        request.POST['check_out'],
                        request.POST['guest'],
                        id
                    ]
                    )
            return redirect("/admin_bookings")
    return render(request, "app/admin_bookings_edit.html", result_dict)

def bookings_add(request):
    """Add bookings"""
    context = {}
    status = ''

    if request.POST:
        if request.POST['action'] == 'Add':
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tempbookings (apartment_id, check_in, check_out, guest, status)
                    VALUES (%s, %s, %s, %s, %s)""",
                    [
                        request.POST['apartment_id'],
                        request.POST['check_in'],
                        request.POST['check_out'],
                        request.POST['guest'],
                        '0'
                    ]
                    )
                return redirect('/admin_bookings')    

    context['status'] = status
    return render(request, "app/admin_bookings_add.html", context)

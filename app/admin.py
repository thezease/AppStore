from readline import insert_text
from django.shortcuts import render, redirect
from django.db import connection

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

    # Number of registered apartments
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM apartments")
        apartments_num = cursor.fetchone()
    result_dict['apartments_num'] = apartments_num[0]

    # Number of rentals
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM rentals")
        rentals_num = cursor.fetchone()
    result_dict['rentals_num'] = rentals_num[0]

    # Number of registered users in the past 7 days
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users WHERE since >= (CURRENT_DATE - 7)")
        users7_num = cursor.fetchone()
    result_dict['users7_num'] = users7_num[0]

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

    # Total income for all rentals
    with connection.cursor() as cursor:
        cursor.execute("SELECT SUM(total_price) FROM rentals;")
        rental_sum = cursor.fetchone()
    result_dict['rental_sum'] = rental_sum[0]

    return render(request,'app/admin_dashboard.html', result_dict)

# rating rank of apartments
def rating_rank(request):
    """Shows rating rank of all apartments DESC"""
    
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT a.country, a.city, a.address, a.apartment_id, ROUND(AVG(r.rating),1) \
                        FROM rentals r, apartments a \
                        WHERE r.apartment_id = a.apartment_id \
                        GROUP BY a.country, a.city, a.apartment_id \
                        ORDER BY ROUND(AVG(r.rating),1) DESC")
        ratingRank = cursor.fetchall()

    result_dict = {'Records': ratingRank}

    return render(request,'app/rating_rank.html', result_dict)

## Admin User Panel
def users(request):
    """
    Shows user data in admin page
    """
    
    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE email = %s", [request.POST['id']])



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
            SELECT * 
            FROM apartments ap, rentals r 
            WHERE ap.apartment_id = r.apartment_id 
            AND r.guest = %s""",
            [id])
        selected_rentals = cursor.fetchall()

    result_dict['records'] = selected_rentals

    return render(request,'app/admin_users_view.html', result_dict)

def users_add(request):
    """Add User"""
    context = {}
    status = ''

    if request.POST:
        ## Check if email is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM users WHERE email = %s", [request.POST['email']])
            user = cursor.fetchone()
            ## No user with same email
            if user == None:
                ##TODO: date validation
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
        if request.POST['action'] == 'table1':
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT ranks.guest_nationality, ranks.income, ranks.rank \
                    FROM ( \
                        SELECT a.country AS apartment_country, u.country AS guest_nationality, ROUND(SUM(r.total_price), 2) AS income, \
                        ROW_NUMBER() OVER (PARTITION BY a.country ORDER BY ROUND(SUM(r.total_price), 2) DESC) AS rank \
                        FROM apartments a, rentals r, users u \
                        WHERE a.apartment_id = r.apartment_id \
                        AND r.guest = u.email \
                        GROUP BY apartment_country, guest_nationality \
                    ) AS ranks \
                    WHERE ranks.apartment_country = %s "
                    [
                        request.POST['country']
                    ]
                    )
                ranking = cursor.fetchall()
                result_dict['table1'] = ranking

    ##  Get all guest nationalities
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT country FROM users ORDER BY country")
        countries = cursor.fetchall()

    result_dict['records'] = countries

    return render(request,'app/admin_statistics.html', result_dict)

## Admin Aparments Panel
def apartments(request):
    """
    Shows Apartment Panel in admin page
    """
    
    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM apartments WHERE apartment_id = %s", [request.POST['id']])



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
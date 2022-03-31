from django.urls import reverse
from readline import insert_text
from django.shortcuts import render, redirect
from django.db import connection

from app.helper import queries


def index(request):
    """Shows the main page"""
    context = {}
    context['user_page'] = 'Login'
    context['user_action'] = '/login'

    return render(request, 'app/index.html', context)


def login(request):
    """Shows the user login page"""
    context = {}
    status = ''

    if request.POST:
        email = request.POST['login_email']
        pw = request.POST['login_password']
        auth = queries.authenticate_user(email, pw)
        if auth:
            context['user_page'] = 'Me'
            return redirect(reverse('user_index', kwargs={'email':email}))
        else:
            status = "Wrong email or password. Please try again."
            context['status'] = status

    return render(request, "app/login.html", context)



def register(request):
    """Shows the user registration page"""
    context = {}
    status = ''

    if request.POST:
        status = queries.insert_user(request.POST)

    context['status'] = status
 
    return render(request, "app/user-registration.html", context)





def user_index(request, email):
    """Shows user's homepage after login"""
    context = {}
    context['user_page'] = 'Me'
    context['user_action'] = '/viewself'

    return render(request, 'app/index.html', context)


def user_search(request, email):
    """Shows user's homepage after login"""
    context = {}
    context['user_page'] = 'Me'
    context['user_action'] = '/viewself'

    return render(request, 'app/search.html', context)


def viewself(request, email):
    """
    Shows the view user details page after login, 
    which include user details and rental data
    """

    context = {}
    context['user_page'] = 'Me'
    context['user_action'] = '/viewself'

    ## Use raw query to get a user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [email])
        selected_user = cursor.fetchone()
    context['user'] = selected_user

    with connection.cursor() as cursor:
        cursor.execute(
            # uses user-defined SQL function
            "Select * FROM selected_rental(%s)",
            [email])
        selected_rentals = cursor.fetchall()

    context['records'] = selected_rentals

    return render(request,'app/viewself.html', context)



def checkpw(request, email):
    """Shows page to enter password and allow user to edit own details once password matches"""
    result_dict = {}
    status = ''

    if request.POST:
        if request.POST['action'] == 'enterpw':
            # auth is True is password submitted matches DB record
            auth = queries.authenticate_user(email, request.POST['password'])
            if auth:
                user = queries.get_single_user(email)
                result_dict['user'] = user
                result_dict['visa'] = ""
                result_dict['americanexpress'] = ""
                result_dict['mastercard'] = ""
                result_dict[user['credit_card_type']] = "checked" # check radio button
                return render(request, "app/edit.html", result_dict)
            else:
                status = 'Incorrect password!'
                context = {'status': status}
                return render(request, "app/checkpw.html", context)


        elif request.POST['action'] == 'Update':
            status = queries.update_user(request.POST, email)
            result_dict['status'] = status

            user = queries.get_single_user(email)
            result_dict['user'] = user
            result_dict['visa'] = ""
            result_dict['americanexpress'] = ""
            result_dict['mastercard'] = ""
            result_dict[user['credit_card_type']] = "checked" # check radio button

            return render(request, "app/edit.html", result_dict)

    context = {"status": status}
    return render(request, "app/checkpw.html")



def search(request):
    """Shows the search page for apartments"""
    context = {}
    status = ''

    if request.POST:
        if request.POST['action'] == 'search':
            with connection.cursor() as cursor:
                cursor.execute(
                 # uses user-defined SQL function
                 "SELECT * FROM get_apartment(%s,%s,%s)",
                [
                    request.POST['country'],
                    request.POST['city'],
                    request.POST['num_guests']
                ])                
                apartments = cursor.fetchall()

            result_dict = {'records': apartments}

            return render(request,'app/search.html', result_dict)
    else:
        context['status'] = status
        ## Use sample query to get apartments

        """
        SQL VIEW ALREADY CREATED:

        CREATE VIEW overall_ratings AS
        SELECT ap.apartment_id, CAST(AVG(r.rating) AS DECIMAL(2, 1)) AS avg_rating
        FROM apartments ap, rentals r
        WHERE ap.apartment_id = r.apartment_id
        GROUP BY ap.apartment_id;
        """

        with connection.cursor() as cursor:
            cursor.execute(
                # uses user-defined SQL function
                "SELECT * FROM get_all_apartments()"),
            apartments = cursor.fetchall()

        result_dict = {'records': apartments}

        return render(request,'app/search.html', result_dict)


def apartment(request, apt_id):
    """Shows the apartment details page"""
    
    result_dict = dict()

    result_dict['apt'] = queries.get_single_apartment(apt_id)

    if request.POST:
        dates_avail = queries.find_apt_availability(request.POST, apt_id)
        result_dict['dates_avail'] = {
                                    'year': request.POST['year'],
                                    'month': request.POST['month'],
                                    'dates': dates_avail
                                    }

    return render(request,'app/apartment.html', result_dict)



def users(request):
    """Shows all users in page"""
    
    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE email = %s", [request.POST['id']])



    ## Call function defined in db_fns.py
    ## which masks raw query in python function
    users = queries.get_all_users()

    result_dict = {'records': users}

    return render(request,'app/users.html', result_dict)

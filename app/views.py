from django.urls import reverse
from readline import insert_text
from django.shortcuts import render, redirect
from django.db import connection

from app.helper import queries


def index(request):
    """Shows the main page"""
    return render(request, 'app/index.html')


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
    if status == 'Successfully registered.':
        context['redirect_msg'] = 'You may now login to our App.'
 
    return render(request, "app/user-registration.html", context)


def user_index(request, email):
    """Shows user's homepage after login"""
    # return render(request, 'app/index.html')
    return index(request)


def search(request):
    """Shows user's homepage after login"""
    result_dict = {}
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
                    ]
                )                
                apartments = queries.dictfetchall_(cursor)
            result_dict['records'] = apartments
            result_dict['orderby'] = 'price'

            return render(request,'app/search-apartments.html', result_dict)
    
    else:
        # default results with all apartments
        # ordered by price asc
        with connection.cursor() as cursor:
            cursor.execute(
                # uses user-defined SQL function
                "SELECT * FROM get_all_apartments()"
            )
            apartments = queries.dictfetchall_(cursor)
        result_dict['records'] = apartments
        result_dict['orderby'] = 'price'
    
    if request.GET:
        if request.GET['orderby'] == 'price':
            result_dict['orderby'] = 'price'
        elif request.GET['orderby'] == 'rating':
            result_dict['orderby'] = 'avg_rating'

    return render(request,'app/search-apartments.html', result_dict)


def user_search(request, email):
    return search(request)


def apartment(request, apt_id):
    """Shows the apartment details page"""
    
    result_dict = dict()

    result_dict['apt'] = queries.get_single_apartment(apt_id)

    if request.POST:
        if request.POST['action'] == 'checkavail':
            dates_avail = queries.find_apt_availability(request.POST, apt_id)
            result_dict['dates_avail'] = dates_avail
        if request.POST['action'] == 'book':
            pass

    return render(request,'app/apartment.html', result_dict)


def user_view_apt(request, email, apt_id):
    """Shows the apartment details page for login user"""
    return apartment(request, apt_id)


def viewself(request, email):
    """
    Shows the view user details page after login, 
    which include user details and rental data
    """
    context = {}
    
    if request.POST:
        if request.POST['rate']:
            rental_id = request.POST['rate']

    # call method form helper module queries
    context['user'] = queries.get_single_user(email)
    context['bookings'] = queries.get_user_bookings(email)
    context['rentals'] = queries.get_user_rentals(email)

    return render(request,'app/viewself-guest.html', context)



def viewself_host(request, email):
    """
    Shows the view user details page after login, 
    which include user details and rental data
    """
    context = {}

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

    return render(request,'app/viewself-host.html', context)



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

    result_dict["status"] = status
    result_dict["email"] = email
    return render(request, "app/checkpw.html", result_dict)










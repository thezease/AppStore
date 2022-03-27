from readline import insert_text
from django.shortcuts import render, redirect
from django.db import connection

from app.helper import queries

# Create your views here.
def index(request):
    """Shows the main page"""

    return render(request, 'app/index.html')



# Create your views here.
def view(request, userid):
    """
    Shows the view user details page, 
    which include user details and rental data
    """
    
    result_dict = dict()

    ## Use raw query to get a user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [userid])
        selected_user = cursor.fetchone()
    result_dict['user'] = selected_user

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * 
            FROM apartments ap, rentals r 
            WHERE ap.apartment_id = r.apartment_id 
            AND r.guest = %s""",
            [userid])
        selected_rentals = cursor.fetchall()

    result_dict['records'] = selected_rentals

    return render(request,'app/view.html', result_dict)



# Create your views here.
def add(request):
    """Shows the user registration page"""
    context = {}
    status = ''

    if request.POST:
        status = queries.insert_user(request.POST)

    context['status'] = status
 
    return render(request, "app/add.html", context)



def checkpw(request, userid):
    """Shows page to enter password and allow user to edit own details once password matches"""
    result_dict = {}
    status = ''

    if request.POST:
        if request.POST['action'] == 'enterpw':
            # auth is True is password submitted matches DB record
            auth = queries.authenticate_pw(request.POST['password'], userid)
            if auth:
                user = queries.get_single_user(userid)
                result_dict['user'] = user
                return render(request, "app/edit.html", result_dict)
            else:
                status = 'Incorrect password!'
                context = {'status': status}
                return render(request, "app/checkpw.html", context)


        elif request.POST['action'] == 'Update':
            status = queries.update_user(request.POST, userid)

            context = {'status': status}
            return render(request, "app/edit.html", context)

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

    ## Use raw query to get an apartment
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * 
            FROM apartments apt, overall_ratings rts 
            WHERE apt.apartment_id = rts.apartment_id 
            AND apt.apartment_id = %s
            """,
            [apt_id])
        selected_apt = cursor.fetchone()
    result_dict['apt'] = selected_apt

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

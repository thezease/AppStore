from django.db import connection
from django.db import IntegrityError, DatabaseError

import re

from django.http import QueryDict


def dictfetchall_(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_all_users():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users ORDER BY first_name")
        records = dictfetchall_(cursor)
    return records


def get_single_user(userid):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [userid])
        return cursor.fetchone()


def check_user_exists(email: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = %s
            """,
            [email])
        
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
    if user_exsts:
        status = 'User with email %s already exists' % (form['email'])

    else:
        with connection.cursor() as cursor:
            ##TODO: date validation
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
                status = 'Successfully inserted.'

            except IntegrityError as ie:
                e_msg = str(ie.__cause__)
                # regex search to find the column that violated integrity constraint
                constraint = re.findall(r'(?<=\")[A-Za-z\_]*(?=\")', e_msg)[-1]
                status = f'Violated constraint: {constraint}. Please follow the required format.'
    
    return status

def authenticate_pw(pw:str, userid:str) -> bool:
    """Return True if password matches record in databse, else False"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT (password = %s)
            FROM users
            WHERE email = %s
            """,
            [pw, userid])
        res = cursor.fetchone()
        if res == None:
            return False
        else:
            return res[0]


def update_user(form:QueryDict, userid:str) -> str:
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
                    userid
                ]
                )
            status = 'User edited successfully!'
       
        except IntegrityError as e:
            e_msg = str(e.__cause__)
            # regex search to find the column that violated integrity constraint
            constraint = re.findall(r'(?<=\")[A-Za-z\_]*(?=\")', e_msg)[1]
            status = f'Violated constraint: {constraint}. Please follow the required format.'

    return status


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

def find_apt_availability(form:QueryDict, apt_id:int) -> str:
    dates_avail = list()
    year = int(form['year'])
    month = int(form['month'])
    for day in range(1, days_in_mth[month]+1):
        curr_day = f'{year}-{month}-{day}'
        with connection.cursor() as cursor:
            cursor.execute(
                # uses user-defined function
                """
                SELECT check_single_date(%s, %s)
                """,
                [apt_id, curr_day]
            )
            avail = cursor.fetchone()[0]
            if avail:
                dates_avail.append(day)
    return ', '.join(str(e) for e in dates_avail)
            

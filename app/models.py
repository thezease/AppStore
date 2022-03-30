from django.db import models, connection

class User(models.Model):
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM users ORDER BY first_name")
    #     users = cursor.fetchall()
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    since = models.DateField(auto_now_add=True)
    country = models.CharField(max_length=32)
    credit_card_type = models.CharField(max_length=16)
    credit_card_no  = models.CharField(max_length=16)

class Apartment(models.Model):
    apartment_id = models.IntegerField()
    host = models.CharField(max_length=64)
    country = models.CharField(max_length=16)
    city = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    num_guests = models.IntegerField()
    num_beds = models.IntegerField()
    num_bathrooms = models.IntegerField()
    property_type = models.CharField(max_length=64)
    amenities = models.CharField(max_length=64)
    house_rules = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=8, decimal_places=2)


class Rental(models.Model):
    rental_id = models.IntegerField()
    apartment_id = models.IntegerField()
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.CharField(max_length=64)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.IntegerField()


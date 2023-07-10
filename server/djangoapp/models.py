from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f'Name: {self.name}\n Description: {self.description}'

class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'SUV'
    PICKUP = 'pickup'
    VAN = 'van'
    WAGON = 'wagon'
    CAR_TYPES = [
		(SEDAN, 'Sedan'),
		(SUV, 'SUV'),
		(PICKUP, 'Pickup'),
		(VAN, 'Van'),
		(WAGON, 'Wagon')
	]
    
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    dealer_id = models.IntegerField(null=False,
                                    validators=[MaxValueValidator(20), MinValueValidator(1)])
    type = models.CharField(max_length=8, choices=CAR_TYPES, default=SEDAN)
    year = models.DateField(null=False, default=now)
    
    def __str__(self):
        return f'{self.car_make.name} {self.name} ({self.type}), {self.year}.\n' + \
               f'Dealer_ID = {self.dealer_id}.'


class CarDealer:

    def __init__(self, id, city, state, st, address, zip_code, 
                 lat, longt, short_name, full_name):
        self.id = id
        self.city = city
        self.st = st
        self.state = state
        self.address = address
        self.zip_code = zip_code
        self.lat = lat
        self.longt = longt
        self.short_name = short_name
        self.full_name = full_name
        
    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    def __init__(self, id, name, dealership, review, purchase, purchase_date, 
                 car_make, car_model, car_year, sentiment):
        self.id = id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        
    def __str__(self):
        return f'The review of {self.car_make} {self.car_model}' + \
               f'from {self.dealership} was: {self.sentiment}.'

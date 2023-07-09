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


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data

from distutils import file_util
from django.db import models
from django.utils.timezone import now
import datetime

class CarMake(models.Model):
    name = models.TextField(null = False, primary_key=True)
    description = models.TextField()
    def __str__(self):
        return(f"Name: {self.name}, \n Description: {self.description}")

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null = False, max_length = 20, primary_key=True)
    dealerID = models.IntegerField(null=False)
    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    COUPE = "coupe"
    HATCHBACK = "hatchback"
    MODEL_CHOICES = [
        (SEDAN,"Sedan"),
        (SUV, "SUV"),
        (WAGON, "WAGON"),
        (COUPE, "Coupe"),
        (HATCHBACK, "Hatchback")
    ]
    type = models.CharField(max_length=120, choices=MODEL_CHOICES)
    year = models.IntegerField(default=datetime.date.today().year)

    def __str__(self):
        return(f"Make: {self.make},\nName: {self.name},\n\
            Dealer-ID: {self.dealerID},\nType: {self.type},\nYear: {self.year}")


class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    def __init__(self, dealership_, name_, purchase_, review_, purchase_date_, car_make_, car_year_, id_, sentiment_,car_model_):
        self.dealership = dealership_
        self.name = name_
        self.purchase = purchase_
        self.review = review_
        self.purchase_date = purchase_date_
        self.car_model = car_model_
        self.car_make = car_make_
        self.car_year = car_year_
        self.id = id_
        self.sentiment = sentiment_
    


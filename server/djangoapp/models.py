from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.TextField(),
    description = models.TextField(),
    def __str__(self):
        print(f"Name: {self.name}, \n Description: {self.description}")



# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE),
    name = models.TextField(),
    dealerID = models.IntegerField(),
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
    year = models.IntegerField(),
    def __str__(self):
        print(f"Make: {self.make},\nName: {self.name},\n\
            Dealer-ID: {self.dealerID},\nType: {self.type},\nYear: {self.year}")


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data

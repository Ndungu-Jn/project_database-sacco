from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    gender = models.CharField(max_length=11)
    weight = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.gender}"


    class Meta:
        db_table = 'customers'
       

class Deposits(models.Model):
    amount = models.IntegerField()
    status = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.customer.first_name} - {self.amount}"

    class Meta:
        db_table = 'deposits'
        






#run migrations
#python3  manage.py makemigrations
#python3 manage.py migrate
#python3 manage.py populate  -- for this populate is our own name.

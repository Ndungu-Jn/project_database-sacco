from django.shortcuts import render
from django.http import HttpResponse

from sacco.models import Customer, Deposits



# Create your views here.

def test(request):
    #save a customer
    # customer1 = Customer(first_name='Jaba', last_name='John', email='jj@gmial.com', dob='2000-11-24', gender='Male', weight='62')
    # customer1.save()

    # customer2 = Customer(first_name='Pesh', last_name='Emma', email='pe@gmial.com', dob='2000-05-14', gender='Female', weight='60')
    # customer2.save()


    customer_count = Customer.objects.count()

    #fetching one customer.
    customer1 = Customer.objects.get(id=1)
    print(customer1)
    deposit1 = Deposits(amount=1000, status=True, customer = customer1)
    deposit1.save()
    deposit2 = Deposits(amount=2000, status=True, customer = customer1)
    deposit2.save()

    deposit_count = Deposits.objects.count()

    return HttpResponse(f"Ok, Done, We have {customer_count} customers and {deposit_count} deposits")

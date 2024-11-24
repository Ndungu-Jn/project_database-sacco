from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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


def customers(request):
    data = Customer.objects.all().order_by('id').values() #ORM -- object relational matter select * from customers
    #pagination.
    paginator = Paginator(data, 15)
    page_number = request.GET.get('page', 1)
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage:
        paginated_data = paginator.page(1)

    return render(request, 'customers.html', {"data": paginated_data})

def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)#select * from customers where id=something
    customer.delete()
    return redirect('customers')


def customer_details(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    deposits = Deposits.objects.filter(customer_id=customer_id)
    return render(request, 'details.html', {"deposits": deposits, "customer": customer})


def add_customer(request):

    return render(request, 'customer_form.html')


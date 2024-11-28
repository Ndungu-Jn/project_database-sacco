from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Sum
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from sacco.app_forms import CustomerForm, DepositForm, LoginForm
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

@login_required
def customers(request):
    data = Customer.objects.all().order_by('-id').values() #ORM -- object relational matter select * from customers
    #pagination.
    paginator = Paginator(data, 15)
    page_number = request.GET.get('page', 1)
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage:
        paginated_data = paginator.page(1)

    return render(request, 'customers.html', {"data": paginated_data})

@login_required
@permission_required("sacco.delete_customer", raise_exception=True)
def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)#select * from customers where id=something
    customer.delete()
    messages.info(request, f"{customer.first_name} was deleted!")
    return redirect('customers')

@login_required
@permission_required("sacco.view_customer", raise_exception=True)
def customer_details(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    deposits = Deposits.objects.filter(customer_id=customer_id)
    total = Deposits.objects.filter(customer=customer).filter(status=True).aggregate(Sum('amount'))["amount__sum"]

    return render(request, 'details.html', {"deposits": deposits, "customer": customer, 'total': total})

@login_required
@permission_required("sacco.add_customer", raise_exception=True)
def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer {form.cleaned_data['first_name']} has been created!")
            return redirect('customers')
    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {'form':form})

@login_required
@permission_required("sacco.change_customer",raise_exception=True)
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES,  instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer {form.cleaned_data['first_name']} has been updated!")
            return redirect('customers')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_update_form.html', {'form':form})


@login_required
@permission_required("sacco.view_customer", raise_exception=True)
def search_customer(request):
    search_term = request.GET.get('search','').strip()
    data = Customer.objects.filter(Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term) | Q(email__icontains=search_term))
    # pagination.
    paginator = Paginator(data, 15)
    page_number = request.GET.get('page', 1)
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage:
        paginated_data = paginator.page(1)

    return render(request, 'search.html', {"data": paginated_data})

    #select * from customers where first _name LIKE '%noel%'
@login_required
@permission_required("sacco.add_deposit", raise_exception=True)
def deposit(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            depo = Deposits(amount=amount, status=True, customer=customer)
            depo.save()
            messages.success(request, 'Your deposit has been successfully saved')
            return redirect('customers')

    else:
        form = DepositForm()

    return render(request,'deposit_form.html', {"form":form, 'customer': customer} )

#logic for the login page.
def login_user(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login_form.html", {"form":form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)  #sessions -- what is stored in your database--server  cookies--data stored on the browser.
                return redirect('customers')
        messages.error(request, 'Invalid username or password')
        return render(request, "login_form.html", {"form":form})


@login_required
def signout_user(request):
    logout(request)
    return redirect('login')


#pip3 install django-crispy-forms
#pip3 install crispy-bootstrap5
#pip3 install Pillow  -- manipulate images.
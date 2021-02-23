from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .decorators import admin_only, allowed_users, unathenticated_user
from .filters import OrderFilter
from .forms import CustomerForm, OrderForm, RegistrationForm
from .models import *
from .signals import customer_profile

# Create your views here.

@unathenticated_user
def registerUser(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            #group = Group.objects.get(name="customer")
            #user.groups.add(group)
            """
            Customer.objects.create(
                user=user,
                name=user.username,
            )
            """
            messages.success(request, 'Account was created for '+username)
            return redirect("login")
    context = {
        'form':form
    }
    return render(request, 'register.html', context)

@unathenticated_user
def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password is incorrect!')

    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status="Delivered").count()
    orders_pending = orders.filter(status="Pending").count()
    print(f'orders: {orders}')
    context = {
        'orders':orders,
        'total_orders':total_orders,
        'orders_delivered':orders_delivered,
        'orders_pending':orders_pending
    }
    return render(request, 'user.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {
        'form':form
    }
    return render(request, 'account_settings.html', context)

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()

    context = {
        'orders':orders,
        'customers':customers,
        'total_orders':total_orders,
        'orders_delivered':orders_delivered,
        'orders_pending':orders_pending
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Products.objects.all()
    return render(request, 'products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'myFilter': myFilter
    }
    return render(request, 'customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {
        'form':form
    }
    return render(request, 'create_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_customer(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'create_customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'create_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {
        'item':order
    }
    return render(request, 'delete_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {
        'form':form
    }
    return render(request, 'create_customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/')
    context = {
        'item': customer
    }
    return render(request, 'delete_customer.html', context)


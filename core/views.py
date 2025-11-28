from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group


@login_required
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Assign role Worker to new accounts
            worker_group = Group.objects.get(name='Worker')
            user.groups.add(worker_group)

            login(request, user)  # auto login after registration
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

from .decorators import manager_required
from .models import Product, SupplierOrder, Shipment, Customer, Invoice, Stock

@manager_required
def manager_dashboard(request):
    context = {
        'product_count': Product.objects.count(),
        'supplier_order_count': SupplierOrder.objects.count(),
        'shipment_count': Shipment.objects.count(),
        'customer_count': Customer.objects.count(),
        'invoice_count': Invoice.objects.count(),
        'total_stock': sum(item.quantity for item in Stock.objects.all()),
    }
    return render(request, 'manager_dashboard.html', context)

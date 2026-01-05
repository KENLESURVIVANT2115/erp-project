from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib import messages
from django.core.exceptions import ValidationError

from .decorators import manager_required, worker_required
from .models import (
    Product,
    SupplierOrder,
    Shipment,
    ShipmentItem,
    Customer,
    Invoice,
    Stock
)


# =========================
# HOME
# =========================
@login_required
def home(request):
    return render(request, 'home.html')


# =========================
# REGISTER
# =========================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Assign Worker role by default
            worker_group = Group.objects.get(name='Worker')
            user.groups.add(worker_group)

            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# =========================
# MANAGER DASHBOARD
# =========================
@manager_required
def manager_dashboard(request):
    context = {
        'product_count': Product.objects.count(),
        'supplier_order_count': SupplierOrder.objects.count(),
        'shipment_count': Shipment.objects.count(),
        'customer_count': Customer.objects.count(),
        'invoice_count': Invoice.objects.count(),
        'total_stock': sum(stock.quantity for stock in Stock.objects.all()),
    }
    return render(request, 'manager_dashboard.html', context)


# =========================
# WORKER DASHBOARD
# =========================
@worker_required
def worker_dashboard(request):
    stocks = Stock.objects.select_related('product')
    shipments = Shipment.objects.prefetch_related('items', 'customer')

    return render(request, 'worker_dashboard.html', {
        'stocks': stocks,
        'shipments': shipments,
    })



@worker_required
def create_shipment(request):
    products = Product.objects.all()
    customers = Customer.objects.all()

    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')

        try:
            quantity = int(quantity)
            product = Product.objects.get(id=product_id)
            customer = Customer.objects.get(id=customer_id)

            # Create shipment
            shipment = Shipment.objects.create(customer=customer)

            # Create shipment item
            ShipmentItem.objects.create(
                shipment=shipment,
                product=product,
                quantity=quantity
            )

            messages.success(request, 'Shipment created successfully.')
            return redirect('worker_dashboard')

        except ValidationError as e:
            messages.error(request, e.message)
        except Exception:
            messages.error(request, 'Unexpected error while creating shipment.')

    return render(request, 'create_shipment.html', {
        'products': products,
        'customers': customers,
    })

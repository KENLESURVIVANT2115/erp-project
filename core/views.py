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

from .decorators import worker_required
from .models import Stock, Product, Shipment, ShipmentItem, Customer

@worker_required
def worker_dashboard(request):
    stocks = Stock.objects.select_related('product')
    shipments = Shipment.objects.all()

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
        quantity = int(request.POST.get('quantity'))

        product = Product.objects.get(id=product_id)
        customer = Customer.objects.get(id=customer_id)

        # stock check
        stock = Stock.objects.get(product=product)
        if stock.quantity < quantity:
            return render(request, 'shipment_error.html', {
                'message': 'Not enough stock!'
            })

        # create shipment
        shipment = Shipment.objects.create(customer=customer)
        ShipmentItem.objects.create(
            shipment=shipment,
            product=product,
            quantity=quantity
        )

        return redirect('worker_dashboard')

    return render(request, 'create_shipment.html', {
        'products': products,
        'customers': customers,
    })

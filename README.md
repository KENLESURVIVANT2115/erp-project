# Mini ERP – Logistics System

## Features
- Stock management
- Supplier orders
- Shipments
- Role-based access (Manager / Worker)
- Warehouse panel

## Tech stack
- Python
- Django
- SQLite
- Bootstrap

## Run locally
```bash
git clone ...
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

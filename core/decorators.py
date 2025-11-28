from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def role_required(role_name):
    def decorator(view_function):
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name=role_name).exists():
                return view_function(request, *args, **kwargs)
            return redirect('home')  # brak uprawnień → strona główna
        return wrapper
    return decorator

admin_required = role_required('Admin')
manager_required = role_required('Manager')
worker_required = role_required('Worker')

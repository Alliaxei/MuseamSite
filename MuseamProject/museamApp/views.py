from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from .models import Exhibit

def login_page(request):

    if request.method == 'POST':
        print("Форма отправлена методом POST")
        print(f"Username: {request.POST.get('username')}")
        print(f"Password: {request.POST.get('password')}")
        password = "admin"
        hashed_password = make_password(password)
        print(hashed_password)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            print("User существует")
            login(request, user)
            if user.is_admin:
                return redirect('adminPage')
    else:
        print("Метод GET")
    return render(request, 'login.html')


def admin_page(request):
    return render(request, 'resAdminPanel.html')

def exhibit_list(request):
    exhibits = Exhibit.objects.all()
    return render(request, "resAdminPanel.html", {'exhibits': exhibits})

def delete_exhibit(request, exhibit_id):
    exhibit = Exhibit.objects.get(id=exhibit_id)
    exhibit.delete()  # Удаляем объект из базы данных
    return redirect('exhibit_list')


def add_exhibits(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        author = request.POST.get('author')
        origin = request.POST.get('origin')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        history = request.POST.get('history')
        condition = request.POST.get('condition')

        Exhibit.objects.create(
            name=name,
            author=author,
            origin=origin,
            quantity=quantity,
            category=category,
            history=history,
            condition=condition,
        )
        return redirect('exhibit_list')

    exhibits = Exhibit.objects.all()
    return render(request, 'resAdminPanel.html',
                  {'exhibits': exhibits})

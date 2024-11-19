from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .forms import UserForm, ExhibitForm, HallForm
from .models import Exhibit, User, Hall, Report


def login_page(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('adminPage')
            else:
                return redirect('employeePage')
        else:
            error_message = "Неправильный логин или пароль"

    return render(request, 'login.html', {'error_message': error_message})
def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginPage')
def admin_page(request):
    employees = User.objects.filter(is_staff=False)
    exhibits = Exhibit.objects.all()
    halls = Hall.objects.all()
    context = {'employees': employees,
               'exhibits': exhibits,
               'halls': halls,
               'reports': Report.objects.all()}
    return render(request, 'resAdminPanel.html', context)
def employee_page(request):
    exhibits = Exhibit.objects.all()
    halls = Hall.objects.all()
    reports = Report.objects.all()
    context = {'exhibits': exhibits,
               'halls': halls,
               'reports': reports}
    return render(request, 'employeePanel.html', context)
def exhibit_list(request):
    exhibits = Exhibit.objects.all()
    return render(request, "resAdminPanel.html", {'exhibits': exhibits})
def delete_exhibit(request, exhibit_id):
    if request.method == 'POST':
        try:
            exhibit = Exhibit.objects.get(id=exhibit_id)
            exhibit.delete()
            exhibits = Exhibit.objects.all()
            exhibit_table_html = render_to_string('exhibit_table_body.html', {'exhibits': exhibits})
            return JsonResponse({'success': True, 'exhibit_table_html': exhibit_table_html})
        except Exhibit.DoesNotExist:
            print("Экспонат не найден")
            return JsonResponse({"error": "Сотрудник не найден"})
def edit_exhibit(request, exhibit_id):
    if request.method == 'POST':
        if not exhibit_id:
            return JsonResponse({"error": "exhibit_id не существует"}, status=400)
        exhibit = get_object_or_404(Exhibit, id=exhibit_id)
        exhibit.name = request.POST.get('name')
        exhibit.author = request.POST.get('author')
        exhibit.origin = request.POST.get('origin')
        exhibit.quantity = request.POST.get('quantity')
        exhibit.category = request.POST.get('category')
        exhibit.history = request.POST.get('history')
        exhibit.condition = request.POST.get('condition')
        hall_id = request.POST.get('hall')
        if not hall_id:
            return JsonResponse({"error": "hall_id не указан"}, status=400)
        exhibit.hall =get_object_or_404(Hall, id=hall_id)
        exhibit.save()

        exhibits = Exhibit.objects.all()
        exhibit_table_html = render_to_string('exhibit_table_body.html', {'exhibits': exhibits})
        return JsonResponse({'success': True, 'exhibit_table_html': exhibit_table_html})
    return JsonResponse({"error": "Некорректный метод запроса"}, status=400)
def get_exhibit_data(request, exhibit_id):
    if request.method == 'GET':
        print(f"Получен запрос на данные о выставке с ID: {exhibit_id}")

        try:
            exhibit = get_object_or_404(Exhibit, id=exhibit_id)
            print(f"Выставка найдена: {exhibit.name} (ID: {exhibit.id})")
        except Exception as e:
            print(f"Ошибка при попытке найти выставку с ID {exhibit_id}: {e}")
            return JsonResponse({'error': 'Exhibit not found'}, status=404)

        try:
            exhibit_data = {
                'id': exhibit.id,
                'name': exhibit.name,
                'author': exhibit.author,
                'origin': exhibit.origin,
                'quantity': exhibit.quantity,
                'category': exhibit.category,
                'history': exhibit.history,
                'condition': exhibit.condition,
                'hall': exhibit.hall.number,
            }
            print(f"Данные для выставки с ID {exhibit_id} успешно подготовлены: {exhibit_data}")
            return JsonResponse(exhibit_data)
        except Exception as e:
            print(f"Ошибка при подготовке данных для выставки с ID {exhibit_id}: {e}")
            return JsonResponse({'error': 'Error preparing exhibit data'}, status=500)

    print(f"Некорректный метод запроса: {request.method}")
    return JsonResponse({'error': 'Invalid request method'}, status=405)
def add_exhibits(request):
    if request.method == 'POST':
        form = ExhibitForm(request.POST)
        if form.is_valid():
            form.save()
            exhibits = Exhibit.objects.all()
            exhibit_table_html = render_to_string('exhibit_table_body.html',{'exhibits': exhibits})
            return JsonResponse({'success': True, 'exhibit_table_html': exhibit_table_html})
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = ExhibitForm()
        # Выполняется при открытии страницы
        exhibits = Exhibit.objects.all()
        return render(request, 'resAdminPanel.html',{'exhibits': exhibits, 'form': form})
def add_hall(request):
    if request.method == 'POST':
        form = HallForm(request.POST)
        if form.is_valid():
            form.save()
            halls = Hall.objects.all()
            hall_table_html = render_to_string('hall_table_body.html', {'halls': halls})
            return JsonResponse({'success': True, 'hall_table_html': hall_table_html})
        else:
            print(form.errors)
            return JsonResponse({"errors": form.errors}, status=400)
def delete_hall(request, hall_id):
    if request.method == 'POST':
        try:
            hall = Hall.objects.get(id=hall_id)
            print(f"Удаление зала: {hall}")  # Отладка
            hall.delete()
            halls = Hall.objects.all()
            hall_table_html = render_to_string('hall_table_body.html', {'halls': halls})
            return JsonResponse({'success': True, 'hall_table_html': hall_table_html})
        except Hall.DoesNotExist:
            return JsonResponse({"error": "Зал не найден"}, status=404)
        except TypeError as e:
            return JsonResponse({"error": f"Ошибка на сервере {e}"}, status=500)
    return JsonResponse({"error": "Некорректный запрос"}, status=400)
def edit_hall(request, hall_id):
    if request.method == 'POST':
        if not hall_id:
            return JsonResponse({"error": "hall_id не существует"} , status=400)
        hall = get_object_or_404(Hall, id=hall_id)
        hall.number = request.POST.get('number')
        hall.thematic = request.POST.get('thematic')
        hall.save()

        halls = Hall.objects.all()
        hall_table_html = render_to_string('hall_table_body.html', {'halls': halls})
        return JsonResponse({"success": True, "hall_table_html": hall_table_html})
    return JsonResponse({"error": "Некорректный метод запроса"}, status=400)
def get_hall_data(request, hall_id):
    if request.method != 'GET':
        return JsonResponse({"error": "Invalid request method"}, status=400)
    try:
        hall = get_object_or_404(Hall, id=hall_id)
        hall_data = {
            'id': hall.id,
            'number': hall.number,
            'thematic': hall.thematic,
        }
        return JsonResponse(hall_data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
def add_employee(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            employees = User.objects.filter(is_staff=False)
            employee_table_html = render_to_string('employee_table_body.html', {'employees': employees})
            return JsonResponse({"success": True, "table_html": employee_table_html})
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = UserForm()
        return render(request, 'resAdminPanel.html', {'form': form})
def delete_employee(request, employee_id):
    if request.method == 'POST':
        try:
            employee = User.objects.get(id=employee_id)
            employee.delete()

            employees = User.objects.filter(is_staff=False)
            employee_table_html = render_to_string('employee_table_body.html', {'employees': employees})
            return JsonResponse({"success": True, "table_html": employee_table_html})
        except User.DoesNotExist:
            print("Не удалось запустить")
            return JsonResponse({"error": "Сотрудник не найден"})
def edit_employee(request, employee_id):
    if request.method == "POST":
        if not employee_id:
            return JsonResponse({"error": "employee_id не существует"} , status=400)
        employee = get_object_or_404(User, id=employee_id)
        employee.name= request.POST.get('name')
        employee.email= request.POST.get('email')
        employee.login= request.POST.get('login')
        employee.save()

        employees = User.objects.filter(is_staff=False)
        employee_table_html = render_to_string('employee_table_body.html', {'employees': employees})
        return JsonResponse({"success": True, "table_html": employee_table_html})
    return JsonResponse({"error": "Некорректный метод запроса"}, status=400)
def get_employee_data(request, employee_id):
    if request.method == 'GET':
        try:
            employee = get_object_or_404(User, id=employee_id)
            employee_data = {
                'id': employee.id,
                'name': employee.name,
                'login': employee.login,
                'email': employee.email,
                'success': True,
            }
            return JsonResponse(employee_data)
        except Exception as e:
            return JsonResponse({'error': 'Employee not found or other error occurred'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def generate_hall_report(request, hall_id):
    if request.method == "POST":
        user = request.user
        hall = get_object_or_404(Hall, id=hall_id)
        exhibits = hall.exhibits.all()
        description = request.POST.get('description')

        if not description:
            return JsonResponse({"error": "Описание отчёта не может быть пустым"}, status=400)

        report_data = {
            "hall": hall.number,
            "theme": hall.thematic,
            "exhibits": [
                {"name": exhibit.name, "author": exhibit.author, "condition": exhibit.condition}
                for exhibit in exhibits
            ],
        }
        report = save_report_to_db(
            report_type='by_hall',
            description=description,
            user=user,
        )
        return JsonResponse({"success": True, "report_id": report.id})
def generate_theme_report(request, theme):
    if request.method == 'POST':
        user = request.user
        description = request.POST.get('description')

        if not description:
            return JsonResponse({"error": "Описание отчёта не может быть пустым"}, status=400)

        exhibits = Exhibit.objects.filter(category=theme)
        report_data = {
            "theme": theme,
            "exhibits": [
                {"name": exhibit.name, "author": exhibit.author, "condition": exhibit.condition}
                for exhibit in exhibits
            ],
        }

        report = save_report_to_db(
            report_type="by_theme",
            description=description,
            user=user
        )

        return JsonResponse({"success": True, "report_id": report.id})
    return JsonResponse({"error": "Invalid request method"}, status=400)
def generate_count_by_theme_report(request, theme):
    if request.method == 'POST':
        user = request.user
        description = request.POST.get('description')

        if not description:
            return JsonResponse({"error": "Описание отчёта не может быть пустым"}, status=400)

        count = Exhibit.objects.filter(category=theme).count()

        report = save_report_to_db(
            report_type="count_by_theme",
            description=description,
            user=user
        )

        return JsonResponse({"success": True, "report_id": report.id, "count": count})
    return JsonResponse({"error": "Invalid request method"}, status=400)
def generate_restoration_report(request):
    if request.method == 'POST':
        user = request.user
        description = request.POST.get('description')

        if not description:
            return JsonResponse({"error": "Описание отчёта не может быть пустым"}, status=400)

        exhibits = Exhibit.objects.filter(condition="restoration_required")
        report_data = {
            "exhibits": [
                {"name": exhibit.name, "author": exhibit.author, "history": exhibit.history}
                for exhibit in exhibits
            ],
        }

        report = save_report_to_db(
            report_type="restoration",
            description=description,
            user=user
        )

        return JsonResponse({"success": True, "report_id": report.id})
    return JsonResponse({"error": "Invalid request method"}, status=400)
def save_report_to_db(report_type, description, user):
    report = Report.objects.create(report_type=report_type, description=description, generated_by=user)
    return report
def create_report(request):
    if request.method == "POST":
        report_type = request.POST.get('report_type')
        description = request.POST.get('description')

        if not description:
            return JsonResponse({"error": "Описание отчёта обязательно"}, status=400)
        if not report_type:
            return JsonResponse({"error": "Тип отчёта не выбран"}, status=400)

        if report_type == "by_hall":
            hall_id = request.POST.get('hall_id')
            response = generate_hall_report(request, hall_id)
        elif report_type == "by_theme":
            theme = request.POST.get('theme')
            response = generate_theme_report(request, theme)
        elif report_type == "count_by_theme":
            theme = request.POST.get('theme')
            response = generate_count_by_theme_report(request, theme)
        elif report_type == "restoration":
            response = generate_restoration_report(request)
        else:
            return JsonResponse({"error": "Некорректный тип отчёта"}, status=400)

        # После успешного выполнения конкретного отчёта обновляем таблицу
        if response.status_code == 200:
            reports = Report.objects.all()
            report_table_html = render_to_string('report_table_body_employee.html', {'reports': reports})
            return JsonResponse({"success": True, "report_table_html": report_table_html})
        else:
            return response

    return JsonResponse({"error": "Неверный метод запроса"}, status=405)
def delete_report(request, report_id):
    if request.method == "POST":
        try:
            report = Report.objects.get(id=report_id)
            report.delete()

            reports = Report.objects.all()
            report_table_html = render_to_string('report_table_body.html', {'reports': reports})
            return JsonResponse({"success": True, "report_table_html": report_table_html})
        except Report.DoesNotExist:
            print("Не удалось запустить")
            return JsonResponse({"error": "Отчёт не найден"})

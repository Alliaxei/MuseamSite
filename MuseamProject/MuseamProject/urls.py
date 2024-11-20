from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

from museamApp import views
from museamApp.views import admin_page, login_page, add_hall, exhibit_list, delete_exhibit, add_exhibits, \
    logout_page, add_employee, delete_employee, delete_hall, employee_page, edit_hall, get_hall_data, edit_exhibit, \
    get_exhibit_data, edit_employee, get_employee_data, create_report, delete_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('loginPage')),
    path('loginPage/', login_page, name='loginPage'),
    path('adminPage/', admin_page, name='adminPage'),
    path('employeePage/', employee_page, name='employeePage'),
    #Не уверен насчет exhibition
    path('exhibits/', exhibit_list, name='exhibit_list'),
    path('deleteExhibit/<int:exhibit_id>/', delete_exhibit, name='deleteExhibit'),
    path('editExhibition/<int:exhibit_id>/', edit_exhibit, name='editExhibit'),
    path('getExhibitData/<int:exhibit_id>/', get_exhibit_data, name='getExhibitData'),
    path('deleteHall/<int:hall_id>/', delete_hall, name='deleteHall'),
    path('add_exhibits/', add_exhibits,name='add_exhibits'),
    path('logout/', logout_page, name='logout'),
    path('addHall/', add_hall, name='addHall'),
    path('editHall/<int:hall_id>/', edit_hall, name='editHall'),
    path('getHallData/<int:hall_id>/', get_hall_data, name='getHallData'),
    path('addEmployee/', add_employee, name='addEmployee'),
    path('delete_employee/<int:employee_id>/', delete_employee, name='deleteEmployee'),
    path('editEmployee/<int:employee_id>/', edit_employee, name='editEmployee'),
    path('getEmployeeData/<int:employee_id>/', get_employee_data, name='getEmployeeData'),
    path('createReport/', create_report, name='createReport'),
    path('deleteReport/<int:report_id>/', delete_report, name='deleteReport'),
]

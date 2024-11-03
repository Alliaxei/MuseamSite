from django.contrib import admin
from django.urls import path

from museamApp import views
from museamApp.views import admin_page, login_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_page, name='loginPage'),
    path('adminPage/', admin_page, name='adminPage'),
    #Не уверен насчет exhibition
    path('exhibits/', views.exhibit_list, name='exhibit_list'),
    path('delete_exhibit/<int:id>', views.delete_exhibit, name='delete_exhibit'),
    path('add_exhibits/', views.add_exhibits,name='add_exhibits')
]

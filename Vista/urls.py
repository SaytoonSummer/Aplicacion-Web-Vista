"""
URL configuration for Vista project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from App.views import index, login, contact, inventory, input, support, update, delete, stakeholders, report, inputsh, updatesh, deletesh, user, ventas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('contact/', contact, name='contact'),
    path('inventory/', inventory, name='inventory'),
    path('input/', input, name='input'),
    path('support/', support, name='support'),
    path('stakeholders/', stakeholders, name='stakeholders'),
    path('report/', report, name='report'),
    path('update/<int:producto_id>/', update, name='update'),
    path('delete/<int:producto_id>/', delete, name='delete'),
    path('inputsh/', inputsh, name='inputsh'),
    path('updatesh/<int:proveedor_id>/', updatesh, name='updatesh'),
    path('deletesh/<int:proveedor_id>/', deletesh, name='deletesh'),
    path('user/', user, name='user'),
    path('ventas/', ventas, name='ventas'),
]

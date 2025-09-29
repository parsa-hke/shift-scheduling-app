from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employees/', views.manage_employees, name='manage_employees'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('locations/', views.manage_locations, name='manage_locations'),
    path('locations/add/', views.add_location, name='add_location'),
    path('holidays/', views.manage_holidays, name='manage_holidays'),
    path('holidays/delete/<int:holiday_id>/', views.delete_holiday, name='delete_holiday'),
    path('off-days/', views.manage_off_days, name='manage_off_days'),
    path('off-days/delete/<int:off_day_id>/', views.delete_off_day, name='delete_off_day'),
    path('generate/', views.generate_schedule, name='generate_schedule'),
    path('schedule/', views.view_schedule, name='view_schedule'),
    path('schedule/<int:month>/<int:year>/', views.view_schedule, name='view_schedule'),
    path('export/<int:month>/<int:year>/', views.export_schedule, name='export_schedule'),
]
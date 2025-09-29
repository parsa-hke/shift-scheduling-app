from django.contrib import admin
from .models import Employee, Location, Holiday, EmployeeOffDay, Schedule


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'phone', 'is_active', 'created_at']
    list_filter = ['gender', 'is_active', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_editable = ['is_active']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'mall_name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'mall_name', 'address']
    list_editable = ['is_active']


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'is_recurring']
    list_filter = ['is_recurring', 'date']
    search_fields = ['name']
    date_hierarchy = 'date'


@admin.register(EmployeeOffDay)
class EmployeeOffDayAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'reason']
    list_filter = ['date', 'employee']
    search_fields = ['employee__name', 'reason']
    date_hierarchy = 'date'


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['employee', 'location', 'date', 'shift', 'created_at']
    list_filter = ['shift', 'date', 'location', 'created_at']
    search_fields = ['employee__name', 'location__name']
    date_hierarchy = 'date'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employee', 'location')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Employee, Location, Holiday, EmployeeOffDay, Schedule
from .forms import (
    EmployeeForm, LocationForm, HolidayForm, OffDayForm,
    ScheduleGenerationForm
)
from .scheduler import ScheduleGenerator
import calendar
from datetime import date


def dashboard(request):
    """Main dashboard view"""
    context = {
        'total_employees': Employee.objects.filter(is_active=True).count(),
        'total_locations': Location.objects.filter(is_active=True).count(),
        'recent_schedules': Schedule.objects.select_related('employee', 'location').order_by('-created_at')[:5],
    }
    return render(request, 'scheduling/dashboard.html', context)


def manage_employees(request):
    """Manage employees view"""
    employees = Employee.objects.filter(is_active=True).order_by('name')
    return render(request, 'scheduling/manage_employees.html', {
        'employees': employees
    })


def add_employee(request):
    """Add single employee"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('manage_employees')
    else:
        form = EmployeeForm()

    return render(request, 'scheduling/add_employee.html', {'form': form})


def edit_employee(request, employee_id):
    """Edit employee"""
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('manage_employees')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'scheduling/edit_employee.html', {'form': form, 'employee': employee})


@require_http_methods(["POST"])
def delete_employee(request, employee_id):
    """Delete employee (soft delete)"""
    employee = get_object_or_404(Employee, id=employee_id)
    employee.is_active = False
    employee.save()
    messages.success(request, f'{employee.name} has been deactivated!')
    return redirect('manage_employees')


def manage_locations(request):
    """Manage locations view"""
    locations = Location.objects.filter(is_active=True).order_by('name')
    return render(request, 'scheduling/manage_locations.html', {
        'locations': locations
    })


def add_location(request):
    """Add single location"""
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location added successfully!')
            return redirect('manage_locations')
    else:
        form = LocationForm()

    return render(request, 'scheduling/add_location.html', {'form': form})


def edit_location(request, location_id):
    """Edit location"""
    location = get_object_or_404(Location, id=location_id)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location updated successfully!')
            return redirect('manage_locations')
    else:
        form = LocationForm(instance=location)

    return render(request, 'scheduling/edit_location.html', {'form': form, 'location': location})


@require_http_methods(["POST"])
def delete_location(request, location_id):
    """Delete location (soft delete)"""
    location = get_object_or_404(Location, id=location_id)
    location.is_active = False
    location.save()
    messages.success(request, f'{location.name} has been deactivated!')
    return redirect('manage_locations')


def manage_holidays(request):
    """Manage holidays"""
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Holiday added successfully!')
            return redirect('manage_holidays')
    else:
        form = HolidayForm()

    holidays = Holiday.objects.all().order_by('date')
    return render(request, 'scheduling/manage_holidays.html', {
        'form': form,
        'holidays': holidays
    })


def edit_holiday(request, holiday_id):
    """Edit holiday"""
    holiday = get_object_or_404(Holiday, id=holiday_id)
    if request.method == 'POST':
        form = HolidayForm(request.POST, instance=holiday)
        if form.is_valid():
            form.save()
            messages.success(request, 'Holiday updated successfully!')
            return redirect('manage_holidays')
    else:
        form = HolidayForm(instance=holiday)

    return render(request, 'scheduling/edit_location.html', {'form': form, 'holiday': holiday})


def manage_off_days(request):
    """Manage employee off days"""
    if request.method == 'POST':
        form = OffDayForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Off day added successfully!')
            return redirect('manage_off_days')
    else:
        form = OffDayForm()

    off_days = EmployeeOffDay.objects.select_related('employee').order_by('date')
    return render(request, 'scheduling/manage_off_days.html', {
        'form': form,
        'off_days': off_days
    })


def edit_off_day(request, off_day_id):
    """Edit off day"""
    off_day = get_object_or_404(EmployeeOffDay, id=off_day_id)
    if request.method == 'POST':
        form = OffDayForm(request.POST, instance=off_day)
        if form.is_valid():
            form.save()
            messages.success(request, 'Off day updated successfully!')
            return redirect('manage_off_days')
    else:
        form = OffDayForm(instance=off_day)

    return render(request, 'scheduling/edit_off_day.html', {'form': form, 'off_day': off_day})


def generate_schedule(request):
    """Generate monthly schedule"""
    if request.method == 'POST':
        form = ScheduleGenerationForm(request.POST)
        if form.is_valid():
            month = int(form.cleaned_data['month'])
            year = int(form.cleaned_data['year'])
            locations = form.cleaned_data['locations']

            # Clear existing schedules for this month
            Schedule.objects.filter(
                date__month=month,
                date__year=year
            ).delete()

            # Generate new schedule
            generator = ScheduleGenerator(month, year, locations)
            try:
                schedules_created = generator.generate()
                messages.success(request, f'Schedule generated successfully! {schedules_created} shifts assigned.')
                return redirect('view_schedule', month=month, year=year)
            except Exception as e:
                messages.error(request, f'Error generating schedule: {str(e)}')
    else:
        form = ScheduleGenerationForm()

    return render(request, 'scheduling/generate_schedule.html', {'form': form})


def view_schedule(request, month=None, year=None):
    """View generated schedule"""
    if month is None:
        month = date.today().month
    if year is None:
        year = date.today().year

    schedules = Schedule.objects.filter(
        date__month=month,
        date__year=year
    ).select_related('employee', 'location').order_by('date', 'shift')

    month_name = calendar.month_name[month]

    return render(request, 'scheduling/view_schedule.html', {
        'schedules': schedules,
        'month': month,
        'year': year,
        'month_name': month_name
    })


def export_schedule(request, month, year):
    """Export schedule to Excel"""
    generator = ScheduleGenerator(month, year, [])
    excel_file = generator.export_to_excel()

    response = HttpResponse(
        excel_file,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="schedule_{calendar.month_name[month]}_{year}.xlsx"'

    return response


@require_http_methods(["POST"])
def delete_holiday(request, holiday_id):
    """Delete holiday"""
    holiday = get_object_or_404(Holiday, id=holiday_id)
    holiday.delete()
    messages.success(request, 'Holiday deleted successfully!')
    return redirect('manage_holidays')


@require_http_methods(["POST"])
def delete_off_day(request, off_day_id):
    """Delete off day"""
    off_day = get_object_or_404(EmployeeOffDay, id=off_day_id)
    off_day.delete()
    messages.success(request, 'Off day deleted successfully!')
    return redirect('manage_off_days')

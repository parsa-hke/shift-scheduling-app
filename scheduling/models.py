from django.db import models
from django.core.validators import RegexValidator


class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        blank=True
    )
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    mall_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.mall_name}" if self.mall_name else self.name

    class Meta:
        ordering = ['name']


class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    is_recurring = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.date}"

    class Meta:
        ordering = ['date']


class EmployeeOffDay(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.employee.name} - {self.date}"

    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['date']


class Schedule(models.Model):
    SHIFT_CHOICES = [
        ('10AM-7PM', '10:00 AM - 7:00 PM'),
        ('1PM-10PM', '1:00 PM - 10:00 PM'),
        ('3PM-12AM', '3:00 PM - 12:00 AM'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateField()
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.location.name} - {self.date} - {self.shift}"

    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['date', 'shift']

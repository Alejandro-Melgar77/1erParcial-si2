# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Administrador'),
        ('resident', 'Residente'),
        ('security', 'Seguridad'),
        ('maintenance', 'Mantenimiento'),
    ]
    dni = models.CharField(max_length=20, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='resident')

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Unit(models.Model):
    number = models.CharField(max_length=10, unique=True)
    floor = models.IntegerField()
    residents = models.ManyToManyField(User, related_name='units', blank=True)

    def __str__(self):
        return f"Unit {self.number}"


class CommonArea(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    available_from = models.TimeField()
    available_to = models.TimeField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(CommonArea, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.area.name} - {self.date}"


class Expense(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.unit.number} - {self.description}"


class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=10, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.owner.username} - {self.plate_number}"


class Visitor(models.Model):
    name = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    visited_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    purpose = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.visited_unit.number}"


class FaceRecord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_encoding = models.TextField()  # JSON string of face encoding
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Face of {self.user.username}"


class SecurityEvent(models.Model):
    EVENT_TYPES = [
        ('face_recognition', 'Face Recognition'),
        ('plate_recognition', 'Plate Recognition'),
        ('unauthorized_access', 'Unauthorized Access'),
    ]
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='security_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.event_type} - {self.timestamp}"
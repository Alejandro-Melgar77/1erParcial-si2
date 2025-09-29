from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Usamos la clase base UserAdmin pero sobre tu modelo
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Campos que se mostrarán en la lista
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')
    
    # Campos que se pueden usar para buscar
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Campos agrupados por secciones en el formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # 👈 añadimos role
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),  # 👈 añadimos role al formulario de creación
    )

# Register your models here.

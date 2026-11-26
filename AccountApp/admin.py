from django.contrib import admin
from .models import User, Doctor, Patient, Specialty


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'last_name', 'first_name', 'phone', 'license_number', 'get_specialties')
    list_filter = ('specialties',)
    search_fields = ('username', 'last_name', 'first_name', 'license_number')
    filter_horizontal = ('specialties',)
    ordering = ('last_name', 'first_name')

    def get_specialties(self, obj):
        return ", ".join([s.name for s in obj.specialties.all()])
    get_specialties.short_description = "Spécialités"

    def get_readonly_fields(self, request, obj=None):
        """license_number ne peut pas être modifié après la création."""
        if obj:
            return ('license_number',)
        return ()


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'last_name', 'first_name', 'phone', 'national_id', 'birth_date')
    search_fields = ('username', 'last_name', 'first_name', 'national_id')
    ordering = ('last_name', 'first_name')

    def get_readonly_fields(self, request, obj=None):
        """national_id ne peut pas être modifié après la création."""
        if obj:
            return ('national_id',)
        return ()

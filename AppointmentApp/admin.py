from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'doctor', 'patient', 'appointment_date',
        'duration_minutes', 'status', 'created_at'
    )
    list_filter = ('status', 'doctor', 'patient', 'appointment_date')
    search_fields = (
        'doctor__last_name', 'doctor__first_name',
        'patient__last_name', 'patient__first_name',
        'reason'
    )
    ordering = ('appointment_date',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations principales', {
            'fields': ('doctor', 'patient', 'appointment_date', 'duration_minutes', 'status')
        }),
        ('Détails', {
            'fields': ('reason', 'prescription')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

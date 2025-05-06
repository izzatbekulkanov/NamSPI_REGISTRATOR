from django.contrib import admin
from .models import Section, SubService, AssignedService

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'online_available')
    list_filter = ('section', 'online_available')
    search_fields = ('name',)

@admin.register(AssignedService)
class AssignedServiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'assigned_at')
    list_filter = ('service__section',)
    search_fields = ('user__full_name', 'service__name')

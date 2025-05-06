from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OperatorProfile, DailyWorkWindow


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Admin ro'yxat jadvali ko'rinishi
    list_display = ('username', 'full_name', 'department_name', 'staff_position', 'academic_degree', 'is_staff')
    list_filter = ('department_name', 'staff_position', 'academic_degree', 'is_staff')
    search_fields = ('username', 'full_name', 'specialty', 'department_name', 'staff_position')

    # Ro'yxatdan tahrirlash uchun maydonlar
    fieldsets = UserAdmin.fieldsets + (
        ('Shaxsiy maʼlumotlar', {
            'fields': (
                'full_name', 'short_name', 'first_name_native',
                'second_name', 'third_name', 'image', 'gender', 'birth_date'
            )
        }),
        ('Bo‘lim va lavozim', {
            'fields': (
                'department_name', 'department_structure', 'department_locality',
                'staff_position', 'academic_degree', 'academic_rank'
            )
        }),
        ('Ishga oid maʼlumotlar', {
            'fields': (
                'employment_form', 'employment_staff',
                'employee_status', 'employee_type', 'specialty',
                'year_of_enter', 'employee_id_number'
            )
        }),
        ('Shartnomalar', {
            'fields': (
                'contract_number', 'contract_date',
                'decree_number', 'decree_date',
            )
        }),
        ('Texnik', {
            'fields': (
                'created_at', 'update_at', 'hash'
            )
        }),
    )

    # Foydalanuvchi yaratish formasi uchun
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Qo‘shimcha maʼlumotlar', {
            'fields': ('full_name', 'department_name', 'staff_position')
        }),
    )


@admin.register(OperatorProfile)
class OperatorProfileAdmin(admin.ModelAdmin):
    list_display = ('operator', 'level', 'total_served')
    list_filter = ('level',)
    search_fields = ('operator__full_name', 'operator__username')

@admin.register(DailyWorkWindow)
class DailyWorkWindowAdmin(admin.ModelAdmin):
    list_display = ('operator', 'date', 'display_window', 'is_leader_display')
    list_filter = ('date', 'is_leader')
    search_fields = ('operator__username', 'operator__full_name')
    ordering = ('-date',)
    autocomplete_fields = ('operator',)

    def display_window(self, obj):
        return obj.window_number if obj.window_number else "—"
    display_window.short_description = "Oyna raqami"

    def is_leader_display(self, obj):
        return "✅ Ha" if obj.is_leader else "—"
    is_leader_display.short_description = "Rahbar"
    is_leader_display.admin_order_field = 'is_leader'
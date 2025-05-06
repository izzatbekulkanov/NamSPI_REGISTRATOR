from django.contrib import admin
from .models import QueueTicket
from django.utils.html import format_html
from django.utils.timezone import localtime
from django.utils.timezone import localtime, is_naive, make_aware, get_current_timezone


@admin.register(QueueTicket)
class QueueTicketAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_number', 'service_name', 'section_name', 'status_colored',
        'result_display', 'served_by', 'created_at_local', 'started_at_local', 'ended_at_local',
        'get_duration_display',
    )
    list_filter = ('status', 'result', 'service__section', 'created_at', 'served_by')
    search_fields = ('ticket_number', 'service__name', 'service__section__name', 'served_by__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'started_at', 'ended_at', 'ticket_number')

    def service_name(self, obj):
        return obj.service.name
    service_name.short_description = "Xizmat"

    def section_name(self, obj):
        return obj.service.section.name
    section_name.short_description = "Bo‘lim"

    def status_colored(self, obj):
        color = {
            'waiting': 'gray',
            'serving': 'orange',
            'done': 'green'
        }.get(obj.status, 'black')
        return format_html(f"<b style='color:{color}'>{obj.get_status_display()}</b>")
    status_colored.short_description = "Holat"

    def result_display(self, obj):
        if obj.result == "completed":
            return format_html('<span style="color:limegreen;">Bajarildi</span>')
        elif obj.result == "rejected":
            return format_html('<span style="color:red;">Rad etildi</span>')
        return "-"
    result_display.short_description = "Natija"

    def _safe_localtime(self, dt):
        if dt:
            if is_naive(dt):
                dt = make_aware(dt, get_current_timezone())
            return localtime(dt).strftime("%H:%M:%S %d.%m.%Y")
        return "-"

    def created_at_local(self, obj):
        return self._safe_localtime(obj.created_at)
    created_at_local.short_description = "Chiqarilgan vaqt"

    def started_at_local(self, obj):
        return self._safe_localtime(obj.started_at)
    started_at_local.short_description = "Boshlangan vaqt"

    def ended_at_local(self, obj):
        return self._safe_localtime(obj.ended_at)
    ended_at_local.short_description = "Yakunlangan vaqt"

    def get_duration_display(self, obj):
        seconds = obj.get_duration()
        if seconds:
            minutes = int(seconds // 60)
            sec = int(seconds % 60)
            return f"{minutes} daqiqa {sec} soniya"
        return "-"
    get_duration_display.short_description = "Xizmat davomiyligi"
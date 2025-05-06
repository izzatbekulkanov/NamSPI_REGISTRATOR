from django.utils.timezone import now
from members.models import DailyWorkWindow, OperatorProfile
from queueing.models import QueueTicket


def global_user_context(request):
    if request.user.is_authenticated:
        today = now().date()

        try:
            work_window = DailyWorkWindow.objects.get(operator=request.user, date=today)
            has_window = True
            window_number = work_window.window_number
            is_leader = work_window.is_leader
        except DailyWorkWindow.DoesNotExist:
            has_window = False
            window_number = None
            is_leader = False

        today_count = QueueTicket.objects.filter(
            served_by=request.user,
            status='done',
            ended_at__date=today
        ).count()

        total_count = QueueTicket.objects.filter(
            served_by=request.user,
            status='done'
        ).count()

        profile, _ = OperatorProfile.objects.get_or_create(operator=request.user)
        level = profile.level or "Boshlovchi"

        level_icons = {
            "Boshlovchi": "🟢",
            "Oddiy": "⭐",
            "Yaxshi": "🌟",
            "Usta": "🔥",
            "VIP": "👑"
        }
        level_icon = level_icons.get(level, "🟢")

        return {
            'has_window': has_window,
            'window_number': window_number,
            'is_leader': is_leader,
            'today_count': today_count,
            'total_count': total_count,
            'level': level,
            'level_icon': level_icon,
            'today': today,
        }

    return {}

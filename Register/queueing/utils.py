from .models import QueueTicket
from datetime import date

def generate_ticket_number(category_code):
    today = date.today()
    count_today = QueueTicket.objects.filter(
        created_at__date=today,
        service__category__short_code=category_code
    ).count() + 1
    return f"{category_code}{count_today:02d}"

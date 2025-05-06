from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import QueueTicket
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=QueueTicket)
def notify_queue_created(sender, instance, created, **kwargs):
    if created and instance.status == 'waiting':
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "queue_group",
            {
                "type": "queue.update",
                "data": {
                    "ticket_number": instance.ticket_number,
                    "service": instance.service.name,
                    "created_at": instance.created_at.strftime('%H:%M:%S'),
                }
            }
        )

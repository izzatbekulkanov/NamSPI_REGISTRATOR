from django.urls import path
from .views import queueing_create_ticket_ajax, subservice_list_view, section_list_view, queue_display_view, \
    ajax_operator_serving_tickets

urlpatterns = [
    path('', section_list_view, name='queueing-section-list'),
    path('section/<int:section_id>/', subservice_list_view, name='queueing-subservice-list'),
    path('ticket/create/<int:subservice_id>/', queueing_create_ticket_ajax, name='queueing-create-ticket'),
    path('display/', queue_display_view, name='queue-display'),
    path('ajax/operator-waiting/', ajax_operator_serving_tickets, name='ajax-operator-waiting-tickets'),
]

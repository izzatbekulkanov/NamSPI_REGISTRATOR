from django.urls import path
from .views import service_dashboard, delete_section, delete_subservice, delete_assignment, operator_queue_view, \
    serve_ticket, complete_ticket, cancel_ticket, ajax_waiting_tickets, ajax_serving_ticket, ajax_done_tickets, \
    dashboard, set_daily_window, statistics_display_view

urlpatterns = [
    path('', dashboard, name='service-dashboard'),
    path('set-window/', set_daily_window, name='set-daily-window'),
    path('services/', service_dashboard, name='service-services'),
    path('delete-section/<int:pk>/', delete_section, name='delete-section'),
    path('delete-subservice/<int:pk>/', delete_subservice, name='delete-subservice'),
    path('delete-assignment/<int:pk>/', delete_assignment, name='delete-assignment'),
    path('operator-queue/', operator_queue_view, name='operator-queue'),
    path('ticket/serve/<int:ticket_id>/', serve_ticket, name='serve-ticket'),
    path('ticket/complete/<int:ticket_id>/', complete_ticket, name='complete-ticket'),
    path('ticket/cancel/<int:ticket_id>/', cancel_ticket, name='cancel-ticket'),
    path('ajax/waiting-tickets/', ajax_waiting_tickets, name='ajax-waiting-tickets'),
    path('ajax/serving-ticket/', ajax_serving_ticket, name='ajax-serving-ticket'),
    path("ajax/done-tickets/", ajax_done_tickets, name="ajax-done-tickets"),

    # ✅ yangi qo‘shilgan URL
    path('statistics/', statistics_display_view, name='statistics-display'),
]

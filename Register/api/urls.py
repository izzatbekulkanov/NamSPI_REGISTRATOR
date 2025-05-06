from django.urls import path
from . import views
from .views import CreateTicketAPI, TodayTicketSummaryAPI, ServingTicketListAPI

urlpatterns = [
    path('sections/', views.SectionListAPI.as_view(), name='api-sections'),
    path('sections/<int:pk>/subservices/', views.SubserviceListAPI.as_view(), name='api-subservices'),
    path('ticket/create/<int:subservice_id>/', CreateTicketAPI.as_view(), name='api-create-ticket'),
    path('tickets/today/', TodayTicketSummaryAPI.as_view(), name='api-today-tickets'),
    path('tickets/serving/', ServingTicketListAPI.as_view(), name='api-serving-tickets'),
]

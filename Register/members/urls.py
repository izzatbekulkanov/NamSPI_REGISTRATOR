from django.urls import path
from .views import CustomLoginView, staff_add, check_username, ResetPasswordView, DeleteStaffView, StaffListView, \
    AssignServiceView, BulkAssignSubServicesView, UnassignServiceView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('staff-add/', staff_add, name='staff-add'),
    path("check-username/", check_username, name="check-username"),
    path('list/', StaffListView.as_view(), name='staff-list'),
    path('staff/<int:pk>/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('staff/<int:pk>/delete/', DeleteStaffView.as_view(), name='delete-staff'),
    path('assign/', AssignServiceView.as_view(), name='assign-services'),
    path('assign/bulk/', BulkAssignSubServicesView.as_view(), name='bulk-assign-subservices'),
    path("unassign/<int:pk>/", UnassignServiceView.as_view(), name="unassign-subservice"),
]

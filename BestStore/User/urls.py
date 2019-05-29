from django.urls import path
from .views import user_dashboard, UpdateUserProfile, DeleteUserProfile, contact_us, change_password

urlpatterns = [
    path('dashboard/', user_dashboard, name='dashboard'),
    path('profile/delete/<int:pk>/', DeleteUserProfile.as_view(), name='delete_profile'),
    path('profile/update/<int:pk>/', UpdateUserProfile.as_view(success_url='/dashboard/'), name='update_profile'),
    path('contact/', contact_us, name='contact'),
    path('change_password/', change_password, name='change_password'),

]

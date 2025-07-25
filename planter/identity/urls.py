from django.urls import path
from .views import LoginView, LogoutView

app_name = 'identity'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

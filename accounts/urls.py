from django.urls import path
from .views import RegisterView
from .views import LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

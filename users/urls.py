from django.urls import path
from .views import RegistrationView, ActivateAccountView, UserListView, LoginView, LogoutView

urlpatterns = [
    #path('get-csrf-token/', CsrfTokenView.as_view(), name='get_csrf_token'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<str:link>/', ActivateAccountView.as_view(), name='activate'),
    path('users/', UserListView.as_view(), name='users'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]

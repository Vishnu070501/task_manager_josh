from django.urls import path
from .views import SignUpView, SigninView, FetchUsers, AccessTokenView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('users/', FetchUsers.as_view(), name='fetch_users'),
    path('token/refresh/', AccessTokenView.as_view(), name='token_refresh'),
] 
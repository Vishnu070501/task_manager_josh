from django.urls import path
from .views import SignUpView, SigninView, FetchUsers, AccessTokenView, AddPermissionToUser, RemovePermissionFromUser

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('fetch-users/', FetchUsers.as_view(), name='fetch_users'),
    path('token/refresh/', AccessTokenView.as_view(), name='token_refresh'),
    path('<int:user_id>/permissions/add/<str:permission_codename>/', AddPermissionToUser.as_view(), name='add_permission_to_user'),
    path('<int:user_id>/permissions/remove/<str:permission_codename>/', RemovePermissionFromUser.as_view(), name='remove_permission_from_user'),
] 
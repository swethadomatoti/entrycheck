from django.urls import path
from . import views
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
urlpatterns = [
    path('entries/', views.EntryView.as_view(), name='entry-list'),
    path('entries/<int:pk>/', views.EntryView.as_view(), name='entry-detail'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # POST email+password -> tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),      # POST refresh -> new access
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
]

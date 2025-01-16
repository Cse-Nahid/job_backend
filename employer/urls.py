from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployerRegistrationView,
    EmployerDashboardView,
    EmployerApplicationsView,
    EmployerProfileDetailView,
    EmployerProfileUpdateView,
    EmployerProfileViewSet,
    EmailVerificationView,
)

# Initialize the router for ViewSets
router = DefaultRouter()
router.register(r'profiles', EmployerProfileViewSet, basename='employer-profile')

urlpatterns = [
    # Authentication URLs
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', EmployerRegistrationView.as_view(), name='employer-register'),
    # Email Verification URL
    path('verify-email/<uidb64>/<token>/', EmailVerificationView.as_view(), name='email-verification'),
    # Dashboard URL
    path('dashboard/', EmployerDashboardView.as_view(), name='employer-dashboard'),

    # Applications URL
    path('applications/', EmployerApplicationsView.as_view(), name='employer-applications'),

    # Profile Detail and Update URLs
    path('profile/', EmployerProfileDetailView.as_view(), name='employer-profile-detail'),
    path('profile/edit/', EmployerProfileUpdateView.as_view(), name='employer-profile-update'),

    # Include router-generated URLs
    path('', include(router.urls)),


]

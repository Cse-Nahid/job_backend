from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import EmployerProfile
from .serializers import EmployerRegistrationSerializer, EmployerProfileSerializer
from jobs.models import Job
from jobs.serializers import JobSerializer
from applications.models import Application
from applications.serializers import ApplicationSerializer
from dj_rest_auth.views import LogoutView as RestAuthLogoutView
from django.contrib.auth import logout as django_logout

User = get_user_model()

class EmployerRegistrationView(APIView):
    """
    Handles Employer Registration with email verification
    """
    serializer_class = EmployerRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate token and encoded user ID for email verification
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Create verification link
            confirm_link = f"https://job-backend-1s1n.onrender.com/employer/verify-email/{uidb64}/{token}/"

            # Send email with confirmation link
            email_subject = "Verify Your Employer Account"
            email_body = render_to_string("employer_confirm_email.html", {
                "user": user,
                "confirm_link": confirm_link,
            })
            email = EmailMultiAlternatives(email_subject, "", to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response(
                {"message": "Registration successful. Check your email to verify your account."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    """
    Handles email verification and user activation
    """
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            # Check the token validity
            if default_token_generator.check_token(user, token):
                user.is_active = True  # Activate the user account
                user.save()
                return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)

            return Response({"error": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EmployerDashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'employerprofile'):
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        jobs = Job.objects.filter(employer=user)
        jobs_data = JobSerializer(jobs, many=True).data

        applications = Application.objects.filter(job__in=jobs)
        applications_data = ApplicationSerializer(applications, many=True).data

        return Response({
            'jobs': jobs_data,
            'applications': applications_data
        })


class EmployerApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employer_id = request.user.id
        jobs = Job.objects.filter(employer_id=employer_id)
        applications = Application.objects.filter(job__in=jobs)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class EmployerProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)

    def get(self, request):
        profile = self.get_object()
        serializer = EmployerProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = self.get_object()
        serializer = EmployerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        profile = self.get_object()
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployerProfileUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployerProfileSerializer

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)

    def put(self, request):
        profile = self.get_object()
        serializer = EmployerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerProfileViewSet(ModelViewSet):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer


class LogoutView(RestAuthLogoutView):
    def post(self, request, *args, **kwargs):
        django_logout(request)
        return Response({"detail": "Successfully logged out."})

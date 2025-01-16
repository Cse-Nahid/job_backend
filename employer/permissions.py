from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsEmployerOrReadOnly, IsEmployerUser

class JobPostView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerOrReadOnly]

    def get(self, request):
        # All users can view job posts
        return Response({"message": "Anyone can view this job post."})

    def post(self, request):
        # Only employers can create a job post
        return Response({"message": "Job post created."})


class EmployerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerUser]

    def get(self, request):
        return Response({"message": "Welcome to the employer dashboard!"})

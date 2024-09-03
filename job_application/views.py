from django.shortcuts import get_object_or_404
from jobseeker.models import Jobseeker
from employer.models import Employer
from job_post.models import JobPost
from job_application.models import JobApplication
from job_application.serializers import JobApplicationSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


from rest_framework.permissions import IsAuthenticatedOrReadOnly
from jobseeker.permissions import IsJobSeekerOrReadOnly, IsJobSeekerUser
from employer.permissions import IsEmployerOrReadOnly, IsEmployerUser
from .permissions import IsApplicantOrReadOnly
from rest_framework.permissions import IsAuthenticated

# to implement email sending functionality
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string



# list view for job applications
class JobApplicationListView(APIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsJobSeekerOrReadOnly, IsApplicantOrReadOnly]


    # to get all the applications
    def get(self, request, format = None):
        # format=None is used here to accept any types of data
        print('applicationList  --->> inside GET ')

        applications = JobApplication.objects.all()
        serializer = JobApplicationSerializer(applications, many = True)

        return Response(serializer.data)
    




# Apply view for job applications
class JobApplicationApplyView(APIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsJobSeekerOrReadOnly, IsApplicantOrReadOnly]

    # to add a job application
    def post(self, request, format = None):
        print('applicationList  --->> inside POST ')
        print('Received data:', request.data)

        serializer = JobApplicationSerializer(data = request.data)

        if serializer.is_valid():
            # Get the JobSeeker instance of the current user
            # job_seeker = Job_seeker.objects.get(user=request.user)

            # Retrieve job_post ID from query parameters
            job_seeker_id = request.query_params.get('job_seeker_id')
            job_seeker = get_object_or_404(Job_seeker, id = job_seeker_id)

            # Retrieve job_post ID from query parameters
            job_post_id = request.query_params.get('job_post_id')  

            if not job_post_id:
                return Response({'error': 'Job post ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            if not job_seeker_id:
                return Response({'error': 'Job seeker ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                # Fetch the job post object
                job_post = JobPost.objects.get(id=job_post_id)
            except JobPost.DoesNotExist:
                return Response({'error': 'Invalid job post ID'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the job seeker has already applied for this job post
            if JobApplication.objects.filter(job_seeker=job_seeker, job_post=job_post).exists():
                return Response({'error': 'You have already applied for this job post'}, status=status.HTTP_400_BAD_REQUEST)
        
            print('job_post_id:', job_post_id, 'job_post:', job_post)
            print('job_seeker:', job_seeker, 'user_type:', job_seeker.user.user_type)

             # Save the serializer with job_seeker and job_post
            serializer.save(job_seeker=job_seeker, job_post=job_post)


            # email sending implementation for applicant
            email_subject = 'Application successful.'
            email_body = render_to_string('applicant_email.html', {
                'job_seeker': job_seeker,
                'employer': job_post.employer,
                'job_post': job_post,
            })

            email = EmailMultiAlternatives(email_subject, '', to = [job_seeker.user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()


            # email sending implementation for employer
            email_subject = 'Application successfully received.'
            email_body = render_to_string('employer_email.html', {
                'job_seeker': job_seeker,
                'employer': job_post.employer,
                'job_post': job_post,
            })

            email = EmailMultiAlternatives(email_subject, '', to = [job_post.employer.user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()


            print('Validation errors:', serializer.errors)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# to check f the job_seeker is applied to a particular job post or not
class CheckJobApplicationView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsJobSeekerOrReadOnly, IsApplicantOrReadOnly]

    def get(self, request, format = None):
        # Retrieve job_post ID from query parameters
            job_seeker_id = request.query_params.get('job_seeker_id')
            job_seeker = get_object_or_404(Job_seeker, id = job_seeker_id)

            # Retrieve job_post ID from query parameters
            job_post_id = request.query_params.get('job_post_id')  

            if not job_post_id:
                return Response({'error': 'Job post ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            if not job_seeker_id:
                return Response({'error': 'Job seeker ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                # Fetch the job post object
                job_post = JobPost.objects.get(id=job_post_id)
            except JobPost.DoesNotExist:
                return Response({'error': 'Invalid job post ID'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the job seeker has already applied for this job post
            if JobApplication.objects.filter(job_seeker=job_seeker, job_post=job_post).exists():
                return Response({'message': 'Already applied for this job post'})
            else:
                return Response({'message': 'Not applied for this job post'})






# job post detail view set
class JobApplicationDetailView(APIView):
    serializer_class = JobApplicationSerializer 
    permission_classes = [IsAuthenticatedOrReadOnly, IsJobSeekerOrReadOnly, IsApplicantOrReadOnly]    


    # creating a custom function to find the post object in the get(), put() or in the delete() method
    def get_object(self, pk):
        try:
            return JobApplication.objects.get(pk = pk)
        except JobApplication.DoesNotExist:
            raise Http404



    # get a single post
    def get(self, request, pk, format = None):
        print('inside GET in application_detail')

        application = self.get_object(pk)
        serializer = JobApplicationSerializer(application)

        return Response(serializer.data)



    # to update a post data
    def put(self, request, pk, format = None):
        print('inside PUT in application_detail')
        # print('Received data:', request.data)

        application = self.get_object(pk)

        if application.job_seeker.user != request.user:
            return Response({'error': 'You are not allowed to edit this application'}, status=status.HTTP_403_FORBIDDEN)

        # application data ke edit & update korar jonno 'application' & request data ke die dite hobe
        serializer = JobApplicationSerializer(application, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        print('Validation errors:', serializer.errors)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



    # to delete a post data
    def delete(self, request, pk, format = None):
        print('inside DELETE in application_detail')

        application = self.get_object(pk)

        if application.job_seeker.user != request.user:
            return Response({'error': 'You are not allowed to delete this application'}, status=status.HTTP_403_FORBIDDEN)
        
        application.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)







# to get the job_posts filtered for a specific job_seeker
class JobApplicationForAJobSeekerAPIView(APIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsJobSeekerOrReadOnly, IsApplicantOrReadOnly]


    def get(self, request, format=None):
        # job_seeker = Job_seeker.objects.get(user=request.user)

        job_seeker_id = request.query_params.get('job_seeker_id')
        job_seeker = get_object_or_404(Job_seeker, id = job_seeker_id)

        applications = JobApplication.objects.filter(job_seeker=job_seeker)
        # creating serializer with application objects
        serializer = JobApplicationSerializer(applications, many=True)

        return Response(serializer.data)
    





# to get all the application for a specific job post
class JobApplicationsForJobPostAPIView(APIView):
    serializer_class = JobApplicationSerializer

    permission_classes = [IsAuthenticated, IsEmployerOrReadOnly]


    def get(self, request, format=None):
        employer_id = request.query_params.get('employer_id')
        employer = get_object_or_404(Employer, id = employer_id)

        job_post_id = request.query_params.get('job_post_id')
        print(employer_id, job_post_id)

        if not job_post_id:
            return Response({'error': 'Job post ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            job_post = JobPost.objects.get(id=job_post_id, employer=employer)
        except JobPost.DoesNotExist:
            return Response({'error': 'Invalid job post ID or you are not authorized to view this job post'}, status=status.HTTP_400_BAD_REQUEST)

        applications = JobApplication.objects.filter(job_post=job_post)
        serializer = JobApplicationSerializer(applications, many=True)

        return Response(serializer.data)
    

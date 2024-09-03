from django.shortcuts import get_object_or_404
from job_post.models import JobPost
from employer.models import Employer
from job_catagory.models import Category
from job_post.serializers import JobPostSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from employer.permissions import IsEmployerOrReadOnly, IsEmployerUser
from .permissions import IsOwnerOrReadOnly


    

class JobPostListView(APIView):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployerOrReadOnly, IsOwnerOrReadOnly]


    # to get all the posts
    def get(self, request, format = None):
        # format=None is used here to accept any types of data
        print('PostList  --->> inside GET ')

        posts = JobPost.objects.all()
        serializer = JobPostSerializer(posts, many = True)

        return Response(serializer.data)
    



class JobPostPublishView(APIView):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployerOrReadOnly, IsOwnerOrReadOnly]


    # to add a post
    def post(self, request, format = None):
        print('PostList  --->> inside POST ')
        print(request.data)

        serializer = JobPostSerializer(data = request.data)

        if serializer.is_valid():
            # Get the Employer instance of the current user
            # employer = Employer.objects.get(user=request.user)

            employer_id = request.query_params.get('employer_id')
            employer = get_object_or_404(Employer, id = employer_id)

            print('employer:', employer, 'user_type:', employer.user.user_type)

            serializer.save(employer=employer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




# job post detail view set
class JobPostDetailView(APIView):
    serializer_class = JobPostSerializer 

    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployerOrReadOnly, IsOwnerOrReadOnly]    


    # creating a custom function to find the post object in the get(), put() or in the delete() method
    def get_object(self, pk):
        try:
            return JobPost.objects.get(pk = pk)
        except JobPost.DoesNotExist:
            raise Http404



    # get a single post
    def get(self, request, pk, format = None):
        print('inside get in post_detail')

        post = self.get_object(pk)
        serializer = JobPostSerializer(post)

        return Response(serializer.data)



    # to update a post data
    def put(self, request, pk, format = None):
        print('inside put in post_detail')
        # print('Received data:', request.data)

        post = self.get_object(pk)

        # post data ke edit & update korar jonno 'post' & request data ke die dite hobe
        serializer = JobPostSerializer(post, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        print('Validation errors:', serializer.errors)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



    # to delete a post data
    def delete(self, request, pk, format = None):
        print('inside delete in post_detail')

        post = self.get_object(pk)
        post.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)






# to get the job_posts filtered for a specific employer
class JobPostForAnEmployerAPIView(APIView):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployerOrReadOnly, IsOwnerOrReadOnly]


    def get(self, request, format=None):
        # employer = Employer.objects.get(user=request.user)

        employer_id = request.query_params.get('employer_id')
        employer = get_object_or_404(Employer, id = employer_id)

        advertisements = JobPost.objects.filter(employer=employer)
        # creating serializer with application objects
        serializer = JobPostSerializer(advertisements, many=True)

        return Response(serializer.data)






# to get all the job_posts filtered for a specific job category
class JobPostsOfJobCategoryAPIView(APIView):
    def get(self, request, format=None):
        job_category_slug = request.query_params.get('slug')
        
        if not job_category_slug:
            return Response({'error': 'Job category slug is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            category = Category.objects.get(slug=job_category_slug)
        except Category.DoesNotExist:
            return Response({'error': 'Invalid job category slug'}, status=status.HTTP_404_NOT_FOUND)
        
        job_posts = JobPost.objects.filter(job_category=category)
        serializer = JobPostSerializer(job_posts, many=True)

        return Response(serializer.data)
    

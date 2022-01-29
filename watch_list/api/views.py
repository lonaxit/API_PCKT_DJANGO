# for use in ViewSet import get_object_or_404
from django.shortcuts import get_object_or_404
# import Response
from rest_framework.response import Response

# import validation errors
from rest_framework.exceptions import ValidationError

from rest_framework import status
# import models
from watch_list.models import *

from watch_list.api.serializers import *

# from rest_framework import mixins
from rest_framework import generics

# import here below used for class based views
from rest_framework.views import APIView

# using viewsets

from rest_framework import viewsets

# using permissions 
from rest_framework.permissions import IsAuthenticated

# import custom permissions
from watch_list.api.permissions import *

# import classes from custom throtle class
from watch_list.api.throttling import *


# import throttle  classes for general settings
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle

# filtering backend
from django_filters.rest_framework import DjangoFilterBackend

# IMPORT FILTERS TO USE FOR SEARCH commented out used only in search and ordering filters
from rest_framework import filters

# import custom pagination classes
from watch_list.api.pagination import *


# ---------------- FILTERS EXAMPLE -----------------

# We write a new class to experiment with filter as in the dfr docs using filter and urls
class UserReviews(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # adding permission, comment out since its a list or get request
    # permission_classes = [IsAuthenticated]
    
    # default throttle classes
    # throttle_classes =[UserRateThrottle, AnonRateThrottle]
    
    # throttle_classes =[ReviewListThrottle, AnonRateThrottle]
    
    # over writing default queryset : filter against current user and urls
    # def get_queryset(self):
    #     # get the wachlist pk
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    
    # filtering using query parameter
    def get_queryset(self):
        
        username = self.request.query_params.get('username',None)
        
        return Review.objects.filter(review_user__username=username)


# -----------------FILTERS END----------------------

# ************** CONCRETE CLASS BASED VIEWS ****************** 
# WE use them for our refactored views urls

# class ReviewList(generics.ListCreateAPIView):
#     # ListCreateAPIView gives us both the get and post methods
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    

# class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
#     # gives get, put and destroy methods
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

# ***************** CONCRETE CLASS BASE VIEWS END ************************


# *********** WRITING CONCRETE VIEWS PER REQUIREMENTS *******************

# changed ListCreate to ListAPIView, so that we can create a link to create review seperate
class ReviewList(generics.ListAPIView):
    # ListCreateAPIView gives us both the get and post methods
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # adding permission, comment out since its a list or get request
    # permission_classes = [IsAuthenticated]
    
    # default throttle classes
    # throttle_classes =[UserRateThrottle, AnonRateThrottle]
    
    throttle_classes =[ReviewListThrottle, AnonRateThrottle]
    
    # filtering backend
    filter_backends = [DjangoFilterBackend]
    
    # pls mention the fields to be filtered against 
    filterset_fields = ['review_user__username', 'active']
    
    # over writing default queryset 
    def get_queryset(self):
        # get the wachlist pk
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
    
    
class ReviewCreate(generics.CreateAPIView):
    
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes=[ReviewCreateThrottle]
    
    def get_queryset(self):
        # just return the review object
        return Review.objects.all()
     
    #  we need to overwrite the current function becos we need to pass the current movie ID for which review is being created
    
    def perform_create(self,serializer):
        
        pk = self.kwargs.get('pk')
        # get movie
        movie= WatchList.objects.get(pk=pk)
        
        # logic to prevent multple creation of reviews by a user
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie,review_user=review_user)
        if review_queryset.exists():
            
            raise ValidationError("You have already reviewed this watchlist")
        
        # custom calculations
        # check if rating is 0 
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
        
        # increase the rating  
        movie.number_rating = movie.number_rating + 1
        
        # save
        movie.save()
        
        # save together with related watchlist and user
        serializer.save(watchlist=movie,review_user=review_user)
        
        
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    # allow get, put and destroy methods
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    
    # throttle_classes =[UserRateThrottle,AnonRateThrottle]
    
    # using ScopedRateThrottle
    throttle_classes =[ScopedRateThrottle]
    throttle_scope = 'review-detail'




# ************** END WRITING CONCRETE VIEWS PER REQUIREMENTS ***************



# We will use mixins to create views for our Reviews :;generics.GenericAPIView is alwys last and do not change attribute names such as queryset and serializer_class
# ******************************** mixins **************************
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#             return self.retrieve(request, *args, **kwargs)
    
# *************** ********** end of mixins ************* 


# APIVIEW [ Class based views]
# AV means API View

# watchlist views 


class WatchListAV(APIView):
     # adding permissions 
    permission_classes=[IsAdminOrReadOnly]
    
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data)
    
    
    def post(self,request):
        
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# A new watch list to test filter and search, for test purpose only
class WatchListGV(generics.ListAPIView):
    queryset =WatchList.objects.all()
    serializer_class = WatchListSerializer
    # throttle_classes =[ReviewListThrottle, AnonRateThrottle]
    
    # filtering backend
    # filter_backends = [DjangoFilterBackend]
    
    # pls mention the fields to be filtered against 
    # filterset_fields = ['title', 'platform__name']
    
    # ------- searching commented out
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']
    
    # -----ordering filters
  
  
    # comment becos interfering with cursorPagination implementation
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']
    
    # pageNumber example
    # pagination_class =WatchListPagination
    
    # LIMIT OFFSET EXAMPLE
    pagination_class =WatchListLOPagination

    # cursor pagination 
    pagination_class =WatchListCPagination
    

class WatchDetailAV(APIView):
    
    # adding permissions 
    permission_classes=[IsAdminOrReadOnly]
    throttle_classes =[AnonRateThrottle]
    
    def get(self,request,pk):
        
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            # creating a custom message
            return Response({'Error': 'Movie Not Found'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    def delete(self,request,pk):
        
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        # you can create a dictionary to sent more information about the action {'Error':'Not Found'}
        return Response(status = status.HTTP_204_NO_CONTENT)
        

# *************** VIEWSETS CODE ****************

# class Platform(viewsets.ViewSet):
#     # viewSet supports list,create,put,patch and delete methods ....
#     # used only for simple tasks and difficult to use with customized urls
    
    
#     def list(self,request):
#         queryset= StreamPlatform.objects.all()
#         serializer= StreamPlatformSerializer(queryset,many=True)
#         return Response(serializer.data)

    
#     def retrieve(self,request,pk=None):
        
#         queryset= StreamPlatform.objects.all()
#         watchlist = generics.get_object_or_404(queryset,pk=pk)
#         serializer= StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create (self,request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self,request,pk):
        
#         platform = StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         # you can create a dictionary to sent more information about the action {'Error':'Not Found'}
#         return Response(status = status.HTTP_204_NO_CONTENT)
    

# # *********** END VIEWSETS CODE ***************** **


# *************** MODEL VIEWSETS CODE ****************

# class PlatformMVS(viewsets.ModelViewSet):
#      # adding permissions 
#     permission_classes=[IsAdminOrReadOnly]
    
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer



# *********** END MODEL VIEWSETS CODE ****************



# streamplatform views

class StreamPlatformAV(APIView):
    
     # adding permissions 
    permission_classes=[IsAdminOrReadOnly]
    
    def get(self,request):
        
        platform = StreamPlatform.objects.all()
        # context={'request': request} is added here because of the HyperLinkedRelatedField becos we are accessing the stream page, if we are accessing a different resource we do the same
        
        # serializer = StreamPlatformSerializer(platform,many=True,context={'request': request})
        
        serializer = StreamPlatformSerializer(platform,many=True)
        
        return Response(serializer.data)
    
    def post(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(APIView):
    
     # adding permissions 
    permission_classes=[IsAdminOrReadOnly]
    throttle_classes= [AnonRateThrottle]
    
    def get(self,request,pk):
        
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            # creating a custom message
            return Response({'Error': 'Not Found'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    def delete(self,request,pk):
        
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        # you can create a dictionary to sent more information about the action {'Error':'Not Found'}
        return Response(status = status.HTTP_204_NO_CONTENT)
        

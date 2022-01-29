
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# we wil import default user model
from django.contrib.auth.models import User
# import Tokens as well 
from rest_framework.authtoken.models import Token

# imports from watch list

from watch_list.api import serializers
from watch_list import models



class StreamPlatformTestCase(APITestCase):
    

    
    def setUp(self):
        # 1 create user
        self.user = User.objects.create_user(username='newuser',password="password@123")
        # authenticate the user
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # create data manually
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix",about="#1 platform",website="htpps://netflix.com")
        
    # send/post data
    def test_streamplatform_create(self):
        
        data ={
            "name":"Netflix",
            "about":"#1 streaming platform",
            "website":"http://netflix.com"
        }
        response = self.client.post(reverse('stream'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    # get data 
  
    def test_streamplatform_list(self):
        # for now empty data
        response = self.client.get(reverse('stream'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # access individual data created in setup 
    def test_streamplatform_individual(self):
      
        response = self.client.get(reverse('stream-detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
        # write test for put, delete for normal user

class WatchListTestCase(APITestCase):
    
    def setUp(self):
        # 1 create user
        self.user = User.objects.create_user(username='newuser',password="password@123")
        # authenticate the user
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # create data manually
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix",about="#1 platform",website="htpps://netflix.com")
        
        # create a movie
        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,title="Example Title",storyline="Example Story",active=True
            )
        
    def test_watchlist_create(self):
        data={
            "platform":self.stream, 
            "title":"Example Title",
            "storyline":"Example Story",
            "active": True
        }
        response = self.client.post(reverse('movie-list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    
    # next we get some data and individual element
    
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    
    def test_watchlist_ind(self):
        
        response = self.client.get(reverse('movie-detail',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        # test for name
        self.assertEqual(models.WatchList.objects.get().title,'Example Title')


class ReviewTestCase(APITestCase):
    
    def setUp(self):
        # 1 create user
        self.user = User.objects.create_user(username='newuser',password="password@123")
        # authenticate the user
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # create data manually
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix",about="#1 platform",website="htpps://netflix.com")
        
        # create a movie
        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,title="Example Title",storyline="Example Story",active=True
            )
        
        self.watchlist2 = models.WatchList.objects.create(
            platform=self.stream,title="Example Title2",storyline="Example Story2",active=True
            )
        # create a review
        self.review = models.Review.objects.create(
            review_user=self.user,
            rating=5,
            description="Great",
            watchlist= self.watchlist2,
            active=True
        )

    def test_review_create(self):
        data={
            "review_user":self.user,
            "rating":5,
            "description":"Great",
            "watchlist": self.watchlist,
            "active":True
        }
        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
        # testing review create for the second time
        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
        
    def test_review_create_unauth(self):
        
        data={
            "review_user":self.user,
            "rating":5,
            "description":"Great",
            "watchlist": self.watchlist,
            "active":True
        }
         
        #  use force_authentication to login as a another user, None means we are not logged in
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    # creaet an update test 
    
    def test_review_update(self):
        
        data={
            "review_user":self.user,
            "rating":4,
            "description":"Great-Updated",
            "watchlist": self.watchlist,
            "active":False
        }
        
        response = self.client.put(reverse('review-detail',args=(self.review.id,)), data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    # access all reviews
    
    def test_review_list(self):
        
        response = self.client.get(reverse('review-list',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    # access individual review 
    
    def test_review_ind(self):
        
        response = self.client.get(reverse('review-detail',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_review_user(self):
        
        response = self.client.get('/watch/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
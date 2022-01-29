# we will use drf and api test cases 

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# we wil import default user model
from django.contrib.auth.models import User
# import Tokens as well 
from rest_framework.authtoken.models import Token





class RegisterTestCase(APITestCase):
    
    # Define the test method
    def test_register(self):
        
        # get data, do a post, check url, get response
        
        # dictionary of data
        data ={
            "username":"testcase",
            "email":"test@zxy.com",
            "password":"password@123",
            "password2":"password@123"
        }
        # send a request to client
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # you can add other assertions here as well  using the assertEqual to
        
class LoginLogoutTestCase(APITestCase):
    
    # we need to create a user before login and we do that in the setUp() method
    def setUp(self):
        self.user = User.objects.create_user(username="example",password="password@123")
    
    
    # login test
    def test_login(self):
        
        data ={
            "username":"example",
            "password":"password@123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    # logout test
    
    def test_logout(self):
        # get the token first
        
        # this works as well
        # self.token = Token.objects.get(user__username='example') 
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        token = Token.objects.get(user__username='example')
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        # send a request to logout reverse link
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
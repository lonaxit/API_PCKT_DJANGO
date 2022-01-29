# We will use  functionbased views all logic is for token based authentication



# api_view used for function based views
from rest_framework.decorators import api_view

# import Response
from rest_framework.response import Response

# import token class for token authentication only
from rest_framework.authtoken.models import Token

# import for jwt authentication comment out
# from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import status

from user_app.api.serializers import *

# comment out because we are not auto generating token as used in tokent authentication
from user_app import models

# logout function based view
@api_view(['POST'])
def logout_view(request):
    
    if request.method =='POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# registration function based view for token authentication
@api_view(['POST',])
def registration_view(request):
    
    if request.method == 'POST':
        
        serializer = RegistrationSerializer(data=request.data)
        
        # create data dictionary to store our data
        data ={}
        
        if serializer.is_valid():
            # the account variable is the one returned in serializer .py file
            account = serializer.save()
            
            data['response'] = "Registration is successful"
            data['username'] = account.username
            data['email'] = account.email
            
            token= Token.objects.get(user=account).key
            
            data['token'] =token
        
        else:
            data= serializer.errors
            
        # access the created token in models.py file
        # returned status code is to be used in the test
        return Response(data,status.HTTP_201_CREATED)


# registration views for jwt authentication comment out
# @api_view(['POST',])
# def registration_view(request):
    
#     if request.method == 'POST':
        
#         serializer = RegistrationSerializer(data=request.data)
        
#         # create data dictionary to store our data
#         data ={}
        
#         if serializer.is_valid():
#             # the account variable is the one returned in serializer .py file
#             account = serializer.save()
            
#             data['response'] = "Registration is successful"
#             data['username'] = account.username
#             data['email'] = account.email
            
#             # token= Token.objects.get(user=account).key
            
#             # data['token'] =token
#             refresh = RefreshToken.for_user(account)
#             data['token'] = {
#                             'refresh': str(refresh),
#                             'access': str(refresh.access_token),
#                             }
#         else:
#             data= serializer.errors
            
#         # access the created token in models.py file
            
#         return Response(data)

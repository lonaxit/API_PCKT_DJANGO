
# import Response
from rest_framework.response import Response
# api_view used for function based views
from rest_framework.decorators import api_view
from rest_framework import status
# import models
from watch_list.models import *

from watch_list.api.serializers import *

# import here below used for class based views

from rest_framework.views import APIView



# # 
@api_view(['GET','POST',])
def movie_list(request):
    # check for http verbs
    if request.method =='GET':
        
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies,many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        

@api_view(['GET','PUT','DELETE'])
def movie_detail(request,pk):
    
    if request.method =='GET':
        
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            # creating a custom message
            return Response({'Error': 'Movie Not Found'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    if request.method == 'DELETE':
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        # you can create a diction to sent more information about the action {'Error':'Not Found'}
        return Response(status = status.HTTP_204_NO_CONTENT)

# serializers for PUT, POST,DELETE
# Every thing above here commented has to with function based views and we have not used ModelSerializers yet.


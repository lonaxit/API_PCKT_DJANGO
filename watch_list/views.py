from django.shortcuts import render
from django.http import JsonResponse

from .models import Movie


def movie_list(request):
    movies = Movie.objects.all()
    
    # create a dictionary
    MovieDict = movies.values()
    # convert to an iterable
    movieList = list(MovieDict)
    
    # create=ing a dictionary to send as json response
    data ={
        'movies': movieList
    }
    
    return JsonResponse(data)

def movie_detail(request,pk):
    movie = Movie.objects.get(pk=pk)
    data ={
        'id':movie.pk,
        'name': movie.name,
        'description':movie.description,
        'active':movie.active,
    }
    return JsonResponse(data)



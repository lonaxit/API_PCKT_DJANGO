from django.urls import path,include
from watch_list.api.views import *

# ******* section of code for ViewSets ******* 
# using routers 1.
from rest_framework.routers import DefaultRouter

# 2. create router
# router = DefaultRouter()
# do not use as_view() when registering ViewSet
# router.register('platform', Platform, basename='platform' )


# # route for MODEL VIEWSET
# router.register('platform', PlatformMVS,basename='platform' )

# # ******* end section of code for ViewSets ******* 

urlpatterns = [

    path('list/',WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name="movie-detail"),
    
    # to test filters on watch list
    path('list2/',WatchListGV.as_view(), name='list2'),
    
    # 3 include router in url patterns for viewset
    # path('',include(router.urls)),
    
    
#    comment out and use view set for test
    path('stream/',StreamPlatformAV.as_view(), name='stream'),
    path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name="stream-detail"),
    
    
    # writing views according to our conditions
     # create a review 
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name="review-create"),
    
    # get reviews for a particular watchlist
    path('<int:pk>/reviews/', ReviewList.as_view(), name="review-list"),

    # get detail of a review
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    
    # for basic/default concrete based views
    
    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>',ReviewDetail.as_view(), name='review-detail')
    
    
    # testing filters for current user and urls
    # path('reviews/<str:username>/', UserReviews.as_view(), name='user-reviews'),
    
    
    # testing for query parameter e.g. /?username=apitivkaa  will be attached automatically
    path('reviews/', UserReviews.as_view(), name='user-reviews'),
    
    
]
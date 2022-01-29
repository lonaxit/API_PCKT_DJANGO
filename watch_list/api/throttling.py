# import for customized throttling 

from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    
    scope ='review-create'


class ReviewListThrottle(UserRateThrottle):
    
    scope ='review-list'
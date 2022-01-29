# contains classes pagination 
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination,CursorPagination

# create custom class to rewrite the page size then import in our views

class WatchListPagination(PageNumberPagination):
    
    # overwrite attributes here method
    page_size =2
    # we can rename the page in the url, comment out 
    # page_query_param= 'p'
    # customized page size
    # page_size_query_param= 'size'
    # limit max page limit
    max_page = 10
    # accessing last page
    # last_page_strings='end' 
    
    
class WatchListLOPagination(LimitOffsetPagination):
    
    default_limit =3
    limit_query_param = 'limit'
    offset_query_param = 'start'


class WatchListCPagination(CursorPagination):
    
    # overwriting values with
    page_size=2
    ordering ='created'
    cursor_query_param = 'record'
   
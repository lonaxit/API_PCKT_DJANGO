from rest_framework import serializers
# import models
from watch_list.models import *

#  ****************************************************************
# REVIEW SERIALIZER
class ReviewSerializer(serializers.ModelSerializer):
    # control what is returned in our nested relationship 
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model= Review
        # To create a review for 'stream/<int:pk>/review-create' we need to exclude the watchlist in the serializer
        
        # fields= "__all__"
        
        # ('watchlist',) the last comma makes it a tuple
        exclude = ('watchlist',)
        
        
        
# MODEL SERIALIZERS BELOW

class WatchListSerializer(serializers.ModelSerializer):
    # custom serializer fields
    # len_name = serializers.SerializerMethodField()
    
    # create relationship with reviews, a watch list may have many reviews
    # commented out so that we dont have the relationship
    
    # reviews = ReviewSerializer(many=True,read_only=True)
    
    # override the platform field, so that
    platform = serializers.CharField(source='platform.name')   
    
    class Meta:
        model= WatchList
        # fields = ['name','description','active'] individual fields
        fields = "__all__"
        # exclude= ['active']
    
    # custom method to calculate length of name
    # signature
    
    # def get_fieldname(self,object):
    #     logic here
    
    # def get_len_name(self,object):
    #     length = len(object.name)
    #     return length
        
        
    # # if you need  validations, then you can define them like so
        
    # # comment to test validators
    # def validate_name(self,value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short!")
    #     return value
    
    # # Object validation
    # def validate(self,data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError('Title and description should not be same')
    #     else:
    #         return data
        

class StreamPlatformSerializer(serializers.ModelSerializer):
    # nested relationship, one platform can have many watchList, use the related name in the model relationship, we have created a new field where we can collect all related fields 
    # i.e. the nested serializer
    
    watchlist = WatchListSerializer(many=True,read_only=True) 
    
    # serializers relations
    # 1. stringRelatedField
    
    # watchlist = serializers.StringRelatedField(many=True)
    
    # 2. PrimaryKeyRelatedField
    
    # watchlist = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    
    # 3. HyperlinkedRelatedField
    
    # watchlist = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='movie-detail')
    
    class Meta:
        model= StreamPlatform
        
        fields ="__all__"
    


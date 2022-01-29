# 1. first import serializers from rest_framework

from rest_framework import serializers
# import models
from watch_list.models import *

# naming conventions : name serializers after model names
# first we use Serializer
# validators function , should be outside of the class
# def name_length(value):
    
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")
#     return value

# class MovieSerializer(serializers.Serializer):
#     pk = serializers.IntegerField(read_only=True)
#     # name = serializers.CharField() used for field validation
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
    # we can add validation and methods in here as well
    # CREATE METHODS FOR PUT, POST AND DELETE REQUEST
    
    # method to create a new item
    # def create(self,validated_data):
    #     return Movie.objects.create(**validated_data)
    
    # update methods
    
    # def update(self,instance,validated_data):
    #     instance.name = validated_data.get('name',instance.name)
    #     instance.description = validated_data.get('description',instance.description)
    #     instance.active = validated_data.get('active',instance.active)
    #     instance.save()
    #     return instance
    
    # Validations
    
    
    # 1. Field level validation
    # comment to test validators
    # def validate_name(self,value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short!")
    #     return value
    
    # Object validation
    # def validate(self,data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError('Title and description should not be same')
    #     else:
    #         return data
        
# ABOVE CODE IS FOR serializers OPTION

# ****************************************************************

# MODEL SERIALIZERS BELOW

class MovieSerializer(serializers.ModelSerializer):
    # custom serializer fields
    len_name = serializers.SerializerMethodField()
    
    class Meta:
        model= Movie
        # fields = ['name','description','active'] individual fields
        fields = "__all__"
        # exclude= ['active']
    
    # custom method to calculate length of name
    # signature
    
    # def get_fieldname(self,object):
    #     logic here
    
    def get_len_name(self,object):
        length = len(object.name)
        return length
        
        
    # if you need  validations, then you can define them like so
        
    # comment to test validators
    def validate_name(self,value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short!")
        return value
    
    # Object validation
    def validate(self,data):
        if data['name'] == data['description']:
            raise serializers.ValidationError('Title and description should not be same')
        else:
            return data
        
from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
 
 
#  Next create a registration serializer

class RegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    
    class Meta:
        model= User
        fields = ['username','email','password','password2']
        # set password as write only
        extra_kwargs ={
            'password': {'write_only':True}
        }
        # overwrite the save method
    def save(self):
        
        # get acccess to password
        password = self.validated_data['password']
        password2 =self.validated_data['password2']
            
        if password != password2:
            
            raise serializers.ValidationError({
                    'error': 'Password mismatch'
                })
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({
                'error': 'email exist already'
            })
            
        if User.objects.filter(username=self.validated_data['username']).exists():
                raise serializers.ValidationError({
                'error': 'username exist already'
            })
        
        # create a user manually
        account = User(email=self.validated_data['email'],username=self.validated_data['username'])
        
        account.set_password(password)
        account.save()
        
        return account
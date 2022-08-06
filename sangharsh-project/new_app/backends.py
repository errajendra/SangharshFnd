from django.contrib.auth.backends import ModelBackend
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

# Overriding the authenticte method to autheticate the users with email

# Authenticate resource with Email Id
class EmailBackend(ModelBackend):
    def authenticate(self,request,username=None,password=None,**kwargs):
        # This Try method will check for resource in ResourceDetail model
        try:
            resource = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            return None      
        else: 
            if check_password(password,resource.password):
                return resource      
    def get_user(self,user_id):
        # This Try method will check for resource in ResourceDetail model
        try:
            resource = CustomUser.objects.get(pk=user_id)
            return resource
        except CustomUser.DoesNotExist:
            return None



# Authenticate User with Email Id
class UserEmailBackend(ModelBackend):
    # This Try method will check for User in User model
    def authenticate(self,request,username=None,password=None,**kwargs):
        try:
                user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None 
        else:
            if user.check_password(password):
                return user 
    def get_user(self,user_id):
        # This Try method will check for user in User model
            try:
                user = User.objects.get(pk=user_id)
                return user
            except User.DoesNotExist:
               return None               

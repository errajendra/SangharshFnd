from datetime import date, timedelta
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import CustomUserManager
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from djmoney.models.fields import MoneyField

# Create your models here.


def one_month_from_today():
    return date.today() + timedelta(days=30)


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value
    


class District(models.Model):
    district_name = models.CharField(max_length=100) 
    state_name = models.CharField(max_length=100) 
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.pin_code:
            return self.district_name +", "+ self.state_name+ "-" + str(self.pin_code)
        return self.district_name +", "+ self.state_name
    
       


class CustomUser(AbstractBaseUser):
    email = LowercaseEmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    AP = "A+"
    AM = "A-"
    BP = "B+"
    BM = "B-"
    ABP = "AB+"
    ABM = "AB-"
    OP = "O+"
    OM = "O-"
    
    BLOOD_GROUP_CHOICES = [
        (AP, "A+"),
        (AM,"A-"),
        (BP, "B+"),
        (BM, "B-"),
        (ABP, "AB+"),
        (ABM, "AB-"),
        (OP,"O+"),
        (OM, "O-"),
    ]
    
    Presidant = 'Presidant'
    Vice_President = 'Vice President'
    Executive_Vice_Presedant = 'Executive Vice Presedant'
    Secretary = 'Secretary'
    Joint_Secretary = 'Joint Secretary'
    Treasure = 'Treasure'
    Executive_Chairman = 'Executive Chairman'
    Member = 'Member'
    
    USER_ROLE_CHOICES = [
        (Presidant , 'Presidant'),
        (Vice_President , 'Vice President'),
        (Executive_Chairman , 'Executive Chairman'),
        (Executive_Vice_Presedant , 'Executive Vice Presedant'),
        (Secretary , 'Secretary'),
        (Joint_Secretary , 'Joint Secretary'),
        (Treasure , 'Treasure'),
        (Member , 'Member'),
    ]
    
    mobile_nomber = models.BigIntegerField()
    alternet_mobile_nomber = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    profile = models.ImageField(upload_to='profile', default='user.png')
    # address
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)  #Choice or Foregen key of Distruct model
    
    role = models.CharField(choices=USER_ROLE_CHOICES, max_length=50, default=Member)
    
    blood_group = models.CharField(max_length=4, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    valid_up_to = models.DateField(default=date.today(), null=True,blank=True)
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_on']

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    objects = CustomUserManager()
    
    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def __str__(self):
        return self.name
    
    def full_address(self):
        if self.address1 and self.address2:
            return str(self.address1)+", "+str(self.address2) + ", "
        elif self.address1:
            return self.address1
        elif self.address2:
            return self.address2
        return " "
    
    def get_district(self):
        if self.district:
            return str(self.district)+", "
        return " "

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
    
    def get_role(self):
        if self.admin:
            return "Admin"
        elif self.staff:
            return "Staff"
        else:
            return "Member"
    
    def get_expiry(self):
        return self.valid_up_to
    
    
# contact model
class Contact(models.Model):
    name = models.CharField(max_length=50)
    mobile_nomber = models.BigIntegerField(default=1234567890)
    email = models.EmailField()
    message = models.TextField()
    mark = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_on']
        
        

# blood donation
class BloodDonate(models.Model):
     
    AP = "A+"
    AM = "A-"
    BP = "B+"
    BM = "B-"
    ABP = "AB+"
    ABM = "AB-"
    OP = "O+"
    OM = "O-"
    
    BLOOD_GROUP_CHOICES = [
        (AP, "A+"),
        (AM,"A-"),
        (BP, "B+"),
        (BM, "B-"),
        (ABP, "AB+"),
        (ABM, "AB-"),
        (OP,"O+"),
        (OM, "O-"),
    ]
    
    donator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="DONATOR")
    patient_name = models.CharField(max_length=100)
    patient_blood_group = models.CharField(max_length=4, choices=BLOOD_GROUP_CHOICES)
    patient_mobile = models.BigIntegerField(blank=True, null=True)
    patient_address = models.CharField(max_length=500)
    receiver_name = models.CharField(max_length=100)
    receiver_mobile = models.BigIntegerField()
    receiver_address = models.CharField(max_length=500)
    message = models.CharField(max_length=500, blank=True, null=True)
    verify = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def is_verified(self):
        return self.verify
    
    def __str__(self):
        return str(self.donator)+"->"+str(self.patient_blood_group)+"->"+str(self.patient_name)
    
    
    
# class UserAddress(models.Model):
    
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_address")
#     address1 = models.CharField(max_length=50)
#     address2 = models.CharField(max_length=50, blank=True, null=True)
#     district = models.CharField(max_length=50)
#     state = models.CharField(max_length=50, default="Madhya Pradesh")
#     pin_code = models.CharField(max_length=6, default="486886")
    
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
    
#     def __str__(self) -> str:
#         return str(self.address1)+" "+str(self.district)+" "+str(self.state) + " " + str(self.pin_code)
    
    
    
# class UserRole(models.Model):
    
#     Presidant = 'PR'
#     Vice_President = 'VPR'
#     Executive_Vice_Presedant = 'EVP'
#     Secretary = 'S'
#     Joint_Secretary = 'JS'
#     Treasure = 'T'
#     Executive_Chairman = 'EC'
#     Member = 'M'
    
#     USER_ROLE_CHOICES = [
#         (Presidant , 'Presidant'),
#         (Vice_President , 'Vice President'),
#         (Executive_Chairman , 'Executive Chairman'),
#         (Executive_Vice_Presedant , 'Executive Vice Presedant'),
#         (Secretary , 'Secretary'),
#         (Joint_Secretary , 'Joint Secretary'),
#         (Treasure , 'Treasure'),
#         (Member , 'Member'),
#     ]
    
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_role")
#     role = models.CharField(choices=USER_ROLE_CHOICES, max_length=3, default=Member)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
    
#     def __str__(self) -> str:
#         return self.role
    
    
    
class Activity(models.Model):
    
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 1.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


    title = models.CharField(max_length=100)
    featured_image = models.ImageField(upload_to='activity/', null= True, blank=True, validators=[validate_image])
    description = RichTextField()
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
    
    
    
def year_choices():
        return [(r,r) for r in range(2022, datetime.date.today().year+1)]
    
    
class FoundationAccountSetting(models.Model):
    
    percentage_validators=[MinValueValidator(0.9), MaxValueValidator(100)]
    
    YEAR_CHOICES = year_choices()
    current_year = datetime.date.today().year
    
    year = models.IntegerField(choices=YEAR_CHOICES, default=current_year)    
    fund_required = MoneyField(max_digits=14, decimal_places=0, default_currency='INR')
    provided_food_percentage = models.FloatField(null=True, blank=True, validators=percentage_validators)
    provided_blood_percentage = models.FloatField(null=True, blank=True, validators=percentage_validators)
    # added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    

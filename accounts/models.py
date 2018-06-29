from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser)
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.db import IntegrityError, transaction
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils import timezone

now = timezone.now()

# from django.utils.timezone.now import timezone
# Create your models here.



class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username ,email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,

        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

USERNAME_REGEX = '^[a-zA-Z0-9]*$'

class MyUser(AbstractBaseUser):
        gender_choices=[('male','Male'),('female','Female')]
        id = models.AutoField(primary_key=True)
        username=models.CharField(max_length=120,validators=[RegexValidator(
                                                    regex=USERNAME_REGEX,
                                                    message='Username must contain alphabets or digits',
                                                    code='Invalid Username')],verbose_name='Username',unique=True)
        email = models.EmailField(
        verbose_name='email address',
        max_length=120,
        unique=True,
    )
        first_name=           models.CharField(max_length=100,verbose_name='First Name',default='')
        last_name=            models.CharField(max_length=100,verbose_name='Last Name',default='')
        gender =              models.CharField(max_length=6,choices=gender_choices,verbose_name='Gender',default='Male')
        class_name =          models.IntegerField(validators=[MinValueValidator(8),MaxValueValidator(12)],verbose_name='Class',default='9')
        father_name=          models.CharField(max_length=100,verbose_name='Father\'s Name',default='')
        father_occupation   = models.CharField(max_length=100,verbose_name='Father\'s Occupation',default='')
        mother_name=          models.CharField(max_length=100,verbose_name='Mother\'s Name',default='')
        mother_occupation   = models.CharField(max_length=100,verbose_name='Mother\'s Occupation',default='')
        date_of_birth=        models.DateField(verbose_name='Date of Birth',null=True)
        date_of_joining=      models.DateField(verbose_name='Date of Joining',null=True)
        subjects_opted=       models.TextField(verbose_name='Subjects',null=True)
        mobile=               models.CharField(max_length=12,verbose_name='Mobile',default='')
        address=              models.TextField(max_length=156,verbose_name='Address',default='')
        city=                 models.CharField(max_length=12,verbose_name='City',default='')
        comments=             models.TextField(max_length=12,verbose_name='comments',default='')
        profile_pic=          models.ImageField(upload_to='profile_pics',max_length=100,null=True)
        created  =            models.DateTimeField(auto_now_add=True)
        updated  =            models.DateTimeField(auto_now=True)



        is_staff= models.BooleanField(default=False)
        is_active = models.BooleanField(default=True)
        is_admin = models.BooleanField(default=False)
        
        objects = MyUserManager()
        
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = ['email']
        
        def get_full_name(self):
        # The user is identified by their email address
            return self.username
        
        def get_short_name(self):
        # The user is identified by their email address
            return self.username
        
        def __str__(self):              # __unicode__ on Python 2
            return self.username
        
        def has_perm(self, perm, obj=None):
            "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
            return True
        
        def has_module_perms(self, app_label):
            "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
            return True
        
        def get_absolute_url(self):
            return reverse("student_detail",kwargs={"pk":self.pk})

        class Meta:
            ordering = ['-created','updated']
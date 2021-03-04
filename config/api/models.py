from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    username = models.CharField(blank=True, null = True, max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    POSITION_CHOICES = (
        ('Manager', 'Manager'),
        ('Senior Developer', 'Senior Developer'),
        ('Junior Developer', 'Junior Developer'),
        ('Intern', 'Intern')
    )
    designation = models.CharField(max_length=30, choices=POSITION_CHOICES)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'designation']

    def __str__(self):
        return "{}".format(self.email)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=10)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=6)
    photo = models.ImageField(upload_to='uploads', blank=True)


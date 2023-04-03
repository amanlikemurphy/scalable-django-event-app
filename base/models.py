from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)

    id = models.UUIDField(default=uuid.uuid4, unique = True, 
                          primary_key=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('health', 'Health'),
        ('tech', 'Tech'),
        ('hobbies', 'Hobbies'),
        ('business', 'Business'),
        ('sports', 'Sports'),
        ('food', 'Food and Eat'),
        ('arts', 'Visual Arts'),
    ]
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='Music')
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default='0.00')
    date_time = models.DateTimeField()
    featured_image = models.ImageField(blank=True, null=True, default="/images/default.jpg")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    attendees = models.ManyToManyField(User, through='Registration', related_name='events_attending')
    id = models.UUIDField(default=uuid.uuid4, unique = True, 
                          primary_key=True, editable=False)

    
    def __str__(self):
        return self.name


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, 
                          primary_key=True, editable=False)

    class Meta:
        unique_together = ('user', 'event')

    #Function to know attendees that registered
    def __str__(self):
        return f"{self.name} ({self.email}) registered for {self.event.name}"


from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

# Create your models here.

class Staff(models.Model):
    name=models.CharField(default=None, max_length=64)
    photo=models.ImageField(default=None,)
    address=models.CharField(default=None, max_length=120)
    description=models.CharField(default=None, max_length=500)

class DishMenu(models.Model):
    img = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    title = models.CharField(max_length=100, verbose_name='Наименование')
    subtitle = models.CharField(max_length=250)
    price = models.IntegerField(null=False, verbose_name='Ценевой сегмент')

    def __str__(self):
        return self.title

class Posts(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    title=models.CharField(default=None, max_length=64,)
    slug=models.SlugField(max_length=200, unique=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE, related_name='blog_posts')
    created_on=models.DateTimeField(auto_now_add=True)
    content=models.TextField()

    class Meta:
        ordering=['-created_on']

    def __str__(self):
        return self.title

class Comment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment', null=True)
    post=models.ForeignKey(Posts, related_name='comments', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, default=None)
    content = models.TextField(default=None)
    email=models.EmailField(max_length=255, default=None)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['date_added']

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='img.jpg', upload_to='profile_pics/')

    def __str__(self):
        return f'{self.user.username} Profile'

class Category(models.Model):
    category_id = models.IntegerField()
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')
    def __str__(self):
        return self.title

Breakfast = 'Breakfast'
Lunch = 'Lunch'
Dinner = 'Dinner'

subsection_choices = [(Breakfast, _("Breakfast")),
                      (Lunch, _("Lunch")),
                      (Dinner, _("Dinner"))]

class Subsection(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    name_of = models.CharField(choices=subsection_choices, null=True, max_length=255)
    name = models.CharField(max_length=60, null=True)
    price = models.IntegerField(null=True)
    description = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Booking(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    email = models.EmailField(max_length=255, default=None)
    booking_date = models.DateTimeField( null=True,blank=True, auto_now_add=True)
    booking_time = models.TimeField( null=True, blank=True,default=None)
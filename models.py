from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class ColorCombination(models.Model):
    top_color = models.CharField(max_length=100)
    bottom_color = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.top_color} with {self.bottom_color}'


class WardrobeItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='wardrobe_images/', default='default_image.jpg')
    article_type = models.CharField(max_length=100, blank=True, default='')
    base_colour = models.CharField(max_length=100, blank=True, default='')
    season = models.CharField(max_length=100, blank=True, default='')
    usage = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f"{self.article_type} - {self.base_colour}"

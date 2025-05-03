from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=40, default="")
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Favourite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recipe = models.CharField(max_length=100)

    def __str__(self):
        return f'Recipe OF {self.user.name}'
    
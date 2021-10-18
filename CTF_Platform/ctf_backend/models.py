from django.db import models
from authentication.models import Team
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=200)
    key=models.CharField(max_length=50)
    def __str__(self):
         return self.name

class Problem(models.Model):
    title=models.CharField(max_length=200)
    desc=models.CharField(max_length=1000)
    file=models.FileField(verbose_name='file',null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category')
    def __str__(self):
         return self.title

class Submission(models.Model):
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)
    team=models.ForeignKey(Team,on_delete=models.CASCADE)
    solution=models.CharField(max_length=200)
    def __str__(self):
        return self.solution
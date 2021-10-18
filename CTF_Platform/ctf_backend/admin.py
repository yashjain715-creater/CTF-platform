from django.contrib import admin
from .models import Category,Problem,Submission
# Register your models here.

admin.site.register(Category)
admin.site.register(Problem)
admin.site.register(Submission)
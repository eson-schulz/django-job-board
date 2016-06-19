from django.contrib import admin
from .models import Post, Category, User, JobType

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(JobType)
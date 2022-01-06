from django.contrib import admin
from .models import User, Post, Following, Liked

@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class AuthorAdmin(admin.ModelAdmin):
    pass
# Register your models here.
@admin.register(Following)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Liked)
class AuthorAdmin(admin.ModelAdmin):
    pass
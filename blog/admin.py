from django.contrib import admin

from blog.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'image', "is_published", "views")
    search_fields = ('title', "is_published",)
    list_filter = ('is_published', "views",)

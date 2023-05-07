from django.contrib import admin
from . import models

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}

admin.site.register(models.Author)
admin.site.register(models.Tag)
admin.site.register(models.Post)
admin.site.register(models.Comment)

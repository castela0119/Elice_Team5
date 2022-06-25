from django.contrib import admin

from .models import Frequency, Keyword, Video

# Register your models here.

admin.site.register(Video)
admin.site.register(Keyword)
admin.site.register(Frequency)

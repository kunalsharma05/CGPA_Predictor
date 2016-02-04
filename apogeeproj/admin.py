from django.contrib import admin
from apogeeproj.models import *

class HiAdmin(admin.ModelAdmin):
    search_fields = ['project_name']


admin.site.register(Hi, HiAdmin)
# Register your models here.

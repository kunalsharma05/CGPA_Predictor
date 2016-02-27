from django.contrib import admin
from apogeeproj.models import *

class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name']

class LectureAdmin(admin.ModelAdmin):
    search_fields = ['Subject']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Profile)

# Register your models here.

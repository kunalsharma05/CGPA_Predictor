from django.db import models
from django.contrib.auth.models import User

class Hi(models.Model):
	project_type = models.CharField(max_length=100)
	project_name = models.CharField(max_length=200)
	class Meta:
		verbose_name_plural = 'experiences'
	def __unicode__(self):
		return str(self.project_name)    

class Subject(models.Model):
	name = models.CharField(max_length=100)
	class Meta:
		verbose_name_plural = 'subjects'
	def __unicode__(self):
		return str(self.name)    




# Create your models here.

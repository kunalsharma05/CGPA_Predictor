from django.db import models
from django.contrib.auth.models import User

# class Hi(models.Model):
# 	project_type = models.CharField(max_length=100)
# 	project_name = models.CharField(max_length=200)
# 	class Meta:
# 		verbose_name_plural = 'experiences'
# 	def __unicode__(self):
# 		return str(self.project_name)    

class Subject(models.Model):
	name = models.CharField(max_length=100)
	class Meta:
		verbose_name_plural = 'subjects'
	def __unicode__(self):
		return str(self.name)

class Lecture(models.Model):
	LECTYPES = (
		('Tutorial','Tutorial'),
		('Lecture','Lecture'),
		('Practical','Practical'),		
		)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	lec_type = models.CharField(max_length=20,choices=LECTYPES)
	week_no = models.IntegerField(blank = True, null = True)
	day_no = models.IntegerField(blank = True, null = True)
	attendence = models.BooleanField(default = False)
	evaluative = models.BooleanField(default = False)
	max_marks = models.IntegerField(blank = True, null = True)
	marks_obtained = models.IntegerField(blank = True, null = True)
	class Meta:
		verbose_name_plural = 'Lectures'
	def __unicode__(self):
		return str(self.subject)




# Create your models here.

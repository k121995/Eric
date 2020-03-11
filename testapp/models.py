from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class filedata(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	filename = models.CharField(max_length=50)
	upload_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.filename
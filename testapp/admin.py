from django.contrib import admin
from testapp.models import filedata
# Register your models here.

class filedataAdmin(admin.ModelAdmin):
	list_display = ['id','filename','upload_date']

admin.site.register(filedata,filedataAdmin)
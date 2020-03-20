from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class filedata(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)

	def upload_file(self, filename):
         return 'Files/%s/%s'%(self.id,  filename)

	filename = models.FileField(upload_to='upload_file', max_length=254)
	# archivo = models.FileField(upload_to = 'path/')
	upload_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.filename


	


class CsvFile(models.Model):
	Financial_Aid_System_Applicant_ID = models.CharField(max_length=20,null=True,blank=True)
	Total_Tuition =models.CharField(max_length=20,null=True,blank=True) 
	Recommended_Award=models.CharField(max_length=20,null=True,blank=True)
	Rec_Award_Perc_Tuition = models.CharField(max_length=20,null=True,blank=True)
	Children_in_Applicants_HH=models.CharField(max_length=20,null=True,blank=True) 
	Est_Household_Contribution =models.CharField(max_length=20,null=True,blank=True)
	Total_Income =models.CharField(max_length=20,null=True,blank=True)
	Total_Available_for_Tuition =models.CharField(max_length=20,null=True,blank=True)
	Total_Assets =models.CharField(max_length=20,null=True,blank=True) 	
	Total_Liabilities =models.CharField(max_length=20,null=True,blank=True) 	
	Total_Net_Worth=models.CharField(max_length=20,null=True,blank=True) 	
	P1_Alumni_Academy =models.CharField(max_length=20,null=True,blank=True) 	
	P1_Alumni_Camp=models.CharField(max_length=20,null=True,blank=True) 	
	P1_Alumni_Institute =models.CharField(max_length=20,null=True,blank=True) 	
	P1_Alumni_All_State =models.CharField(max_length=20,null=True,blank=True) 	
	P2_Alumni_Academy =models.CharField(max_length=20,null=True,blank=True) 
	P2_Alumni_Camp	=models.CharField(max_length=20,null=True,blank=True) 
	P2_Alumni_All_Stat=models.CharField(max_length=20,null=True,blank=True) 
	P2_Alumni_Institute= models.CharField(max_length=20,null=True,blank=True) 	
	Sum_Alum =models.CharField(max_length=20,null=True,blank=True) 	
	Grade =models.CharField(max_length=20,null=True,blank=True) 	
	Primary_Arts_Area =models.CharField(max_length=20,null=True,blank=True) 	
	Aid_Total_Need =models.CharField(max_length=20,null=True,blank=True) 	
	Aid_Merit =models.CharField(max_length=20,null=True,blank=True) 	
	Aid_Inst_Grant =models.CharField(max_length=20,null=True,blank=True) 	
	Sex =models.CharField(max_length=20,null=True,blank=True) 	
	Behavior_Review=models.CharField(max_length=20,null=True,blank=True)	
	Academic_Review=models.CharField(max_length=20,null=True,blank=True)	
	Health_Review =models.CharField(max_length=20,null=True,blank=True) 	
	Learning_Specialist_Review =models.CharField(max_length=20,null=True,blank=True) 	
	CAPS_Review =models.CharField(max_length=20,null=True,blank=True) 	
	Sum_Review =models.CharField(max_length=20,null=True,blank=True) 	
	Tuition_Default=models.CharField(max_length=20,null=True,blank=True) 	
	Art_Rating=models.CharField(max_length=20,null=True,blank=True)
	Accepted=models.CharField(max_length=20,null=True,blank=True) 	
	Attended_Camp=models.CharField(max_length=20,null=True,blank=True) 	
	Attended_Inst=models.CharField(max_length=20,null=True,blank=True) 	
	Attended_Sum=models.CharField(max_length=20,null=True,blank=True) 	
	Tuition_Remander=models.CharField(max_length=20,null=True,blank=True) 
	Total_FA=models.CharField(max_length=20,null=True,blank=True)
	Percent_FA=models.CharField(max_length=20,null=True,blank=True)	
	Enrolled=models.CharField(max_length=20,null=True,blank=True) 

	def __str__(self):
		return self.Financial_Aid_System_Applicant_ID
	
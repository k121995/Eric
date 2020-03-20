from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import views as login
import logging
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from .models import filedata,CsvFile
from django.conf import settings
# Create your views here.

import argparse
import time
import csv
import io
import os,shutil

from sklearn.model_selection import train_test_split
import sklearn.datasets
from sklearn.metrics import r2_score, classification_report, explained_variance_score
from autosklearn.classification import AutoSklearnClassifier

import autosklearn.regression
from tpot import TPOTRegressor
import numpy as np
from .main import report, do_sklearn,do_tpot
# WORK_DIR = '/home/user/eluellenml/project1/Files/'
WORK_DIR = settings.MEDIA_ROOT
# def Home(request):
#     # hello = "hiiiiiii"
#     return render(request, 'registration/dashboard.html',)



def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username="username", password=password).exists()
        if user is not None:        	
        	return redirect("upload/csv/")
        else:
            return HttpResponse("Not signed in")
    form = AuthenticationForm()
    return render(request = request,template_name = "registration/login.html",context={"form":form})



ENROLLED_ONLY = True
def load_ica_aid_opt(data_file_name,*args, **kwargs):
		data = []
		target = []

		print(f"[INFO] Loading dataset from {data_file_name}.")

		
		with open(data_file_name) as f:
			reader_file = csv.reader(f)
			# io_string = io.StringIO(reader)
			# next(io_string)
			# print(data_file,"################################################################################################################")
			# for row in reader_file:
			# 	# print(row,"################")
			# 	# print(row[2],row[1],"hellllllllllllllllllllllllllllll")
			# 	if row[1]!= "Total Tuition":
			# 		# print(row[0],row[1])
			# # 		# result = None
			# # 		# try:
			# 		obj,created = CsvFile.objects.update_or_create(Financial_Aid_System_Applicant_ID=row[0],
			# 						Total_Tuition=row[1],
			# 						Recommended_Award=row[2] ,	
			# 						Rec_Award_Perc_Tuition = row[3],
			# 						Children_in_Applicants_HH=row[4], 
			# 						Est_Household_Contribution =row[5],	
			# 						Total_Income =row[6]	 ,
			# 						Total_Available_for_Tuition =row[7] ,	 
			# 						Total_Assets =row[8] 	,
			# 						Total_Liabilities =row[9] 	,
			# 						Total_Net_Worth=row[10],
			# 						P1_Alumni_Academy =row[11],
			# 						P1_Alumni_Camp=row[12],
			# 						P1_Alumni_Institute =row[13] ,	
			# 						P1_Alumni_All_State =row[14] 		,
			# 						P2_Alumni_Academy =row[15],
			# 						P2_Alumni_Camp =row[16],
			# 						P2_Alumni_All_Stat=row[17] ,
			# 						P2_Alumni_Institute=row[18] 	,
			# 						Sum_Alum =row[19] 	,
			# 						Grade =row[20]	,
			# 						Primary_Arts_Area =row[21] 	,
			# 						Aid_Total_Need =row[22] 	,
			# 						Aid_Merit =row[23]	,
			# 						Aid_Inst_Grant =row[24] 	,
			# 						Sex =row[25] 	,
			# 						Behavior_Review=row[26] ,	
			# 						Academic_Review=row[27],					
			# 						Health_Review =row[28] ,	
			# 						Learning_Specialist_Review=row[29],
			# 						CAPS_Review =row[30],
			# 						Sum_Review =row[31] ,
			# 						Tuition_Default=row[32]	,
			# 						Art_Rating=row[33] ,
			# 						Accepted=row[34] ,
			# 						Attended_Camp=row[35],
			# 						Attended_Inst=row[36],
			# 						Attended_Sum=row[37],
			# 						Tuition_Remander=row[38],
			# 						Total_FA=row[39],
			# 						Percent_FA=row[40],
			# 						Enrolled=row[41])
			# 		print(obj,created)
					
					# get the total lines in the CSV -1 for headers
			samples = sum(1 for row in reader_file)-1

			f.seek(0)
			temp = next(reader_file)  # column headings/features
			feature_names = np.array(temp)
			# print(f"DEBUG: Feature names = {feature_names}")

			# We skip the first and last columns.
			unwanted_columns = 2
			if ENROLLED_ONLY:
			# We also don't want the Percent FA column
				unwanted_columns = 3
			# Subtract columns we don't want
			features = len(feature_names) - unwanted_columns			
			print(f"[INFO] Samples = {samples}, Features = {features}")
			print(samples)
			print(features)

			# Initialize two empty arrays for the CSV data
			data = np.empty((samples, features))
			print(	"++++++++++++++")
			target = np.empty((samples,))

			index=0
			for d in reader_file:
				# print(f"DEBUG: {index} = {str(d)}")
				enrolled = int(d[-1])


				if ENROLLED_ONLY and enrolled == 1:
					'''
					Data resides in CSV columns starting with 'Total Tuition'
					and ending with 'Tuition Remander' (formerly 'Percent FA')
					'''
					# dd
					data[index] = np.asarray(d[1:-2], dtype=np.float64)
					print(f"DEBUG: data = {str(d[1:-2])}")
					'''
					Target is 'Percent FA' (formerly the last column 'Enrolled')
					'''
					target[index] = np.asarray(d[-2], dtype=np.float64)
					print(f"DEBUG: target = {str(d[-2])}")
					index += 1

			d = data[:index]
			t = target[:index]
			return d,t
				
def report(X_test, y_test, classifier, type='sklearn'):
	r2={}
	# r3={}
	if type == 'sklearn':
		predictions = classifier.predict(X_test)
		# print("\n\n---- CLASSIFICATION REPORT ----")
		# print(classification_report(y_test, predictions))

		print("\n\n---- VARIANCE SCORE ----")
		print(explained_variance_score(y_test, predictions))

		print("\n\n---- MODELS ----")
		# r2['best_model']=classifier.show_models()
		print(classifier.show_models())

		print("\n\n---- STATISTICS ----")
		print(classifier.sprint_statistics())

		print("\n\n---- R2 SCORE ----")
		r2['result_set']=r2_score(y_test, predictions)
		print(r2,"yyyy")

		# print(r2_score(y_test, predictions))
		return r2


def do_sklearn(X,y):
	# os.rmdir(WORK_DIR +'/'+'File/ica_tmp',ignore_errors=True)

	print('[INFO] Splitting.')

	X_train, X_test, y_train, y_test = \
		train_test_split(X, y, random_state=1)

	print(f'[INFO] Train shape: {X_train.shape}')
	print(f'[INFO] Test shape: {X_test.shape}')

	print('[INFO] Finding best model...')
	start = time.time()
	# shutil.rmtree(WORK_DIR +'/'+'File/ica_tmp')
	# shutil.rmtree(WORK_DIR +'/'+'File/ica_tmp')
	# os.rmdir(WORK_DIR +'/'+'File/ica_out')
	automl = autosklearn.regression.AutoSklearnRegressor(
		time_left_for_this_task=120,
		per_run_time_limit=30,
		tmp_folder= WORK_DIR +'/'+'File/ica_tmp',
		# output_folder= WORK_DIR +'/'+'File/ica_out',
	)
	automl.fit(X_train, y_train)
	model_timing="[INFO] Elapsed time finding best model: "+str(time.time() - start)+"seconds."
	print(f'[INFO] Elapsed time finding best model: {time.time() - start} seconds.')
	print(model_timing)	
	y['data']=report(X_test, y_test, automl, 'sklearn')
	return y

def do_tpot(X,y):
    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, train_size=0.75, test_size=0.25)

    tpot = TPOTRegressor(generations=5, population_size=50, verbosity=2)
    tpot.fit(X_train, y_train)
    result=tpot.score(X_test, y_test)
    print(result,"########")		#print(tpot.score(X_test, y_test))
    tpot.export(WORK_DIR + '/tpot_ica_pipeline.py')
    return result
# def main():
#     # Setup our CLI to accept an argument to determine which
#     # algorithm to run.
#     parser = argparse.ArgumentParser(
#             description="Run sklearn or tpot on a dataset.")
#     parser.add_argument('--tpot', action='store_true', dest='run_tpot',
#             default=False, help="Run the TPOT regressor")
#     parser.add_argument('--debug', action='store_true', dest='debug',
#             default=False, help="Enable debugging.")
#     args = parser.parse_args()

#     X, y = upload_csv(re)

#     if args.run_tpot:
#         do_tpot(X,y)
#     else:
#         do_sklearn(X,y)

# from django.http import JsonResponse

def upload_csv(request):
	db={}
	# data=
	t=''
	s=''

	if request.method == "GET":
		print("GET DATA")
		return render(request,"registration/dashboard.html")
	if request.method == "POST":
		print("POST DATA")
		# q = request.POST['q']
		# os.rmdir(WORK_DIR +'/'+'File/ica_tmp')
		csv_file=request.FILES['csvfile']
		print(csv_file)
		if not csv_file.name.endswith('.csv'):
			return HttpResponse("THIS IS NOT A CSV FILE")

		with open(WORK_DIR + '/'+str(csv_file)) as f:
			data_set = csv.reader(f)
		# data_set = csv_file.reader()
			print(data_set)
			for row in data_set:
					# print(row,"################")
					# print(row[2],row[1],"hellllllllllllllllllllllllllllll")
					if row[1]!= "Total Tuition":
						# print(row[0],row[1])
				# 		# result = None
				# 		# try:
						obj,created = CsvFile.objects.update_or_create(Financial_Aid_System_Applicant_ID=row[0],
										Total_Tuition=row[1],
										Recommended_Award=row[2] ,	
										Rec_Award_Perc_Tuition = row[3],
										Children_in_Applicants_HH=row[4], 
										Est_Household_Contribution =row[5],	
										Total_Income =row[6]	 ,
										Total_Available_for_Tuition =row[7] ,	 
										Total_Assets =row[8] 	,
										Total_Liabilities =row[9] 	,
										Total_Net_Worth=row[10],
										P1_Alumni_Academy =row[11],
										P1_Alumni_Camp=row[12],
										P1_Alumni_Institute =row[13] ,	
										P1_Alumni_All_State =row[14] 		,
										P2_Alumni_Academy =row[15],
										P2_Alumni_Camp =row[16],
										P2_Alumni_All_Stat=row[17] ,
										P2_Alumni_Institute=row[18] 	,
										Sum_Alum =row[19] 	,
										Grade =row[20]	,
										Primary_Arts_Area =row[21] 	,
										Aid_Total_Need =row[22] 	,
										Aid_Merit =row[23]	,
										Aid_Inst_Grant =row[24] 	,
										Sex =row[25] 	,
										Behavior_Review=row[26] ,	
										Academic_Review=row[27],					
										Health_Review =row[28] ,	
										Learning_Specialist_Review=row[29],
										CAPS_Review =row[30],
										Sum_Review =row[31] ,
										Tuition_Default=row[32]	,
										Art_Rating=row[33] ,
										Accepted=row[34] ,
										Attended_Camp=row[35],
										Attended_Inst=row[36],
										Attended_Sum=row[37],
										Tuition_Remander=row[38],
										Total_FA=row[39],
										Percent_FA=row[40],
										Enrolled=row[41])
						print(obj,created,"ggggggggggggggggggggggggggggggg")	
		
		user_id = request.user.id
		print(user_id,"NO")
		userobj=User.objects.get(id=user_id)
		data = filedata.objects.create(user_id=userobj,filename=csv_file)		
		# input_dataset = WORK_DIR + '/'+str(csv_file)
		
		# print(input_dataset)
		# print(input_dataset,":DAAATA GO")
		# parser = argparse.ArgumentParser(
		# 	description="Run sklearn or tpot on a dataset.")
		# parser.add_argument('--tpot', action='store_true', dest='run_tpot',
		# 	default=False, help="Run the TPOT regressor")
		# parser.add_argument('--debug', action='store_true', dest='debug',
		# 	default=False, help="Enable debugging.")
		# args = parser.parse_args()
		# print(input_dataset,":DAAATA")
		input_dataset = WORK_DIR + '/'+str(csv_file)
		print(input_dataset)
		# print(input_dataset,":DAAATA GO")
		# parser = argparse.ArgumentParser(
		# 	description="Run sklearn or tpot on a dataset.")
		# parser.add_argument('--tpot', action='store_true', dest='run_tpot',
		# 	default=False, help="Run the TPOT regressor")
		# parser.add_argument('--debug', action='store_true', dest='debug',
		# 	default=False, help="Enable debugging.")
		# args = parser.parse_args()
		# print(input_dataset,":DAAATA")
		X, y = load_ica_aid_opt(input_dataset)
		# if q =='T':
		# 	db["value"]=do_tpot(X,y)
		# else:
		# 	db["value"]=do_sklearn(X,y)
		# if args.run_tpot:
		# 	do_tpot(X,y)
		# else:
		# data=do_sklearn(X,y)
		db["value"]=do_sklearn(X,y)
		print(db)
		shutil.rmtree(WORK_DIR +'/'+'File/ica_tmp',ignore_errors=True)		
		return render(request,'registration/dashboard.html',{'db':db['value']})
		# return JsonResponse(db['value'])	

		

# def Ajax_view(request):
# 	if request.method == 'GET':
# 		print('getdataaaaa')
# 	# if request.method == 'POST':	
# 		return render(request,"registration/dashboard.html")
# 	# if request.method == 'POST':	
# 	# # 	filename = request.Files['csv_file']
# 	# # 	print(filename)
# 	# 	return render(request,'registration/dashboard.html',)

# # return render(request,'registration/dashboard.html',{'db':db['value']})






from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import views as login
import logging
from django.contrib import messages
from django.urls import reverse
# Create your views here.

import argparse
import time
import csv
import io

from sklearn.model_selection import train_test_split
import sklearn.datasets
from sklearn.metrics import r2_score, classification_report, explained_variance_score
from autosklearn.classification import AutoSklearnClassifier

import autosklearn.regression
from tpot import TPOTRegressor
import numpy as np
from .main import report, do_sklearn,do_tpot

def Home(request):
    # hello = "hiiiiiii"
    return render(request, 'registration/dashboard.html',)



def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        seo_specialist = authenticate(username=username, password=password)
        if seo_specialist is not None:
            return render(request,'registration/dashboard.html')
        else:
            return HttpResponse("Not signed in")
    form = AuthenticationForm()
    return render(request = request,template_name = "registration/index.html",context={"form":form})



ENROLLED_ONLY = True
def upload_csv(request):
	d=None
	t=None
	s=''
	if request.method == "GET":
		print("GET DATA")
		return render(request,"registration/upload_csv.html")
	if request.method == "POST":
		print("POST DATA")
		s=request.FILES['csv_file']
		
		WORK_DIR = '/home/user/eluellenml/eluellenml/'
		re = WORK_DIR + str(s)
		# pa ="/home/user/eluellenml/"
		# re=pa+request.FILES['csv_file']
		# csv_file = request.POST['csv_file']
		# csv_file = request.path
		# print(csv_file, "jbdvhddddddddddddd")
		# return render(request, "registration/upload_csv.html")
		with open(re) as f:
			data_file = csv.reader(f)

			# get the total lines in the CSV -1 for headers
			samples = sum(1 for row in data_file)-1

			f.seek(0)
			temp = next(data_file)  # column headings/features
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

			# Initialize two empty arrays for the CSV data
			data = np.empty((samples, features))
			target = np.empty((samples,))

			index=0
			for d in data_file:
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
			return True
			# report(d,t)
			# print(d,t,"hello")
			# print(f"Target column - {feature_names[-2]}")
			# print(f"Data columns - {feature_names[1:-2]}")

	# print(s,"FILENAME")
	# return HttpResponse({"hh":d, "kk":t})
	        # report(d,t)
def report(X_test, y_test, classifier, type='sklearn'):
    if type == 'sklearn':
        predictions = classifier.predict(X_test)
        # print("\n\n---- CLASSIFICATION REPORT ----")
        # print(classification_report(y_test, predictions))

        print("\n\n---- VARIANCE SCORE ----")
        print(explained_variance_score(y_test, predictions))

        print("\n\n---- MODELS ----")
        print(classifier.show_models())

        print("\n\n---- STATISTICS ----")
        print(classifier.sprint_statistics())

        print("\n\n---- R2 SCORE ----")
        print(r2_score(y_test, predictions))



def do_sklearn(X,y):

    print('[INFO] Splitting.')

    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, random_state=1)

    print(f'[INFO] Train shape: {X_train.shape}')
    print(f'[INFO] Test shape: {X_test.shape}')

    print('[INFO] Finding best model...')
    start = time.time()
    automl = autosklearn.regression.AutoSklearnRegressor(
        time_left_for_this_task=120,
        per_run_time_limit=30,
        tmp_folder= WORK_DIR +'/ica_tmp',
        output_folder= WORK_DIR +'/ica_out',
    )
    automl.fit(X_train, y_train)
    print(f'[INFO] Elapsed time finding best model: {time.time() - start} seconds.')

    report(X_test, y_test, automl, 'sklearn')

def do_tpot(X,y):
    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, train_size=0.75, test_size=0.25)

    tpot = TPOTRegressor(generations=5, population_size=50, verbosity=2)
    tpot.fit(X_train, y_train)
    print(tpot.score(X_test, y_test))
    tpot.export(WORK_DIR + '/tpot_ica_pipeline.py')

def main():
    # Setup our CLI to accept an argument to determine which
    # algorithm to run.
    parser = argparse.ArgumentParser(
            description="Run sklearn or tpot on a dataset.")
    parser.add_argument('--tpot', action='store_true', dest='run_tpot',
            default=False, help="Run the TPOT regressor")
    parser.add_argument('--debug', action='store_true', dest='debug',
            default=False, help="Enable debugging.")
    args = parser.parse_args()

    X, y = upload_csv(re)

    if args.run_tpot:
        do_tpot(X,y)
    else:
        do_sklearn(X,y)



if __name__ == '__main__':
    main()














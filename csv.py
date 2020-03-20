import pandas as pd
data = pd.read_csv (r'/home/user/Desktop/ICA_Aid_Opt_CSV.csv')   
df = pd.DataFrame(data, columns= ['Financial Aid System Applicant ID','Total Tuition'])
print(df)
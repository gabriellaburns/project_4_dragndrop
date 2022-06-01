from flask import Flask, render_template, request
import os
import glob
import time
import pickle
import numpy as np

import app

# importing pandas module
import pandas as pd
  
#app = Flask(__name__)
def loop():

    list_of_files = glob.glob('/Users/gabriellaburns/Desktop/project_4_dragndrop/uploads/*') 
    latest_file = max(list_of_files, key=os.path.getctime)

    #latest_file = app.upload()

    # reading the data in the csv file
    df1 = pd.read_csv(latest_file)
    df1["prediction"] = ""
    df1["probability"] = ""

    df = df1.astype(str)


    for i in df["loan_type"]:
        df.replace("Conventional", '1000', inplace=True)
        df.replace("FHA Insured", '0100', inplace=True)
        df.replace("VA-guaranteed", '0010', inplace=True)
        df.replace("FSA/RHS (Farm Service Agency or Rural Housing Service)", '0001', inplace=True)

    for i in df["applicant_ethnicity"]:
        df["applicant_ethnicity"].replace("Hispanic or Latino", '10', inplace=True)
        df["applicant_ethnicity"].replace("Not Hispanic or Latino", '01', inplace=True)

    for i in df["co_applicant_ethnicity"]:
        df["co_applicant_ethnicity"].replace("Hispanic or Latino", '100', inplace=True)
        df["co_applicant_ethnicity"].replace("Not Hispanic or Latino", '010', inplace=True)
        df["co_applicant_ethnicity"].replace("No co-applicant", '001', inplace=True)

    for i in df["applicant_race_1"]:
        df["applicant_race_1"].replace("American Indian or Alaska Native", '10000', inplace=True)
        df["applicant_race_1"].replace("Asian", '01000', inplace=True)
        df["applicant_race_1"].replace("Black or African American", '00100', inplace=True)   
        df["applicant_race_1"].replace("Native Hawaiian or Other Pacific Islander", '00010', inplace=True)
        df["applicant_race_1"].replace("White", '00001', inplace=True)       
        
    for i in df["co_applicant_race_1"]:
        df["co_applicant_race_1"].replace("American Indian or Alaska Native", '100000', inplace=True)
        df["co_applicant_race_1"].replace("Asian", '010000', inplace=True)
        df["co_applicant_race_1"].replace("Black or African American", '001000', inplace=True)   
        df["co_applicant_race_1"].replace("Native Hawaiian or Other Pacific Islander", '000100', inplace=True)
        df["co_applicant_race_1"].replace("White", '000010', inplace=True)    
        df["co_applicant_race_1"].replace("No co-applicant", '000001', inplace=True)  

    for i in df["applicant_sex"]:
        df["applicant_sex"].replace("Male", '10', inplace=True)
        df["applicant_sex"].replace("Female", '01', inplace=True)

    for i in df["co_applicant_sex"]:
        df["co_applicant_sex"].replace("Male", '100', inplace=True)
        df["co_applicant_sex"].replace("Female", '010', inplace=True)
        df["co_applicant_sex"].replace("No co-applicant", '001', inplace=True)
    df


    inputs = []
    for i in range(len(df)): 
        input = []
        #loan amount
        loan_amount = df.iloc[i, 0] # for the input
        input.append(loan_amount)
        #income
        income = df.iloc[i, 1]
        input.append(income)
        #loan type
        loantype = df.iloc[i, 2]
        for x in loantype:
            input.append(x)
        #applicant ethnicity
        aeth = df.iloc[i, 3]
        for x in aeth:
            input.append(x)
        #coapplicant ethnicity
        coaeth = df.iloc[i, 4]
        for x in coaeth:    
            input.append(x)
        #applicant race
        arac = df.iloc[i, 5]
        for x in arac:
            input.append(x)
        #coapplicant race
        coarac = df.iloc[i, 6]
        for x in coarac:
            input.append(x)
        #applicant sex
        asex = df.iloc[i, 7]
        for x in asex:
            input.append(x)
        #coapplicant sex
        coasex = df.iloc[i, 8]
        for x in coasex:
            input.append(x)
        inputs.append(input)
    inputs


    model = pickle.load(open('resources/lr_classifier.pkl', 'rb'))       
    chance=0


    df_predictions = []
    df_prob = []

    for i in inputs:
        
        data = np.array(i)[np.newaxis, :]  # converts shape for model test
    # runs model on the data
        prob= model.predict_proba(data)
        predict = model.predict(data)
        #append prediction to df
        if predict == [1]:
            df_predictions.append("Likely will qualify")
        else:
            df_predictions.append("Unlikely to qualify.")

        #append prob to df
        if predict == [1]:
            chance = prob[0][1]
            df_prob.append(str((chance*100)) + '%')
        else:
            chance = prob[0][0]
            df_prob.append(str((chance*100)) + '%')


    df1['prediction'] = df_predictions
    df1['probability'] = df_prob


    df1.to_csv("table_calc.csv", index=False)

    #data = df1.to_dict(orient='records')

    data = df1
    return(data)

# route to html page - "table"
#@app.route('/')
#@app.route('/table')
#def table():
    
    # converting csv to html
  #  data = pd.read_csv("table_calc.csv")
 #   return render_template('tables.html', tables=[data.to_html()], titles=[''])
  
  
#f __name__ == "__main__":
  #  app.run(host="localhost", port=int("5000"))


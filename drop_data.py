# importing flask
from flask import Flask, render_template, request
import os
import glob
import time
  
# importing pandas module
import pandas as pd
  
  
app = Flask(__name__)
  
list_of_files = glob.glob('/Users/gabriellaburns/Desktop/project_4/uploads/*') 
latest_file = max(list_of_files, key=os.path.getctime)


# reading the data in the csv file
df = pd.read_csv(latest_file)
df.to_csv(latest_file, index=None)
  
  
# route to html page - "table"
@app.route('/')
@app.route('/table')
def table():
    
    # converting csv to html
    data = pd.read_csv(latest_file)
    return render_template('tables.html', tables=[data.to_html()], titles=[''])
  
  
if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))


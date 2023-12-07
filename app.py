from flask import Flask, render_template, request
from flask_cors import CORS,cross_origin
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import requests
import pandas as pd

app = Flask(__name__)


client = MongoClient('mongodb+srv://jaykumar002kori:GvlkAZqob1TdfrSz@cluster0.wxxmacs.mongodb.net/?retryWrites=true&w=majority')  
db = client['vehicals_database']  
collection = db['vehicals_data'] 

@app.route('/',methods=['GET'])
@cross_origin()
def homepage():
 # Read CSV data into a DataFrame
# df = pd.read_csv('products.csv', encoding='latin1')
# Convert DataFrame to list of dictionaries
#reviews = df.to_dict(orient='records')
    return render_template('index.html')

@app.route('/review',methods=['POST','GET']) 
@cross_origin()
def index():
    result_data=None
    if request.method=='POST':
        
        user_query=request.form.get('query')
        query_type=request.form.get()
        
        exists_data=collection.find_one({'query': user_query})
        
        if exists_data:
            result_data=exists_data['data']
        else:
            result_data=data_scrap(user_query)
            collection.update_one({'query': user_query}, {'$set':{"data": result_data}}, upsert=True)
    return render_template('test.html',result_data=result_data)      

  
def data_scrap(query):
    pass
    
    
    
    
if __name__ == '__main__':
    app.run(debug=True)
       






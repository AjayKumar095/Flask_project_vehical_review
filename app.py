from flask import Flask, render_template, request
from flask_cors import CORS,cross_origin
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import requests

app = Flask(__name__)


client = MongoClient('Paste_your_mongodb_client_id')  
db = client['vehicals_database']  
collection = db['vehicals_data'] 

@app.route('/',methods=['GET'])
@cross_origin()
def homepage():
    return render_template('index.html')

@app.route('/review',methods=['POST','GET']) 
@cross_origin()
def index():
    result_data=None
    if request.method=='POST':
        user_query=request.form.get('query')
        exists_data=collection.find_one({'query': user_query})
        
        if exists_data:
            result_data=exists_data['data']
        else:
             result_data = data_scrap(user_query)
             collection.update_one({'query': user_query}, {'$set': {'data': result_data}}, upsert=True)
    return render_template('review.html',result_data=result_data)      

  
def data_scrap(query):
    car_makes = [
    "aston-martin", "audi", "bajaj", "bentley", "bmw", "bugatti", "byd", "citroen", "ferrari", "fisker",
    "force-motors", "ford", "haval", "honda", "hyundai", "isuzu", "jaguar", "jeep", "kia", "lamborghini",
    "land-rover", "lexus", "lotus", "maserati", "maruti-suzuki", "mahindra", "mclaren", "mercedes-benz", 
    "mg-motor", "mini", "mitsubishi", "nissan", "ola-electric", "ora", "pmv", "porsche", "pravaig", "renault",
    "rolls-royce", "skoda", "strom-motors", "tata", "tesla", "toyota", "volkswagen"
    ]

    try:
        
       if query in car_makes:
           main_url=main_url="https://www.zigwheels.com/"+query+"-cars/"
       else:
           return render_template("index.html")
       
    except Exception:
        print("Somthing went wrong")
        print(Exception)
        
    try:
        response=requests.get(main_url)
        html_source=bs(response.text,'html.parser')
        sorted_html_page=html_source.find_all('li', {'class':"col-lg-6 txt-c rel modelItem"})
        links=[]
        for i in sorted_html_page:
            links.append(i.find_all('a',{"data-track-label":"launched-model-name"}))
        filtered_links=[sublist for sublist in links if sublist]  
        combined_links = list(zip(*filtered_links))
        html_content=[]
        for i in combined_links:
            if type(i)==tuple:
                for j in i:
                    html_content.append(j)
        link_list=[]            
        for i in html_content:
           link_list.append(i['href'])
        link_list
        
        
        data=[]  
        for link in link_list:
            try:
               # Collecting Model name of car.
               response=requests.get(link)
               html_content=bs(response.text, 'html.parser')
               html_links=html_content.find('div',{'class':"rel i-b mn-head model-heading-rating"})
               string_link=str(html_links)
               string_link
               soup=bs(string_link, 'html.parser')
               model=soup.div.h1.text
               model=model.replace('\n','')
            except Exception:
                print(Exception)    
        
        
        
            try:
               # Collecting price of respective mode.
               response=requests.get(link)
               html_content=bs(response.text, 'html.parser')
               html_links=html_content.find('span',{'class':"fnt-black fnt-18 b modelPrice-fnt"})
               string_link=str(html_links)
               string_link
               soup=bs(string_link, 'html.parser')
               price=soup.span.text
               price=price.replace('\n','')
            except Exception:
                print(Exception)   
        
    
            try:
                # Collecting specifications for respective modal.
               response=requests.get(link)
               html_content=bs(response.text, 'html.parser')
               html_links=html_content.find('ul',{'class':"pb-20"})
               html_links=str(html_links)
               soup=bs(html_links, 'html.parser')
               Specifications = soup.find_all('li')
               specifications_strings = []
               for li in Specifications:
                   li_text = li.find(string=True, recursive=False).strip()
                   span_text = li.span.get_text(strip=True)
                   specification_string=(f"{li_text}: {span_text}")
                   specifications_strings.append(specification_string)
               specifications_string_for_link = '\n'.join(specifications_strings)
               specifications_string_for_link=specifications_string_for_link.replace('\n',', ')
            
            except Exception:
                print(Exception)      
            
            try:
                # Collecting features for respective model.
                 response=requests.get(link)
                 html_content=bs(response.text, 'html.parser')
                 html_links=html_content.find('ul',{'id':"keyFeatures"})
                 html_links=str(html_links)
                 soup=bs(html_links,'html.parser')
                 Features=soup.find_all('li')
                 features_string = '\n'.join(feature.text for feature in Features) 
                 features_string=features_string.replace('\n',', ')
            except Exception:
                print(Exception)
                
            # appending car details in dict.    
            mydict={'Model':model, 'Price':price, 'Specifications':specifications_string_for_link, 'Features':features_string} 
            data.append(mydict)    
        return data     
    
    except Exception:
        print("Somthing went wrong")
        print(Exception)     
        
if __name__ == '__main__':
    app.run('0.0.0.0',port=8000)
       

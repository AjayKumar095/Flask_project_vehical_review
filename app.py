from flask import Flask, render_template, request
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import requests

print("What you want to search for cars or bike:")
print("1 for car\n2 for bikes")
user_input=int(input("Enter your choice:"))

if user_input==1:
    car_brand=input("Enter the car companie name")
    #car_model=input("Enter the car model name if any or enter black space")
    main_url="https://www.zigwheels.com/"+car_brand+"-cars/"

elif user_input==2:
    bike_brand=input("Enter the bike companie name")
    #bike_model=input("Enter the bike model name if any or enter black space")
    main_url="https://www.zigwheels.com/"+bike_brand+"-bikes/"

else:
    print(None)    

response=requests.get(main_url)

html_source=bs(response.text,'html.parser')
sorted_html_page=html_source.find('li', {'class':"col-lg-6 txt-c rel modelItem"})

links=[]
for i in sorted_html_page:
    links.append(i.find_all('a',{"data-track-label":"launched-model-name"}))
       
combined_links = list(zip(*links))
#print(combined_links)
html_content=[]
for i in combined_links:
    if type(i)==tuple:
        for j in i:
            html_content.append(j)
html_content_links=[]            
for i in html_content:
   html_content_links.append(i['href'])

sorted_link_review=[]
for review_page in html_content_links:
    review_page_response=requests.get(review_page)
    review_page_html=bs(review_page_response.text,"html.parser")
    sorted_review_page_data=review_page_html.find_all('ul', {'class':"txt-c mt-0 mb-0 fnt-14 mmv-nv"})
    sorted_link_review.append(sorted_review_page_data)

combined_links_review=list(zip(*sorted_link_review))   
combined_links_review_list=[]

for k in combined_links_review:
    if type(k) == tuple:
        for l in k:
            combined_links_review_list.append(l)
combined_links_review_list  

     





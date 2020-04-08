import urllib.request

f = open("list2019.html", "wb") #wb = binary write

response = urllib.request.urlopen('https://www.boxofficemojo.com/daily/2019/?view=year')
html=response.read()

f.write (html)
# print (html)
f.close() #do not forget to close it

#__________________________

from bs4 import BeautifulSoup
import os
import pandas as pd
import glob
import time
import numpy as np
import random

if not os.path.exists ("parsed_files"):
    os.mkdir("parsed_files")
df=pd.DataFrame()


for one in glob.glob("html_files/*.html"):
    print("parsing: ",one)
    # scraping_time=os.path.basename(one).replace("list", "").replace(".html", "")
    f = open(one, "r")
    soup=BeautifulSoup(f.read(), "html.parser")
    f.close()
 
    m_table = soup.find('div', {"id" : 'table'})
    m_rows =m_table.find_all("tr")

    for r in m_rows:
    	found_date_urls = [link["href"] for link in r.find_all("a", href=True) if link["href"].startswith("/date")]
    	found_name_urls = [link.string for link in r.find_all("a", href=True) if link["href"].startswith("/release")]
    	df=df.append({"link":found_date_urls,"name":found_name_urls}, ignore_index=True)
df.to_csv("parsed_files/dataset_names11.csv")

#__________________________________

df2=pd.read_csv("parsed_files/dataset_names11.csv")
df3=df2.drop_duplicates("name")
# print(df3)
df3.to_csv("parsed_files/dataset_names12.csv")



#___________________________________

if not os.path.exists("deep_link_html"):
	os.mkdir("deep_link_html")

df = pd.read_csv("parsed_files/dataset_names234.csv")



for link in df['link']:
	
	filename = link.replace("/","").replace("date","")
	if os.path.exists("deep_link_html/" + filename + ".html"):
		print(filename + "exists")
	else:
		print("Downloading: ", filename)	
		f = open("deep_link_html/" + filename + ".html.temp", "wb")
		response = urllib.request.urlopen('http://boxofficemojo.com' + link)
		html = response.read()
		f.write(html)
		f.close()
		os.rename("deep_link_html/" + filename + ".html.temp","deep_link_html/" + filename + ".html")
		timedelay = random.randrange(1,2)
		time.sleep (timedelay) 

#________________________________________


if not os.path.exists ("parsed_files2"):
    os.mkdir("parsed_files2")
df3=pd.DataFrame()


for one in glob.glob("deep_link_html/*.html", recursive=True):

    try:
    	print("parsing: ",one)
    	f = open(one, "r")
    	soup=BeautifulSoup(f.read(), "html.parser")
    	f.close()
    	m_table = soup.find('div', {"id" : 'table'})
    	m_rows =m_table.find_all("tr")
    	for r in m_rows:
    		# found_text=[link.string for link in r.find_all('a')]
    		# found_name_urls = [link.string for link in r.find_all("a", href=True) if link["href"].startswith("/release")]
    		found_number=[link.get_text() for link in r.find_all("td")]
    		# print(found_number)
    		df3=df3.append({"headers":found_number}, ignore_index=True)
    except:
    	pass
df3.to_csv("parsed_files2/dataset_two.csv")

#___________________________________________________
df2=pd.read_csv("parsed_files2/dataset_two2.csv")
df3=df2.drop_duplicates("name")

# print(df3)
df3.to_csv("parsed_files2/final_output.csv")







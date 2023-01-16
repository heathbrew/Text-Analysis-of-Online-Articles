import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
#from urllib.request import urlopen
import time 
from urllib.error import HTTPError

def try_again(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        response = requests.get(url, headers=headers)
        html_content = response.text
        
        # Create a BeautifulSoup object
        soup = BeautifulSoup(html_content, 'html.parser')
        # print(soup.prettify())
        article_text = soup.find("div", class_="td-post-content").text
        return article_text
    except ConnectionAbortedError as e:
        print("ConnectionAbortedError occurred, trying again in 0.5 seconds")
        #time.sleep(2)
        try_again(url)
    except HTTPError as e:
        print("HTTPError occurred, trying again in 0.5 seconds")
        #time.sleep(2)
        try_again(url)
    except AttributeError as err:
        return "skip"        
    except Exception as e:
        #'NoneType' object has no attribute 'text'
        print(e)
        #time.sleep(2)
        try_again(url) 

# Read data from input.xlsx file
data = pd.read_excel('input.xlsx')


# Create a new directory called "extract"
if not os.path.exists("extract"):
    os.makedirs("extract")

# Iterate over each row in the data
for index, row in data.iterrows():
    url = row['URL']
    url_id = row['URL_ID']
    if not os.path.exists("extract/{url_id}.txt"):
        content = str(try_again(url))
        if content == "skip":
             with open(f'extract/{url_id}.txt', 'w') as f:
                    f.write("")
        else:
            # Save the extracted article text to a file with the URL_ID as its file name
                with open(f'extract/{url_id}.txt', 'w') as f:
                    ascii_text = content.encode('ascii', 'ignore').decode()
                    f.write(ascii_text)

                
            # break

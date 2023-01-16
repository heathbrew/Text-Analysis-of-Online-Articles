import requests
from bs4 import BeautifulSoup

# Fetch the HTML content of the URL
url = "https://insights.blackcoffer.com/how-machine-learning-will-affect-your-business/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
response = requests.get(url, headers=headers)
#response = requests.get(url)
html_content = response.text

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')
# print(soup.prettify())
article_text = soup.find("div", class_="td-post-content").text
print(article_text)

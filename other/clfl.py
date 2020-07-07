import requests

word = 'privet'
word2 = 'vasya'
url = f'http://127.0.0.1:5000/hello/{word}'
response = requests.post(url, json= {'dog':'собака'})

print(response.content)
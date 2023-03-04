from requests import get, put, delete, post
from pprint import pprint

url = 'http://localhost:8080/api/'
pprint(get(url + 'jobs').json())
pprint(get(url + 'job/1').json())
pprint(get(url + 'job/999').json())
pprint(get(url + 'job/q').json())
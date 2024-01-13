import requests
import csv
import os.path
from time import sleep


api_key_list = [
    "3ae8e9e5bc2862aac38f9a3adae1592bda78c9ec",
    "89fad834cfa823e4e7a715c734ca36467c9d11ba",
    "a3cad565bf2da0e7140dad4835ba532135c5f7ac",
    "aca19ac6c6a1063493c674dcb7dbca96e1ca3776",
    "0b3a57da6ddebcf4a3a5047418556c613a61296d",
    "9ed7a74500caba5031604613b0d78f012613832e",
    "a7b3aea6b49d1b871965cf44513b460f7b7d9242",
    "c3bb7803a74b4965526e29f01f53399f916f1109",
]

api_key_number = 0  # start using api key number 0 (first position)

base = "http://streeteasy.com/nyc/api/sales/data?criteria="

housing_type = "condos"
num_bedrooms = 3

housing_type_arg = "housing_type:%s" % housing_type

num_bedrooms_arg = "beds:%s" % num_bedrooms

criteria = "|".join([num_bedrooms_arg, housing_type_arg])
key_and_format = "&key=%s&format=json" % api_key_list[api_key_number]
api_request = base + criteria + key_and_format

print(api_request)

response = requests.get(api_request)
data = response.json()
print(data)

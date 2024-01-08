#By: Glenda Ascencio										Microsoft Research Summer School
import requests
import csv
import os.path
from time import sleep

school_list = ['ps282-brooklyn', 'ps321-brooklyn', 'ps107-brooklyn', 'ps39-brooklyn', 'ps124-brooklyn', 'ps10-brooklyn']

housing_types_of_interest = ['condos', 'coops', 'miltifamily', 'houses']
num_bedrooms_of_interest = [1, 2, 3]
sqfts_of_interest = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]

api_key_list = [
    '3ae8e9e5bc2862aac38f9a3adae1592bda78c9ec',
    '89fad834cfa823e4e7a715c734ca36467c9d11ba',
    'a3cad565bf2da0e7140dad4835ba532135c5f7ac',
    'aca19ac6c6a1063493c674dcb7dbca96e1ca3776',
    '0b3a57da6ddebcf4a3a5047418556c613a61296d',
    '9ed7a74500caba5031604613b0d78f012613832e',
    'a7b3aea6b49d1b871965cf44513b460f7b7d9242',
    'c3bb7803a74b4965526e29f01f53399f916f1109'
]

api_key_number = 0 #start using api key number 0 (first position)
api_key_used_counter = 0 #times current api key has been used

base = 'http://streeteasy.com/nyc/api/sales/data?criteria='



for school in school_list: #go through defined schools
    school_arg = 'school:%s' % school
    filename = '%s_school.csv' % school

    # check for existing file
    # if exists, don't write header and create a set of previously covered criteria
    previous_criteria = set()
    write_header = 1
    if os.path.exists(filename):
	write_header = 0
        with open(filename, 'r') as f:
                reader = csv.DictReader(f, quotechar='"', delimiter=',')
                previous_criteria = set([row["criteria"] + "|housing_type:" + row["housing"] for row in reader])

    with open(filename, 'a') as f:
        for housing_type in housing_types_of_interest: #go through defined housing
	        housing_type_arg = 'housing_type:%s' % housing_type
            for num_bedrooms in num_bedrooms_of_interest: # go through 1,2,3 bedrooms
                num_bedrooms_arg = 'beds:%s' % num_bedrooms
                for sqft in sqfts_of_interest: # go through defined sqft
	    	        sgft_arg = 'sqft>%s' % sqft
                    criteria = "|".join([sgft_arg, school, beds, housing_type])
                    if criteria not in previous_criteria:
                        key_and_format = '&key=%s&format=json'% api_key_list[api_key_number]
                        api_request = base + criteria + key_and_format
                        api_key_used_counter = api_key_used_counter + 1
                        if(api_key_used_counter >= 100):
                            api_key_used_counter = 0
                            api_key_number = api_key_number + 1
                        #api_request = base+housing_type+sgft+beds+school+key_and_format #create api request based on the parameters
                        print api_request
                        print "apikey:", api_key_number, "numTimesUsed:", api_key_used_counter

                        response = requests.get(api_request)
                        sleep(2)
                        data = response.json()
                        print data
                        dict2 = {'school':school,'housing':housing_type, 'sqft':sq_ft, 'beds':num_bedrooms} #creating dict to separate the adjusted criteria column to dif columns
                        dict2.update(data)
                        w = csv.DictWriter(f, dict2.keys(), quotechar='"', delimiter=',')
                        if write_header == 1:#to write header only one time check if flag is 0
                                w.writeheader()
                                write_header = 0
                        w.writerow(dict2)
                        f.flush()# see line by line in a file
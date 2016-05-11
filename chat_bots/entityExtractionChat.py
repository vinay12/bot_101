import json
from pprint import pprint
import math
from datetime import datetime
import requests
import config

url = "http://console.arya.ai/api/v2/entityExtraction/query?access_token="+config.access_token+"&m_key="+config.m_key+"&app="+config.app_name
#print url
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
threshold_reprints = 3

def original_query():
    query = raw_input("Enter your name, last job location, name of the organization, your last salary, your joining date and ending date\n")
    original_data = {}
    response = {}
    original_data["task"] = ["person", "organization", "date", "location", "money"]
    original_data["query"] = query
    data = json.dumps(original_data)
    #print data
    #print json.loads(requests.request("POST", url, data=data)).text
    response = requests.request("POST", url, data=data, headers=headers)
    return response

def name_query():
    name_data = {}
    name_data["task"] = ["person"]
    name_data["query"] = raw_input("We didn't catch your name. Please enter your name again\n")
    data = json.dumps(name_data)
    return requests.request("POST", url, data=data, headers=headers)

def org_query():
    org_data = {}
    org_data["task"] = ["organization"]
    org_data["query"] = raw_input("We couldn't find your previous organization's name. Please enter again\n")
    data = json.dumps(org_data)
    return requests.request("POST", url, data=data, headers=headers)

def date_query():
    date_data = {}
    date_data["task"] = ["date"]
    date_data["query"] = raw_input("We couldn't get either one or both of your joining date and ending date. Please enter again\n")
    data = json.dumps(date_data)
    #print "Date is "
    #print data
    return requests.request("POST", url, data=data, headers=headers)

def sal_query():
    sal_data = {}
    sal_data["task"] = ["money"]
    sal_data["query"] = raw_input("We couldn't catch you salary. Will you be kind enough to enter it again?\n")
    data = json.dumps(sal_data)
    return requests.request("POST", url, data=data, headers=headers)

def loc_query():
    loc_data = {}
    loc_data["task"] = ["location"]
    loc_data["query"] = raw_input("We didn't ask where you stayed. Will you tell us?\n")
    data = json.dumps(loc_data)
    return requests.request("POST", url, data=data, headers=headers)


def main():
    original_response = original_query();
    for i in range(0, threshold_reprints-1):
        if(original_response is None):
            original_response = original_query()

    original_response_data = original_response.json()
    #print(original_response_data["success"])
    #specific cases
    #name
    person_response = {}
    if(len(original_response_data["person"])==0):
        person_response = name_query()
        person_response_data = person_response.json()
        for i in range(0, threshold_reprints-1):
            if(len(person_response_data['person'])==0):
                person_response = name_query()
                person_response_data = person_response.json()

        if(len(person_response_data["person"])>0):
            print("Hello")
            print(person_response_data["person"])

    #location
    if(len(original_response_data["location"])==0):
        loc_response = loc_query()
        loc_response_data = loc_response.json()
        for i in range(0, threshold_reprints-1):
            if(len(loc_response_data['location'])==0):
                loc_response = loc_query()
                loc_response_data = loc_response.json()

        if(len(loc_response_data["location"])>0):
            print("So you were at ")
            print(loc_response_data["location"])


    org_response = {}
    #organization name
    if(len(original_response_data['organization'])==0):
        org_response = org_query()
        org_response_data = org_response.json()
        for i in range(0, threshold_reprints-1):
            if(len(org_response_data['organization'])==0):
                org_response = org_query()
                org_response_data = org_response.json()
 
        if(len(org_response_data['organization'])>0):
            print("We hope your journey at ")
            print(org_response_data["organization"])
            print("was good")


    #joining date/ending date
    if(len(original_response_data['date'])<2):
        date_response = date_query()
        date_response_data = date_response.json()
        for i in range(0, threshold_reprints-1):
            if('date' in date_response_data and len(date_response_data['date'])>=0 and len(date_response_data['date'])+len(original_response_data['date'])<2):
                print "Date not found"
                date_response = date_query()
                date_response_data = date_response.json()

    if 'date' in date_response_data and len(date_response_data['date'])==2:
        date1 = date_response_data['date'][0][0]
        #print date1
        date2 = date_response_data['date'][1][0]
	dob1 = ""
	dob2 = ""
	try:        
		dob1 = datetime.strptime(date1, "%Y")
       		dob2 = datetime.strptime(date2, "%Y")
		if(dob1<dob2):
		    print "Your joining date was "
		    print dob1
		    print " and ending date was " 
		    print dob2
		else:
		    print "Your joining date was "
		    print dob2
		    print " and ending date was " 
		    print dob1
	except Exception, e:
		print "Invalid dates"

    elif 'date' in date_response_data and len(date_response_data['date'])==1:
        date1 = date_response_data['date'][0]
        date2 = original_response_data['date'][0]
	dob1 = ""
	dob2 = ""	
	try:
        	dob1 = datetime.strptime(date1, "%Y")
        	dob2 = datetime.strptime(date2, "%Y")
		if(dob1<dob2):
		    print "Your joining date was "
		    print dob1
		    print " and ending date was " 
		    print dob2
		else:
		    print "Your joining date was "
		    print dob2
		    print " and ending date was " 
		    print dob1
	except Exception, e:
		print "Invalid dates"
        

    #salary
    if(len(original_response_data["money"])==0):
        sal_response = sal_query()
        sal_response_data = sal_response.json()
        for i in range(0, threshold_reprints-1):
            if(len(sal_response_data['money'])==0):
                sal_response = sal_query()
                sal_response_data = sal_response.json()

        if(len(sal_response_data["money"])>0):
            print(sal_response_data["money"])
            print(" is a lot of money! Congrats")


if (__name__ == '__main__'):
    main()

"""
Albert Einstein started at Apple Inc. for usd 3000. I stayed at California, USA.
I joined on 12 May 2015 and ended the job on June 2016

"""
         

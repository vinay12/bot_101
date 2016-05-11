import json
from pprint import pprint
import math
from datetime import datetime
import requests
import config

url = "http://console.arya.ai/api/v2/entityExtraction/query?access_token="+config.access_token+"&m_key="+config.m_key+"&app="+config.app_name
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
url_intent = "http://console.arya.ai/api/v2/faq/query?access_token=&m_key=IntentClassChatBot&app=TestChatBox"
threshold_reprints = 3

def college_chat_begin(this_intent):
    original_data = {}
    query = raw_input("Please enter your name, your college's name, its location, your joining date and your graduation date\n")
    original_data["task"] = ["person", "organization", "date", "location"]
    original_data["query"] = query
    data = json.dumps(original_data)
    response = requests.request("POST", url, data=data, headers=headers)
    hotel_chat_continue(response, this_intent)

def hotel_chat_begin(this_intent):
    original_data = {}
    query = raw_input("Please enter your name, the name of the hotel you'd like to book, the hotel's location, the check-in and check-out dates of booking and the money you'd like to spend\n")
    original_data["task"] = ["person", "organization", "date", "location", "money"]
    original_data["query"] = query
    data = json.dumps(original_data)
    response = requests.request("POST", url, data=data, headers=headers)
    college_chat_continue(response, this_intent)

def hotel_chat_continue(r, this_intent):
    response = r.json()
    #name
    if(len(response["person"])==0):
        person_response = name_query()
        person_response_data = person_response.json()
        for i in range(0, threshold_reprints-1):
            if(len(person_response_data['person'])==0):
                person_response = name_query()
                person_response_data = person_response.json()

        if(len(person_response_data["person"])>0):
            print("Hello")
            print(person_response_data["person"])

    #organization name
    if(len(response['organization'])==0):
        org_response = org_query()
        org_response_data = org_response.json()
        for i in range(0, threshold_reprints-1):
            if(len(org_response_data['organization'])==0):
                org_response = org_query()
                org_response_data = org_response.json()
 
        if(len(response['organization'])>0):
            print("We hope your stay at ")
            print(response["organization"])
            print("was good")

    #location
    if(len(response["location"])==0):
        loc_response = loc_query(this_intent)
        loc_response_data = loc_response.json()
        for i in range(0, threshold_reprints-1):
            if(len(loc_response_data['location'])==0):
                loc_response = loc_query(this_intent)
                loc_response_data = loc_response.json()

        if(len(loc_response_data["location"])>0):
            print("So you were at ")
            print(loc_response_data["location"])

    #joining date/ending date
    if(len(response['date'])<2):
        date_response = date_query(this_intent)
        date_response_data = date_response.json()
        for i in range(0, threshold_reprints-1):
            if('date' in date_response_data and len(date_response_data['date'])>=0 and len(date_response_data['date'])+len(response['date'])<2):
                print "Date not found"
                date_response = date_query(this_intent)
                date_response_data = date_response.json()

    if 'date' in date_response_data and len(date_response_data['date'])==2:
        date1 = date_response_data['date'][0][0]
        print date1
        date2 = date_response_data['date'][1][0]
        dob1 = datetime.strptime(date1, "%Y")
        dob2 = datetime.strptime(date2, "%Y")
        if(dob1<dob2):
            print "Your check-in date was "
            print dob1
            print " and check-out date was " 
            print dob2
        else:
            print "Your check-in date was "
            print dob2
            print " and check-out date was " 
            print dob1

    elif 'date' in date_response_data and len(date_response_data['date'])==1:
        date1 = date_response_data['date'][0]
        date2 = response['date'][0]
        dob1 = datetime.strptime(date1, "%Y")
        dob2 = datetime.strptime(date2, "%Y")
        if(dob1<dob2):
            print "Your check-in date was "
            print dob1
            print " and check-out date was " 
            print dob2
        else:
            print "Your check-in date was "
            print dob2
            print " and check-out date was " 
            print dob1


def college_chat_continue(r, this_intent):
    response = r.json()
    #name
    if(len(response["person"])==0):
        person_response = name_query()
        person_response_data = person_response.json()
        for i in range(0, threshold_reprints-1):
            if(len(person_response_data['person'])==0):
                person_response = name_query()
                person_response_data = person_response.json()

        if(len(person_response_data["person"])>0):
            print("Hello")
            print(person_response_data["person"])

    #organization name
    if(len(response['organization'])==0):
        org_response = org_query()
        org_response_data = org_response.json()
        for i in range(0, threshold_reprints-1):
            if(len(org_response_data['organization'])==0):
                org_response = org_query()
                org_response_data = org_response.json()
 
        if(len(org_response_data['organization'])>0):
            print("We hope your stay at ")
            print(org_response_data["organization"])
            print("will be enjoyable")

    #location
    if(len(response["location"])==0):
        loc_response = loc_query(this_intent)
        loc_response_data = loc_response.json()
        for i in range(0, threshold_reprints-1):
            if(len(loc_response_data['location'])==0):
                loc_response = loc_query(this_intent)
                loc_response_data = loc_response.json()

        if(len(loc_response_data["location"])>0):
            print("So your hotel is at ")
            print(loc_response_data["location"])

    #joining date/ending date
    if(len(response['date'])<2):
        date_response = date_query(this_intent)
        date_response_data = date_response.json()
        for i in range(0, threshold_reprints-1):
            if('date' in date_response_data and len(date_response_data['date'])>=0 and len(date_response_data['date'])+len(response['date'])<2):
                print "Date not found"
                date_response = date_query(this_intent)
                date_response_data = date_response.json()

    if 'date' in date_response_data and len(date_response_data['date'])==2:
        date1 = date_response_data['date'][0][0]
        print date1
        date2 = date_response_data['date'][1][0]
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

    elif 'date' in date_response_data and len(date_response_data['date'])==1:
        date1 = date_response_data['date'][0]
        date2 = response['date'][0]
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


def date_query(this_intent):
    date_data = {}
    date_data["task"] = ["date"]
    if(this_intent=="college"):
        date_data["query"] = raw_input("We couldn't get either one or both of your joining date and graduation date. Please enter again\n")
    elif(this_intent=="hotel"):
        date_data["query"] = raw_input("We couldn't get the your check-in and check-out dates. Please enter again\n")
    data = json.dumps(date_data)
    #print "Date is "
    #print data
    return requests.request("POST", url, data=data, headers=headers)

def sal_query(this_intent):
    sal_data = {}
    sal_data["task"] = ["money"]
    if(this_intent=="hotel"):
        sal_data["query"] = raw_input("We couldn't catch you budget. Will you be kind enough to enter it again?\n")
    data = json.dumps(sal_data)
    return requests.request("POST", url, data=data, headers=headers)

def loc_query(this_intent):
    loc_data = {}
    loc_data["task"] = ["location"]
    if(this_intent=="college"):
        loc_data["query"] = raw_input("We didn't ask where you stayed. Will you tell us?\n")
    elif(this_intent=="hotel"):
        loc_data["query"] = raw_input("We didn't ask where the hotel is. Will you tell us?\n")
    data = json.dumps(loc_data)
    return requests.request("POST", url, data=data, headers=headers)

def intent_query(): 
    intent_data = {}
    intent_data["query"] = raw_input("What do you want to do? Currently I can help you with hotel bookings and storing your college information.\n")
    intent_data["num_res"] = "1"
    data = json.dumps(intent_data)
    #pprint(data)
    return requests.request("POST", url_intent, data=data, headers=headers)

def main():
    this_intent = ""
    intent_response = intent_query()
    intent_response_data = intent_response.json()
    if(intent_response_data["success"]):
        #print intent_response_data["success"]
        #pprint(intent_response_data)
        try:
            this_intent = intent_response_data["response"][0]["answer"]
            print this_intent
        except Exception, e:
            print "No such json object in intent_response_data"
    else:
        print "Intent Classification failed"

    if(this_intent=="hotel"):
        print "So its related to a hotel booking... ok!"
        hotel_chat_begin(this_intent)
    elif(this_intent=="college"):
        print "So its related to your college studies... ok!"
        college_chat_begin(this_intent)


if (__name__ == '__main__'):
    main()
         

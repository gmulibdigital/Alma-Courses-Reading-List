
from http import HTTPStatus
import urllib.request # instead of urllib2 like in Python 2.7
from urllib.error import HTTPError,URLError
import os
import json
from json import JSONDecodeError

BASE_URL = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/courses'


#API_KEY = {} need to fill it from api_key.ini

os.environ['DJANGO_SECRET_KEY'] = 'pds)t&(axu+xvhy@7ncd@zggr=7k2&nu^$m^(mv0au=)v2=0)m'

def getJsonData(requestUrl):
    try:
        coursesData = {}
        webUrl = urllib.request.urlopen(requestUrl)
        print ("request url  =" + requestUrl)
        if (webUrl.getcode() == HTTPStatus.OK):
            data = webUrl.read()
            coursesData = json.loads(data.decode("utf-8"))
    except HTTPError as err:
            print (str(webUrl.getcode()))
    except URLError as err:
            print("server is down..." + err.name())

    return coursesData


def main():
    offset = 0
    total  = 100
    context = {
        'course' : [],
    }

    while total - offset > 0 :
        urlData = "{}?&limit=100&offset={}&status=active&order_by=code%2Csection&direction=ASC&format=json&view=full&apikey={}".format(BASE_URL,offset,API_KEY)
        obj = getJsonData(urlData)
        total = obj['total_record_count']
        offset +=100  #increase offset to fetch remaining data
        for i in obj["course"]: 
            if i['campus']: #only show the first campus info
                i['address'] = i['campus'][0]['campus_code']['value']
            else:
                i['address'] = "TBD"
            
            if i['instructor']:
                i['teacher'] = i['instructor'][0]['last_name']
            else:
                i['teacher'] = "TBD"

            o = getCitationDataFromCourseId(i['id'])
            i['citations'] = o['citations']
        
        context['course']+=obj['course'] #attach to context list

    print("total records = " + str(len(context['course'])))
    
    try:
        with open('courses.txt', 'w') as json_file:   #write to json file
            json.dump(context, json_file, indent=2)
            json_file.close()
    except :
        print("file writing error...")
        return

   

    print("end... ")




def getCitationDataFromCourseId(id):
    urlData = "{}/{}?format=json&view=full&apikey={}".format(BASE_URL,id,API_KEY)
    course = getJsonData(urlData)
    c = {}
    c['citations']=[]
    # combine a list of all citations
    if 'reading_list' in course['reading_lists']:
        for i in course['reading_lists']['reading_list']:
            if 'citation' in  i['citations']:
                a =  i['citations']['citation']
                for x in a :
                    t = x['metadata']['title']
                    x['metadata']['title'] = t.replace('/', '')
                c['citations'] += i['citations']['citation']
    course['citations'] = c['citations']
    return course
    


def parseResults(data):
  # Use the json module to load the string data into a dictionary
  try:
    theJSON = json.loads(data)
    for i in theJSON["course"]:
        firstCampus = i["campus"]
  except JSONDecodeError as err:
      print("JSON decode error " + err.msg + err.lineno)
  return thsJSON



def readJsonFile (aFileName) :
    with open(aFileName) as json_file:  
        data = json.load(json_file)
    return data


if __name__ == "__main__":
  main()

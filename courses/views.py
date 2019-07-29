from django.http import HttpResponse
from http import HTTPStatus
from django.shortcuts import render
import urllib.request # instead of urllib2 like in Python 2.7
from urllib.error import HTTPError,URLError
import os
import json
from json import JSONDecodeError
from django.views.decorators.cache import cache_page


BASE_URL = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/courses'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def getJsonData(requestUrl):
    try:
        coursesData = {}
        # Open the URL and read the data
        webUrl = urllib.request.urlopen(requestUrl)
        print (requestUrl)
        if (webUrl.getcode() == HTTPStatus.OK):
            data = webUrl.read()
            coursesData = json.loads(data)
            print ("return url  =" + str(webUrl))
    except HTTPError as err:
            print (str(webUrl.getcode()))
    except URLError as err:
            print("server is down..." + err.name())

    return coursesData

# @cache_page(60 * 15)
def index(request):
    obj = readJsonFile("courses.txt")
    print("total records = " + str(len(obj['course'])))
    context = {
        'obj' : obj['course'],
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def CoursesListView(request):
    return render(request, 'index.html', {})

def CourseDetailView(request , id):
 
    course = getCitationDataFromCourseId(id)
    context = {
        'obj' : course['citations'],
    }
    return render(request, 'reading_list.html',context=context)


def getCitationDataFromCourseId(id):
    urlData = "{BASE_URL}/{id}?format=json&view=full&apikey={API_KEY}"
    course = getJsonData(urlData)
    c = {}
    c['citations']=[]
    # combine a list of all citations
    if 'reading_list' in course['reading_lists']:
        for i in course['reading_lists']['reading_list']:
            if 'citation' in  i['citations']:
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
    file_path = os.path.join(BASE_DIR,aFileName)

    with open(file_path) as json_file:  
        data = json.load(json_file)
    return data

    

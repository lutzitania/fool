from django.shortcuts import render
from datetime import datetime
import json
import random
import operator

# Create your views here.



data = json.load(open('content_api.json'))

#Find the first article with the "10-promise" tag
def findtoparticle():
	i = 0 #Article counter
	toparticle = 0
	for result in data["results"]:
		for tag in result["tags"]:
			if tag["slug"] == "10-promise":
				toparticle = i
				return toparticle
		i += 1

def getarticledetail(uuid):
	i = 0
	articleid = 0
	for result in data["results"]:
		if result["uuid"] == uuid:
			articleid = i
			return articleid
		i += 1

def getRandomArticles(top):
	articles = [-1, -1, -1]
	length = len(data["results"]) #Get the number of results for the top bound of the rand generator
	i = 0
	for num in articles:
		rand = random.randint(0, (length-1))
		while rand in articles or rand == top:
			rand = random.randint(0, (length-1)) #This avoids getting the same article twice.
		articles[i] = rand
		i += 1
	return articles

def getLatestHeadlines():
	"""
	  * Okay, in this method, we are going to:
	  *   1.) Create a dictionary containing each article's index as the key and its publish_at value as the value
	  *   2.) Write that into another dictionary in which we sort by the value (the date)
	  *   3.) Grab the top 5 (a number I totally made up)
	  *   4.) Return an array of those indices (same as the getRandomArticles method)
	  *
	  * NOTE: The articles in the JSON file are already ordered by date! And that's super convenient,
	  *		but not something we should necessarily count on. Unless we're able to send that sort by
	  *		condition as part of the HTTP request, but I don't want to assume that, here.
	"""
	articles = [-1, -1, -1, -1, -1]
	dates = {}
	i = 0
	for result in data["results"]:
		dates.update({i:result["publish_at"]})
		i += 1
	date_sort = sorted(dates.items(), key=operator.itemgetter(1), reverse=True)[:5]

	i = 0
	for key, value in date_sort:
		articles[i] = key
		i += 1
	return articles

def homepage(request):
	topindex = findtoparticle()
	toparticle = data["results"][topindex]
	articleindices = getRandomArticles(topindex)
	article1 = data["results"][articleindices[0]]
	article2 = data["results"][articleindices[1]]
	article3 = data["results"][articleindices[2]]
	return render(request, 'articles/homepage.html', {'topindex': topindex, 'toparticle': toparticle, 'article1': article1, 'article2': article2, 'article3': article3})

def detail(request, uuid):
	articleid = getarticledetail(uuid)
	article = data["results"][articleid]
	publish_at_string = data["results"][articleid]["publish_at"]
	publish_at_datetime = datetime.strptime(publish_at_string, "%Y-%m-%dT%H:%M:%SZ" )
	pretty_publishdate = (publish_at_datetime.strftime("%B") + " " + str(publish_at_datetime.day) + ", " + str(publish_at_datetime.year))
	recentheadlines = getLatestHeadlines()
	hl1 = data["results"][recentheadlines[0]]
	hl2 = data["results"][recentheadlines[1]]
	hl3 = data["results"][recentheadlines[2]]
	hl4 = data["results"][recentheadlines[3]]
	hl5 = data["results"][recentheadlines[4]]
	articlebody = (data["results"][articleid]["body"]).encode('ascii', 'ignore')
	return render(request, 'articles/detail.html', {'article': article, 'articlebody': articlebody, 'publish_at': pretty_publishdate, 'hl1': hl1, 'hl2': hl2, 'hl3': hl3, 'hl4': hl4, 'hl5': hl5})
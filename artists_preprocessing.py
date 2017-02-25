import sys
import urllib2
import ast


#My API Key
APIKEY = "90abbe594e2c2ebdab5744a18ff8d8fa"

#some argument checking
if len(sys.argv)==3:
	limit = sys.argv[1]
	limitTagCounter=sys.argv[2]
	if (int(limit)>1000):
		limit = 1000
else:
	limit = 100
	limitTagCounter = 5

#REST CALL to last.fm API for greece top artists
responseTopArtists = urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country=greece&api_key="+APIKEY+"&limit="+str(limit)+"&format=json")

#Creating a dict to save the unique artists 
dict={}
dataArtist = responseTopArtists.read()
dataArtist = ast.literal_eval(dataArtist)
artistcounter=0

#inserting key-values to dicts, keys are the tags-categories and values are the artists
print "\n__________getting the top "+ str(limit) +" artists listened from greek users and their "+ str(limitTagCounter)  +" top tags-categories_______________\n"

for entry in dataArtist["topartists"]["artist"]:
	if ("name" in entry.keys() and entry["name"] != "" and entry["mbid"]!="" and entry["name"] != "[unknown]"):
		print str(artistcounter+1)+" "+entry["name"]
		artist = entry["mbid"]
		artistName = entry["name"]
	
		#get top tags-categories from each artist that belongs to
		responseTag = urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&mbid="+artist+"&api_key="+APIKEY+"&format=json")
		dataTag = responseTag.read()
		dataTag = ast.literal_eval(dataTag)
		tagCounter=0
		for fieldTags in dataTag["toptags"]["tag"]:
			print fieldTags["name"]
			if (fieldTags["name"] in dict):
				dict[fieldTags["name"]].append(artistName)
			else:
				dict[fieldTags["name"]] = [artistName]
			tagCounter = tagCounter + 1
			if (tagCounter==int(limitTagCounter)):
				break
		responseTag.close()
		print "\n"
		artistcounter = artistcounter + 1


'''
creating a csv file containing a source -> target relation for gephi input
the source -> target relation is the that an artist (source) is connected to
another artist (target) due to their common tag
'''
file1 = open("greece_top_artists_number_of_artists_"+str(limit)+"_top_tags"+str(limitTagCounter)+".csv", "w")
file1.write("source,target\n")

for the_key, the_value in dict.iteritems():
	data = the_value
	#print "tag: "+the_key
	for i in range(0, len(data)):
		for j in range(i+1, len(data)):
			#print data[i]+","+data[j]
			row = "'"+data[i]+"','"+data[j]+"'\n"
			#row = row.encode('utf-8')
			file1.write(row)
	#print "\n"		
file1.close()


'''
creating a csv file containing the most popular tag-categories based on 
the most popular artists listed by greek users that these artists fetched
by REST call to API 
'''
file2 = open("greece_top_artists_number_of_artists_"+str(limit)+"_top_tags_"+str(limitTagCounter)+"_most_frequent_tags.csv", "w")
file2.write("tag,frequency\n")
#print "\n__________most popular tag-categories taken by artists_______________\n"
for k in sorted(dict, key=lambda k: len(dict[k]), reverse=True):
	#print k+" "+str(len(dict[k]))+" \n"
	row = "'"+k+"',"+str(len(dict[k])) + "\n"
	file2.write(row)


file2.close()

responseTopArtists.close()
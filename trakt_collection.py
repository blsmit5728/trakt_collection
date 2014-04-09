import trakt.tv
import collections
import json
from pprint import pprint
import sys
import getopt
import os

shows = [] 

def list_test():
    trakt.tv.List.add(name="testt",privacy="public",desc="asjkldfh",show_numbers="true",allow_shouts="false")
    items = [ {'type':'movie','imdb_id':'tt0372784'} ]
    trakt.tv.List.item_add(name="testt", items=items)
    items = [ {'type':'movie','imdb_id':'tt0372784'} ]
    trakt.tv.List.item_delete(name="testt", items=items)
    c = trakt.tv.User.lists("blsmit5728")
    print c
    c = trakt.tv.User.list("blsmit5728", "testt")
    print c
    trakt.tv.List.delete(name="testt")
    c = trakt.tv.User.lists("blsmit5728")
    print c

def movies_collected():
    movies = trakt.tv.User.movies_collected("blsmit5728")
    #print movies
    ljson = json.dumps(movies, ensure_ascii=False)
    ljsonload = json.loads(ljson)
    #print ljsonload
    for titles in ljsonload:
        print titles['title']

def shows_collected():
    shows = trakt.tv.User.shows_collected("blsmit5728")
    #print movies
    ljson = json.dumps(shows, ensure_ascii=False)
    ljsonload = json.loads(ljson)
    #print ljsonload
    for titles in ljsonload:
        print titles['title']

def usage(status):
    print "Usage: ./trakt_collection -a<api_key> -u<user> -p<password> -d<directory> (-f<filename>)"
    print "       -a : trakt api key "
    print "       -d : directory containing folders of Show names"
    print "       -f : output file for listing of missing episodes default: default_out_file.txt"
    print "       -p : trakt password in plain text"
    print "       -u : trakt username"
    if(status):
        exit(1)
    else:
        exit(0)

def sanitize_for_trakt(series_name):
    if '(' in series_name:
        series_name = series_name.replace("(","")
        series_name = series_name.replace(")","")
    if '.' in series_name:
        series_name = series_name.replace(".","")
    if '\'' in series_name:
        series_name = series_name.replace("'","")
    if '!' in series_name:
        series_name = series_name.replace("!","")
    if '&' in series_name:
        series_name = series_name.replace("&","and")
    if '-' in series_name:
        series_name = series_name.replace("-","")
    return series_name

def main(argv):
    trakt_user = ""
    trakt_pass = ""
    search_dir = ""
    trakt_api_key = ""
    tst = ""
    output_file = "default_out_file.txt"
    try:                                
        opts, args = getopt.getopt(argv, "a:d:f:hp:t:u:", ["help","api_key=","dir=", "username=", "password=","filename=","test="]) 
    except getopt.GetoptError:           
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d","--dir"):
            search_dir = arg
        elif opt in ("-u","--username"):
            trakt_user = arg
        elif opt in ("-p","--password"):
            trakt_pass = arg
        elif opt in ("-a","--api","--api_key"):
            trakt_api_key = arg
        elif opt in ("-f","--filename"):
            output_file = arg
        elif opt in ("-h","--help"):
            usage(0)
        elif opt in ("-t","--test"):
            tst = arg

    if trakt_user is "":
        print "Error: You need to enter a username for trakt"
        usage(1)
    if trakt_pass is "":
        print "Error: You need to enter a password for trakt"
        usage(1)
    if trakt_api_key is "":
        print "Error: You need to enter a trakt api key"
        usage(1)
    try:
        f_handle = open(output_file,"w")
    except IOError:
        print "Error opening the output file, check permissions, etc..."
        exit(2)

    trakt.tv.setup(apikey=trakt_api_key,username=trakt_user,password=trakt_pass)

    if tst == "":
        print "Please enter a test number"
    elif tst == "1":
        p = trakt.tv.Activity.user()
        print p
    elif tst == "2":
        list_test()
    elif tst == "3":
        movies_collected()
    elif tst == "4":
        shows_collected()


    exit(0)
    '''
    b = trakt.tv.User.list(list_name='tvshows')
    ljson = json.dumps(b, ensure_ascii=False)
    ljsonload = json.loads(ljson)
    for i in range(0,55):
        #print ljsonload['items'][i]['show']['title']
        shows.append(ljsonload['items'][i]['show']['title'])
    shows_sort =  sorted(shows)
    for i in range(0,55):
        print shows_sort[i]
    '''
    names = os.listdir(search_dir)
    for n in names:
        trakt.tv.setup(apikey=trakt_api_key,username=trakt_user,password=trakt_pass)
        print "Show: " + n
        n = sanitize_for_trakt(n) 
        seas = trakt.tv.show.seasons(n.replace(" ", "-"))
        seas_j = json.dumps(seas,ensure_ascii=False)
        seas_jload = json.loads(seas_j)
        seasons = int(seas_jload[0]['season'])
        if int(seasons) > 2000:
            print "This show probably starts with a yearly season...fuck"
        else:   
            for i in range(1,seasons+1):
                t = trakt.tv.show.season(n.replace(" ", "-"),str(i))
                x = json.dumps(t,ensure_ascii=False)
                y = json.loads(x)
                for c in y:
                    if c['in_collection'] is False:
                        #print "Is " + str(n) + " [S" + str(c['season']) + "E" + str(c['episode']) +  "] in your collection? " + str(c['in_collection'])
                        season_num = "%02d" % c['season']
                        episode_num = "%02d" % c['episode']
                        ep_id = "S" + season_num + "E" + episode_num
                        wo = str(n) + " " + str(ep_id) + "\n"
                        f_handle.write(wo)
                    print "Is " + str(n) + " [S" + str(c['season']) + "E" + str(c['episode']) +  "] in your collection? " + str(c['in_collection'])

if __name__ == "__main__":
    main(sys.argv[1:])



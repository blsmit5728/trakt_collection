import trakt.tv
import collections
import json
from pprint import pprint
import sys
import getopt
import os

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
    grammar = "kant.xml"                 
    try:                                
        opts, args = getopt.getopt(argv, "a:d:u:p:", ["api_key=","dir=", "username=", "password="]) 
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
                    if "Brooklyn" in n:
                        print c
                    print "Is " + str(n) + " [S" + str(c['season']) + "E" + str(c['episode']) +  "] in your collection? " + str(c['in_collection'])

if __name__ == "__main__":
    main(sys.argv[1:])

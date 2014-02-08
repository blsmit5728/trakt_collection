import trakt.tv
import collections
import json
from pprint import pprint
import sys
import getopt
import os

#trakt.tv.setup(apikey='a115a168132e06e8b05ab9a58790390d',username='blsmit5728',password='baseball1')
#t = trakt.tv.show.season('the-walking-dead',3)
#x = json.dumps(t,ensure_ascii=False)
#y = json.loads(x)
#print y
#for c in y:
#    print c['episode']
#    print c['in_collection']
#    print c['tvdb_id']

def main(argv):
    trakt_user = ""
    trakt_pass = ""
    search_dir = ""
    grammar = "kant.xml"                 
    try:                                
        opts, args = getopt.getopt(argv, "d:u:p:", ["dir=", "username=", "password="]) 
    except getopt.GetoptError:           
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d","--dir"):
            print "Directory=" + arg
            search_dir = arg
        elif opt in ("-u","--username"):
            trakt_user = arg
            print trakt_user
        elif opt in ("-p","--password"):
            trakt_pass = arg
            print trakt_pass

    names = os.listdir(search_dir)
    for n in names:
        trakt.tv.setup(apikey='a115a168132e06e8b05ab9a58790390d',username=trakt_user,password=trakt_pass)
        #t = trakt.tv.show.season('the-walking-dead',3)
        print n
        if '(' in n:
            n = n.replace("(","")
            n = n.replace(")","")
            print n
        elif '.' in n:
            n = n.replace(".","")
            print n
        elif '\'' in n:
            n = n.replace("'","")
            print n
        elif '!' in n:
            n = n.replace("!","")
            print n
        elif '&' in n:
            n = n.replace("&","")
            print n
        t = trakt.tv.show.season(n.replace(" ", "-"),1)
        x = json.dumps(t,ensure_ascii=False)
        y = json.loads(x)
        #print y
        for c in y:
        #pprint(c)
        #print c['episode']
            #print c['in_collection']
            print c['tvdb_id']

if __name__ == "__main__":
    main(sys.argv[1:])

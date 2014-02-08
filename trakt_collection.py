import trakt.tv
import collections
import json
from pprint import pprint



trakt.tv.setup(apikey='a115a168132e06e8b05ab9a58790390d',username='blsmit5728',password='baseball1')
t = trakt.tv.show.season('the-walking-dead',3)
x = json.dumps(t,ensure_ascii=False)
y = json.loads(x)
#print y
for c in y:
    print c['episode']
    print c['in_collection']
    print c['tvdb_id']

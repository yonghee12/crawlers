from crawlers.watcha.config import *
from crawlers.watcha.metadata_evaluations import WatchaMetadataHandler

api = WatchaMetadataHandler(max_attempt=3)

for key in list(api.keys)[2:]:
    print(key)
    api.get(key, max_page=1000, verbose=1)

print()
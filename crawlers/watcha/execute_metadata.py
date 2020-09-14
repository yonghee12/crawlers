from crawlers.watcha.metadata_evaluations import WatchaMetadataHandler

api = WatchaMetadataHandler(max_attempt=3)
api.get('평균별점 TOP 영화', 1000, verbose=1)
print()
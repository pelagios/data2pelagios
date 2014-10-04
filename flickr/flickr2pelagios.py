import flickrapi

with open('api-key.txt', 'r') as f:
  api_key = f.readline().strip()
  
  print('API key: ' + api_key)

  flickr = flickrapi.FlickrAPI(api_key)

  for photo in flickr.walk(user_id = 'palestineexplorationfund'):
    print photo.get('title')

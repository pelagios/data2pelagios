import flickrapi

with open('api-key.txt', 'r') as f:
  api_key = f.readline().strip()
  
  print('API key: ' + api_key)
  
  flickr = flickrapi.FlickrAPI(api_key)

  output = open('pef-pelagios.ttl', 'w')
  output.write('@prefix dcterms: <http://purl.org/dc/terms/> .\n')  
  output.write('@prefix foaf: <> . \n')
  output.write('@prefix pelagios: <http://pelagios.github.io/vocab/terms#> .\n')
  output.write('@prefix oa: <http://www.w3.org/ns/oa#> .\n\n')

  for photo in flickr.walk(user_id = 'palestineexplorationfund'):
    output.write('<http://example.org/pef/dump.ttl#images/' + photo.get('id') + '> a pelagios:AnnotatedThing ;\n')
    output.write('  dcterms:title "' + photo.get('title').encode('utf-8') + '" ;\n');  
    output.write('  foaf:homepage <https://farm' + photo.get('farm') + '.staticflickr.com/' + photo.get('server') + '/' + photo.get('id') + '_' + photo.get('secret') + '.jpg> ;\n')   
    output.write('  .\n\n')



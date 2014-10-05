import flickrapi

with open('api-key.txt', 'r') as f:
  api_key = f.readline().strip()
  user_id = 'palestineexplorationfund'
    
  flickr = flickrapi.FlickrAPI(api_key)

  output = open('pef-pelagios.ttl', 'w')
  
  output.write('@prefix dcterms: <http://purl.org/dc/terms/> .\n')  
  output.write('@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n')
  output.write('@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .\n')
  output.write('@prefix oa: <http://www.w3.org/ns/oa#> .\n\n')
  output.write('@prefix pelagios: <http://pelagios.github.io/vocab/terms#> .\n')

  ctr_all = 0
  ctr_with_pleiades = 0
  
  for photo in flickr.walk(user_id = user_id, extras = 'machine_tags,date_taken,geo'):
    ctr_all += 1
    photo_id = photo.get('id')
    pleiades_tags = [ tag for tag in photo.get('machine_tags').split() if tag.startswith('pleiades') ]

    if len(pleiades_tags) > 0:
      ctr_with_pleiades += 1
      output.write('<http://example.org/flickr/dump.ttl#images/' + photo_id + '> a pelagios:AnnotatedThing ;\n')
      output.write('  dcterms:title "' + photo.get('title').encode('utf-8') + '" ;\n');  
      output.write('  foaf:homepage <http://www.flickr.com/photos/' + user_id + '/' + photo_id + '> ;\n')
      # output.write('  foaf:homepage <https://farm' + photo.get('farm') + '.staticflickr.com/' + photo.get('server') + '/' + photo.get('id') + '_' + photo.get('secret') + '.jpg> ;\n')   

      if photo.get('datetaken'):
        output.write('  dcterms:temporal "' + photo.get('datetaken') + '" ;\n')
        
      if photo.get('latitude') and photo.get('longitude'):
        output.write('  dcterms:spatial [ geo:lat ' + photo.get('latitude') + ' ; geo:long ' + photo.get('longitude') + ' ] ;\n')
        
      output.write('  .\n\n')
      
      for idx, pleiades_tag in enumerate(pleiades_tags):  
        output.write('<http://example.org/flickr/dump.ttl#image/' + photo_id + '/annotations/' + str(idx) + '> a oa:Annotation ;\n')
        output.write('  oa:hasTarget <http://example.org/flickr/dump.ttl#images/' + photo_id + '> ;\n')
        output.write('  oa:hasBody <http://pleiades.stoa.org/places/' + pleiades_tag[17:] + '> ;\n')
        output.write('  .\n\n')
      
  output.close()
  print('Processed ' + str(ctr_all) + ' photos')
  print('Got ' + str(ctr_with_pleiades) + ' with Pleiades tag')

import sys
import flickrapi

with open('api-key.txt', 'r') as key_file:
  api_key = key_file.readline().strip()
  api_secret = key_file.readline().strip()
    
  if len(sys.argv) < 3:
	  print('Missing parameters. Usage: \'python flickr2pelagios.py <user-id> <title>\'')
	  sys.exit()
	  
  user_id = sys.argv[1]
  stream_title = sys.argv[2]	  
  
  print('Harvesting \'' + stream_title + '\' (' + user_id + ')')
  
  # Write VoID
  with open('flickr.void.ttl.template') as void_template:
    void = open('harvest/' + user_id + '.void.ttl', 'w')
    void.write(void_template.read().replace('@@title@@', stream_title).replace('@@userID@@', user_id))
    void.close()
    
    # Write annotations
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    annotations = open('harvest/' + user_id + '.ttl', 'w')
    annotations.write('@prefix dcterms: <http://purl.org/dc/terms/> .\n')  
    annotations.write('@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n')
    annotations.write('@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .\n')
    annotations.write('@prefix oa: <http://www.w3.org/ns/oa#> .\n')
    annotations.write('@prefix pelagios: <http://pelagios.github.io/vocab/terms#> .\n\n')

    ctr_all = 0
    ctr_with_pleiades = 0
  
    for photo in flickr.walk(user_id = user_id, extras = 'machine_tags,date_taken,geo'):
      ctr_all += 1
      photo_id = photo.get('id')
      pleiades_tags = [ tag for tag in photo.get('machine_tags').split() if tag.startswith('pleiades') ]

      if len(pleiades_tags) > 0:
        ctr_with_pleiades += 1
        annotations.write('<http://example.org/flickr/' + user_id + '.ttl#photos/' + photo_id + '> a pelagios:AnnotatedThing ;\n')
        annotations.write('  dcterms:title "' + photo.get('title').replace('"', '\\"').encode('utf-8')[:250]  + '" ;\n');  
        annotations.write('  foaf:homepage <http://www.flickr.com/photos/' + user_id + '/' + photo_id + '> ;\n')
        annotations.write('  foaf:depiction <http://farm' + photo.get('farm') + '.staticflickr.com/' + photo.get('server') + '/' + photo_id + '_' + photo.get('secret') + '.jpg> ;\n')
      
        if photo.get('datetaken'):
          year = photo.get('datetaken').split('-', 1)[0]
          annotations.write('  dcterms:temporal "' + year + '" ;\n')
        
        if photo.get('latitude') and photo.get('longitude'):
          annotations.write('  dcterms:spatial [ geo:lat ' + photo.get('latitude') + ' ; geo:long ' + photo.get('longitude') + ' ] ;\n')
        
        annotations.write('  .\n\n')
      
        for idx, pleiades_tag in enumerate(pleiades_tags):  
          annotations.write('<http://example.org/flickr/' + user_id + '.ttl#photos/' + photo_id + '/annotations/' + str(idx) + '> a oa:Annotation ;\n')
          annotations.write('  oa:hasTarget <http://example.org/flickr/' + user_id + '.ttl#photos/' + photo_id + '> ;\n')
          
          annotations.write('  oa:hasBody <http://pleiades.stoa.org/places/' + pleiades_tag[(pleiades_tag.rfind("=") + 1):] + '> ;\n')
          annotations.write('  .\n\n')
      
    annotations.close()
  
    print('Processed ' + str(ctr_all) + ' photos')
    print('Got ' + str(ctr_with_pleiades) + ' with Pleiades tag')

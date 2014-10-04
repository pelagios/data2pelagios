import json
import re

with open('horsfield.json') as f:
  output = open('horsfield-pelagios.ttl', 'w')
  output.write('@prefix dcterms: <http://purl.org/dc/terms/> .\n')  
  output.write('@prefix pelagios: <http://pelagios.github.io/vocab/terms#> .\n')
  output.write('@prefix oa: <http://www.w3.org/ns/oa#> .\n')
  
  dump = json.load(f)
  
  print('Converting ' + str(len(dump)) +  ' records')
  
  ctr = 0
  for record in dump:
    info = record['info'] 
    
    if 'pleiadesID' in info.keys() and info['pleiadesID']:
      ctr += 1
      output.write('<http://example.org/horsfield/dump.ttl#images/' + info['imageID'] + '> a pelagios:AnnotatedThing ;\n')
      output.write('  dcterms:title "' + re.sub(r"\r\n", " ", info['imageLabel']) + '" ;\n');     
      output.write('  dcterms:identifier "' + info['imageID'] + ' ;\n');   
      output.write('  .\n\n')
      
      output.write('<http://example.org/horsfield/dump.ttl#image/' + info['imageID'] + '/annotations/0> a oa:Annotation ;\n')
      output.write('  oa:hasTarget <http://example.org/horsfield/dump.ttl#images/' + info['imageID'] + '> ;\n')
      output.write('  oa:hasBody <http://pleiades.stoa.org/places/' + info['pleiadesID'] + '> ;\n')
      output.write('  .\n\n')
      
  output.close()
  
  print('Done - converted ' + str(ctr) + ' records with Pleiades ID')
  
  # {u'info': {u'activities': [u'landscape'], u'annotations': [], u'orientation': u'landscape', u'people': None, 
  #  u'things': None, u'lon': u'', u'keywordsUser': u'', u'comments': u'', u'toSearch': u' ', u'pleiadesID': u'', 
  #  u'theme': None, u'geojson': {u'geometry': {u'type': u'Point', u'coordinates': [u'', u'']}}, u'lat': u'', 
  #  u'imageID': u'P2008-395', u'imageLabel': u'GEWERA PLAIN - looking south east from 652 (Antiquities Dept. Neg. 6.355)'}, 
  #  u'user_id': 646, u'task_id': 10005, u'calibration': None, u'finish_time': u'2014-09-08T13:42:10.895636', 
  #  u'created': u'2014-09-08T13:42:10.895611', u'app_id': 29, u'user_ip': None, u'timeout': None, u'id': 18603}

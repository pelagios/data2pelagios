import json

with open('gazetteer_places_2013-12-06.json') as f:
  output = open('dai.ttl', 'w')
  
  output.write('@prefix dcterms: <http://purl.org/dc/terms/> .\n')
  output.write('@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n')
  output.write('@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .\n')
  output.write('@prefix lawd: <http://lawd.info/ontology/> .\n')
  output.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
  output.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n')
  output.write('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n')

@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
  
  for line in f.readlines():
    record = json.loads(line)

    if record['deleted'] == False:
      output.write('<http://gazetteer.dainst.org/place/' + record['_id'] + '> a lawd:Place ;\n')
      if 'prefName' in record.keys():
        output.write('  rdfs:label "' + (record['prefName']['title']).encode('utf8').replace('"','\'').replace('\\','') + '" ;\n')
      else:
        output.write('  rdrs:label "' + record['_id'] + '" ;\n')
      
      if 'type' in record.keys():
        output.write('  dcterms:subject "' + (record['type']).encode('utf8') + '" ;\n')

      for closeMatch in record['ids']:
        if 'context' in closeMatch.keys():
          if closeMatch['context'] == 'pleiades':
            output.write('  skos:closeMatch <http://pleiades.stoa.org/places/' + closeMatch['value'] + '> ;\n')
          elif closeMatch['context'] == 'geonames':
            output.write('  skos:closeMatch <http://sws.geonames.org/' + (closeMatch['value']).encode('utf8') + '> ;\n')

      for name in record['names']:
        if 'language' in name.keys() and name['language'] != '':
          output.write(  '  lawd:hasName [ lawd:primaryForm "' + (name['title']).encode('utf8').replace('"','\'').replace('\\','')  + '"@' + (name['language']).encode('utf8') + ' ] ;\n')
        else:
          output.write(  '  lawd:hasName [ lawd:primaryForm "' + (name['title']).encode('utf8').replace('"','\'').replace('\\','')  + '" ] ;\n')
  
      if 'parent' in record.keys():
        output.write('  dcterms:isPartOf <http://gazetteer.dainst.org/place/' + record['parent'] + '> ;\n')
   
      if 'prefLocation' in record.keys():
        lonlat = record['prefLocation']['coordinates']
        output.write('  geo:location [ geo:lat "' + str(lonlat[1]) + '"^^xsd:double ; geo:long "' + str(lonlat[0]) + '"^^xsd:double ] ;\n')
  
      output.write('  .\n\n')
  
  output.close()

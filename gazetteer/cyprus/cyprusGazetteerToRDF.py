import json

with open('cyprus-gazetteer.json') as f:
  data = json.load(f)
  output = open('cyprus-gazetteer.ttl', 'w')

  output.write('@prefix dcterms: <http://purl.org/dc/terms/> .\n')
  output.write('@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n')
  output.write('@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .\n')
  output.write('@prefix geosparql: <http://www.opengis.net/ont/geosparql#> .\n')
  output.write('@prefix lawd: <http://lawd.info/ontology/> .\n')
  output.write('@prefix osgeo: <http://data.ordnancesurvey.co.uk/ontology/geometry/> .\n')
  output.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
  output.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n')
  output.write('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n')

  for item in data['features']:
    props = item['properties']

    output.write('<' + props['uri'] + '> a lawd:Place ;\n')
    output.write('  rdfs:label "' + (props['default_toponym']).encode('utf8').replace('"','\'').replace('\\','') + '" ;\n')

    for variant in props['toponym_variants']:
      output.write(  '  lawd:hasName [ lawd:primaryForm "' + (variant['toponym']).encode('utf8').replace('"','\'').replace('\\','')  + '" ] ;\n')

    if 'geonames_uri' in props:
      output.write('  skos:closeMatch <' + (props['geonames_uri']).encode('utf8') + '> ;\n')

    output.write('  geosparql:hasGeometry [ osgeo:asGeoJSON "' + json.dumps(item['geometry']).replace('"', '\\"') + '" ] ;\n')

    output.write('  .\n\n')

  output.close()

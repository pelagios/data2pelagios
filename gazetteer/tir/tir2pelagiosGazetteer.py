import csv

def esc(chars):
  return chars.replace('"','\'').replace('\\','')

with open('TIR-CAT.csv') as f:
  output = open('tir.ttl', 'w')
  
  output.write('@prefix dcterms: <http://purl.org/dc/terms/> .\n')
  output.write('@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n')
  output.write('@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .\n')
  output.write('@prefix lawd: <http://lawd.info/ontology/> .\n')
  output.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
  output.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n')
  output.write('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n')

  reader = csv.reader(f, delimiter=';')
  next(reader, None)  # skip the header
  
  cnt_all = 0
  cnt_located = 0
  
  for row in reader:
    cnt_all += 1
    idx = row[0]
    modernName = row[3]
    ancientName = row[4]
    lat = row[22]
    lon = row[23]
    
    output.write('<http://www.example.org/tir/place/' + idx + '> a lawd:Place ;\n')
    output.write('  rdfs:label "' + esc(modernName) + '" ;\n')
    
    if (ancientName):
      output.write('  lawd:hasName [ lawd:primaryForm "' + esc(ancientName) + '" ] ;\n')
  
    if (lat and lon):
      cnt_located += 1
      output.write('  geo:location [ geo:lat "' + str(lat) + '"^^xsd:double ; geo:long "' + str(lon) + '"^^xsd:double ] ;\n')
      
    output.write('  .\n\n')
    
  print('Converted ' +  str(cnt_all) + ' places (' + str(cnt_located) + ' located)')
  output.close()

import csv

def esc(chars):
  return chars.replace('"','\'').replace('\\','')

def writeName(name, language, output):
  if (name):
    output.write('  lawd:hasName [ lawd:primaryForm "' + esc(name) + '"@' + language + ' ] ;\n')

with open('TM_Geo_Pelagios.csv') as f:
  output = open('trismegistos.ttl', 'w')
  
  output.write('@prefix dcterms: <http://purl.org/dc/terms/> .\n')
  output.write('@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n')
  output.write('@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .\n')
  output.write('@prefix lawd: <http://lawd.info/ontology/> .\n')
  output.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
  output.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n')
  output.write('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n')

  reader = csv.reader(f, delimiter=',')
  next(reader, None)  # skip the header
  
  cnt_all = 0
  
  for row in reader:
    uri = row[13]
    nameStandard = row[1]
    nameGreek = row[2]
    nameLatin = row[3]
    nameEgyptian = row[4]
    nameCoptic = row[5]
    
    pleiadesId = row[11]
    geonamesId = row[12]
    
    if (uri):
      cnt_all += 1
      output.write('<' + uri + '> a lawd:Place ;\n')
      output.write('  rdfs:label "' + esc(nameStandard) + '" ;\n')
    
      writeName(nameGreek, 'gre', output)
      writeName(nameLatin, 'lat', output)
      writeName(nameEgyptian, 'egy', output)
      writeName(nameCoptic, 'cop', output)
    
      if (pleiadesId):
        output.write('  skos:closeMatch <http://pleiades.stoa.org/places/' + pleiadesId + '> ;\n')
      
      if (geonamesId):
        output.write('  skos:closeMatch <http://sws.geonames.org/' + geonamesId + '> ;\n')
    
      output.write('  .\n\n')
    
  print('Converted ' +  str(cnt_all) + ' places')
  output.close()

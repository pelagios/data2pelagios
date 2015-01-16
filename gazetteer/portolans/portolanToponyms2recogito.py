# Modified version of the gazetteer conversion script that generates a basic human-readable
# text file, pre-annotated for import to Recogito

import csv
import re

def esc(chars):
  return chars.replace('"','\'').replace('\\','').replace(';', ',')
  
def toInt(chars):
  # Some dates have '+' appended - we want to keep the date, but strip the +
  normalized = chars[0:len(chars) - 1] if chars.endswith('+') else chars
    
  try:
    toInt = int(normalized)
    return toInt
  except ValueError:
    return None

with open('PortolanPRECURSORS.csv') as f:
  outputText = open('recogito-portolan.txt', 'w')  
  outputAnnotations = open('recogito-portolan.csv', 'w')
  outputAnnotations.write('offset;toponym;\n')

  reader = csv.reader(f, delimiter=';')
  next(reader, None)  # skip the header
  
  cnt_all = 0
  cnt_invalid = 0
  idx = 0
  offset = 0
  
  for row in reader:
    idx += 1
    
    if len(row) < 11:
      cnt_invalid += 1
    else:
      cnt_all += 1
    
      # Fields in source CSV
      sorting = row[0]
      modernName = row[2]
      nameOnChart = row[3]
      dateFirstSeen = toInt(row[5])
      dateLastSeen = toInt(row[10])
      coastalSection = row[4]
      chartMakerBlack = row[6]
      chartMakerRed = row[8]
      comments = row[23]
    
      # Line in output text file
      idAndName = re.sub(' +', ' ', (str(idx) + '-' + sorting + ', ' + esc(nameOnChart)).replace('}','')).strip()
      restOfLine = '; '
      
      if (modernName):
        restOfLine += esc(modernName) + '; '
      
      description = 'Portolan chart name'
      if (coastalSection):
        description += ', coastal section ' + coastalSection
      else:
        description += '.'
        
      if (chartMakerBlack):
        description += ' Chartmaker (black name): ' + chartMakerBlack
      if (chartMakerRed):
        description += ', chartmaker (red name): ' + chartMakerRed + '.'
      else:
        description += '.'
        
      if (comments):
        description += ' (' + comments + ')'
       
      restOfLine += description + '; '
    
      if (dateFirstSeen and dateLastSeen):
        restOfLine += 'First seen ' + str(dateFirstSeen) + ', last seen ' + str(dateLastSeen) + '; '
      elif (dateFirstSeen):
        restOfLine += 'First seen ' + str(dateFirstSeen) + '; '
        
      restOfLine = re.sub(' +', ' ', restOfLine).strip()

      outputText.write(idAndName + restOfLine + '\n')
      outputAnnotations.write(str(offset) + ';' + idAndName + '\n')
      offset += len(idAndName.decode('utf-8')) + len(restOfLine.decode('utf-8')) + 1
    
  print('Converted ' +  str(cnt_all) + ' places, ' + str(cnt_invalid) + ' invalid lines')
  outputText.close()
  outputAnnotations.close()

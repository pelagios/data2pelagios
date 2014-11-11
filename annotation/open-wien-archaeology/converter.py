import csv

with open('FUNDPUNKTEOGD.csv') as f:
    output = open('FUNDPUNKTEOGD.ttl', 'w')
    output.write('@prefix cnt: <http://www.w3.org/2011/content#> .\n'
        '@prefix dcterms: <http://purl.org/dc/terms/> .\n'
        '@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n'
        '@prefix oa: <http://www.w3.org/ns/oa#> .\n'
        '@prefix pelagios: <http://pelagios.github.io/vocab/terms#> .\n'
        '@prefix relations: <http://pelagios.github.io/vocab/relations#> .\n'
        '@prefix xsd: <http://www.w3.org/2001/XMLSchema> .\n')
    reader = csv.reader(f, delimiter=',')
    next(reader, None) # skip the header
    row_number = 0
    for row in reader:
        row_number += 1
        object_id = row[1]
        shape = row[2]
        street_name = row[4]
        house_number = row[5]
        house_number_to = row[6]
        find_category = row[7]
        find = row[8]
        age = row[9]
        street = street_name
        if house_number:
            street += " " + house_number
            if house_number_to:
                street += "-" + house_number_to
        output.write('\n<http://example.org/pelagios/dump.ttl#items/' + str(row_number) + '>\n'
            '   a pelagios:AnnotatedThing ;\n\n'
            ' dcterms:title "' + find_category + ', ' + street + '" ;\n'
            ' dcterms:identifier "' + object_id + '" ;\n'
            ' dcterms:description "' + find + '" ;\n'
            ' dcterms:subject "' + find_category + '" ;\n'
            ' dcterms:subject "' + age + '" ;\n'
            ' .\n\n'
            '<http://example.org/pelagios/dump.ttl#items/' + str(row_number) + '/annotations/01>\n'
            '   a oa:Annotation ;\n\n'
            ' oa:hasTarget <http://example.org/pelagios/dump.ttl#items/' + str(row_number) + '> ;\n'
            ' oa:hasBody <http://pleiades.stoa.org/places/128537> ;\n'
            ' pelagios:relation relations:foundAt ;\n'
            ' oa:hasBody [ cnt:chars "' + shape + '";\n'
            '              dcterms:format "application/wkt" ] ;\n'
            ' .\n')
    output.close()
    print('converted ' + str(row_number) + ' places')

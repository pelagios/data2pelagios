require 'csv'
require 'zlib'

class GeoNamesConcordances

  def initialize()
    @concordances = {}

    gzipped = open("wikidata_geonames.csv.gz")
    gz = Zlib::GzipReader.new(gzipped)

    ctr = 0

    gz.each_line do |line|
      if ctr > 0
        row = line.split(',')

        qid   = row[0]
        gn_id = row[4]

        @concordances[qid] = gn_id
      end

      ctr += 1
    end

    puts "Loaded #{ctr} concordances"
  end

end

GeoNamesConcordances.new

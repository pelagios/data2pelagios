require 'csv'
require 'json'
require 'zlib'

WIKIDATA_PREFIX  = "http://www.wikidata.org/wiki/Q"

class WikidataToGeonames

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

  def get(qid)
    gn_id = @concordances[qid]
    unless gn_id.nil?
      "http://sws.geonames.org/" + gn_id
    end
  end

end

def getBody(bodies, hasType)
  bodiesOfType = bodies.select do |b|
    b["type"] == hasType
  end

  if bodiesOfType.length > 0
    bodiesOfType[0]
  end
end

def rewrite_wikidata(body, concordances)
  qid = body["uri"][WIKIDATA_PREFIX.length .. -1]
  match = concordances.get(qid)
  if (match.nil?)
    puts "No match found"
    body.delete("uri")
    false
  else
    puts "Rewriting #{body["uri"]} -> #{match}"
    body["uri"] = match
    true
  end
end

def rewrite_one(annotation, concordances)
  rewritten = false

  bodies = annotation["bodies"]
  place_body = getBody(bodies, "PLACE")

  unless place_body.nil?
    uri = place_body["uri"]
    unless uri.nil?
      if uri.start_with?(WIKIDATA_PREFIX)
        rewritten = rewrite_wikidata(place_body, concordances)
      end
    end
  end

  open('out-geonames.jsonl', 'a') { |f| f.puts annotation.to_json }

  rewritten
end

concordances = GeoNamesConcordances.new

if ARGV.empty?
  puts("no input file")
else
  filename = ARGV[0]
  File.open(filename, "r") do |f|
    ctr = [0, 0]
    f.each_line do |line|
      ctr[0] += 1
      rewritten = rewrite_one(JSON.parse(line), concordances)
      if rewritten
        ctr[1] += 1
      end
    end
    puts "#{ctr[0]} URIs total. #{ctr[1]} rewritten successfully"
  end
end

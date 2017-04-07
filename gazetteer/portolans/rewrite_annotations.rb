require 'json'
require './concordances'

MAP_HIST_PREFIX  = "http://www.maphistory.info/portolans/record/"
PASTPLACE_PREFIX = "http://data.pastplace.org/search?q="
WIKIDATA_PREFIX  = "http://www.wikidata.org/wiki/Q"

def rewrite_annotations(concordances)

  def parseURI(uri)
    id = uri[MAP_HIST_PREFIX.length .. -1].split('-')
    { "sorting" => id[1], "line_number" => id[0] }
  end

  def getBody(bodies, hasType)
    bodiesOfType = bodies.select do |b|
      b["type"] == hasType
    end

    if bodiesOfType.length > 0
      bodiesOfType[0]
    end
  end

  # Type needs to be change from QUOTE to TRANSCRIPTION
  def rewrite_quote(quote_body)
    quote_body["type"] = "TRANSCRIPTION"
  end

  # Just a simple string replace
  def rewrite_pastplace(place_body)
    # TODO
  end

  # Rewrite fake maphist URIs through the concordance list
  def rewrite_maphist(place_body, quote_body, concordances)
    id = parseURI(place_body["uri"])
    match = concordances.get(id['sorting'], id['line_number'], quote_body["value"])
    if (match.nil?)
      false
    else
      puts "  Rewriting #{place_body["uri"]} -> #{match}"
      place_body["uri"] = match
      true
    end
  end

  def rewrite_one(annotation, concordances)
    rewritten = false

    bodies = annotation["bodies"]
    quote_body = getBody(bodies, "QUOTE")
    place_body = getBody(bodies, "PLACE")

    if !quote_body.nil?
      rewrite_quote(quote_body)
    end

    if !place_body.nil?
      uri = place_body["uri"]
      puts "  URI: #{uri}"
      if !uri.nil?
        if uri.start_with?(PASTPLACE_PREFIX)
          rewrite_pastplace(place_body)
          rewritten = true
        elsif uri.start_with?(MAP_HIST_PREFIX)
          rewritten = rewrite_maphist(place_body, quote_body, concordances)
          if !rewritten
            # TODO remove this body
          end
        end
      end
    end

    rewritten
  end

  if ARGV.empty?
    puts("no input file")
  else
    filename = ARGV[0]
    File.open(filename, "r") do |f|
      ctr = [0, 0]
      f.each_line do |line|
        ctr[0] += 1
        puts "--Record #{ctr[0]} (#{ctr[1]} matches so far)"
        rewritten = rewrite_one(JSON.parse(line), concordances)
        if rewritten
          ctr[1] += 1
        end
      end
      puts "#{ctr} URIs rewritten"
    end
  end
end

rewrite_annotations(Concordances.new("portolan_precursors_recogito.csv"))

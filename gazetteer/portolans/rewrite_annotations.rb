require 'csv'
require 'json'

@MAP_HIST_PREFIX = "http://www.maphistory.info/portolans/record/"

def load_concordances
  concordances = {}

  csv_text = File.read("portolan_precursors_recogito.csv")
  csv = CSV.parse(csv_text, :headers => true, :col_sep => ';')
  csv.each do |row|
    maphist_id = row[0].split('-')
    maphist_sorting = maphist_id[1]
    maphist_line_number = maphist_id[0]

    mapped_uri = row[2]
    status     = row[6]

    if status == "VERIFIED" && !mapped_uri.empty?
      record = {
        'sorting'     => maphist_sorting,
        'line_number' => maphist_line_number,
        'uri'         => @MAP_HIST_PREFIX + row[0],
        'mapped_uri'  => row[2],
        'toponym'     => row[1]
      }

      existing_records = concordances[maphist_sorting]
      if (existing_records.nil?)
        concordances[maphist_sorting] = [record]
      else
        existing_records << record
      end
    end
  end

  concordances
end

def rewrite_annotations(concordances)

  def parseURI(uri)
    id = uri[@MAP_HIST_PREFIX.length .. -1].split('-')
    { "sorting" => id[1], "line_number" => id[0] }
  end

  def rewrite_one(annotation, concordances)
    rewritten = false
    bodies = annotation["bodies"]
    placeBody = bodies.select do |b|
      b["type"] == "PLACE"
    end

    if !placeBody.empty?
      uri = placeBody[0]["uri"]
      if !uri.nil? && uri.start_with?(@MAP_HIST_PREFIX)
        id = parseURI(uri)
        concordance = concordances[id['sorting']]
        if (concordance.nil?)
          # TODO what to do?
          puts "No concordance found for #{uri}, #{id}"
        elsif concordance.length == 1
          # TODO replace
          replacement = concordance[0]['mapped_uri']
          offset = concordance[0]['line_number'].to_i - id['line_number'].to_i
          if offset == 0
            puts "SUPER exact match for #{uri} -> #{replacement}"
          else
            puts "Exact (offset #{offset}) match for #{uri} -> #{replacement}"
          end
          rewritten = true
        else
          puts "Multiple matches for #{uri}"
          rewritten = true
        end

      end
    end

    # TODO replace with concordance if available
    # TODO or remove the Place body if not

    rewritten
  end

  if ARGV.empty?
    puts("no input file")
  else
    filename = ARGV[0]
    File.open(filename, "r") do |f|
      ctr = 0
      f.each_line do |line|
        rewritten = rewrite_one(JSON.parse(line), concordances)
        if rewritten
          ctr += 1
        end
      end
      puts "#{ctr} URIs rewritten"
    end
  end
end

concordances = load_concordances()
rewrite_annotations(concordances)

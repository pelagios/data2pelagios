require 'csv'

class Concordances

  @@MAP_HIST_PREFIX = "http://www.maphistory.info/portolans/record/"

  def initialize(filename)
    @concordances = {}

    csv_text = File.read(filename)
    csv = CSV.parse(csv_text, :headers => true, :col_sep => ';')
    csv.each do |row|
      maphist_id = row[0].split('-')
      maphist_sorting = maphist_id[1]
      maphist_line_number = maphist_id[0]

      mapped_uri = row[2]
      status     = row[6]

      if status == "VERIFIED" && !mapped_uri.empty?
        record = {
          "sorting"     => maphist_sorting,
          "line_number" => maphist_line_number,
          "uri"         => @@MAP_HIST_PREFIX + row[0],
          "mapped_uri"  => row[2],
          "toponym"     => row[1]
        }

        existing_records = @concordances[maphist_sorting]
        if (existing_records.nil?)
          @concordances[maphist_sorting] = [record]
        else
          existing_records << record
        end
      end
    end
  end

  def get(sorting, line_number, toponym)
    matches = @concordances[sorting]
    if (matches.nil?)
      puts "  No concordance found for #{line_number}-#{sorting}"
    elsif matches.length == 1
      offset = matches[0]["line_number"].to_i - line_number.to_i
      puts "  One concordance found (offset #{offset})"
      matches[0]["mapped_uri"]
    else
      puts "  Multiple possible matches for #{toponym}:"

      maybeExact = matches.select do |m|
        m["line_number"] == line_number
      end

      if maybeExact.empty?
        # No exact match - query user
        matches.each_with_index do |match, idx|
          offset = match["line_number"].to_i - line_number.to_i
          puts "  [#{idx}] #{match['line_number']} #{match['toponym']}, offset #{offset}"
        end

        selection = $stdin.gets.chomp.to_i
        puts "  Returning selection #{selection}"
        matches[selection]["mapped_uri"]
      else
        # Exact match
        puts "  Exact line number match"
        maybeExact[0]["mapped_uri"]
      end

    end
  end

end

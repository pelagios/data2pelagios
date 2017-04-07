require 'csv'

def load_concordances
  concordances = {}

  csv_text = File.read('portolan_precursors_recogito.csv')
  csv = CSV.parse(csv_text, :headers => true, :col_sep => ';')
  csv.each do |row|
    maphist_id = row[0]
    mapped_uri = row[2]
    status     = row[6]

    if status == 'VERIFIED' && !mapped_uri.empty?
      concordances['http://www.maphistory.info/portolans/record/' + maphist_id] = mapped_uri
    end
  end

  concordances
end

def rewrite_annotations(concordances)
  if ARGV.empty?
    puts('no input file')
  else
    # TODO read file, get all map_hist URIs
    # TODO replace with concordance if available
    # TODO or remove the Place body if not
  end
end

concordances = load_concordances()
rewrite_annotations(concordances)

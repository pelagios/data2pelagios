require 'csv'

input_file = ARGV

def load_concordances
  concordances = {}

  csv_text = File.read('portolan_precursors_recogito.csv')
  csv = CSV.parse(csv_text, :headers => true, :col_sep => ';')
  csv.each do |row|
    maphist_id = row[0]
    mapped_id  = row[2]
    status     = row[6]

    if status == 'VERIFIED' && !mapped_id.empty?
      puts(maphist_id + ' -> ' + mapped_id)
    end
  end

  concordances
end

def rewrite_annotations(concordances)
end

concordances = load_concordances()
rewrite_annotations(concordances)

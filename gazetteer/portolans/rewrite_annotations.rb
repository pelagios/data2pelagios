require 'csv'

input_file = ARGV

def load_concordances
  csv_text = File.read('portolan_precursors_recogito.csv')
  csv = CSV.parse(csv_text, :headers => true, :col_sep => ';')
  csv.each do |row|
    # TODO implement
  end
end

def rewrite_annotations
end

load_concordances()
rewrite_annotations()

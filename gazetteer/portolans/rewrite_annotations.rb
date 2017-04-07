require 'csv'

csv_text = File.read('portolan_precursors_recogito.csv')
csv = CSV.parse(csv_text, :headers => true, :col_sep => ';')
csv.each do |row|
  # TODO implement
  puts(row[0])
end
